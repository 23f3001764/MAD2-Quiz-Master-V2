from flask import Flask,request,redirect
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_caching import Cache
from datetime import datetime
from model import db, User, Subject, Chapter, Quizz, Question, Answer, Scores, Notify
from task import download_csv, send_monthly_report, notify

cache=Cache()
class ExportAPT(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()

        # Prevent admin from generating CSV
        if user.get('isadmin'):
            return {'message': 'Unauthorized Access'}, 401

        # Start the CSV generation task
        result = download_csv.delay(user.get('user_id'))

        # Return only the task ID (result.result is not available yet)
        return {'id': result.id}, 202


class NotifyAPI(Resource):
    @jwt_required()
    def get(self,chap_id=None):
        user = get_jwt_identity()
        if user.get('isadmin'):
            return {'message':'Unauthorized Access'}, 401
        notify = Notify.query.filter_by(chap_id=chap_id).all()
        if not chap_id:
            notify = Notify.query.filter_by(user_id=user.get('user_id'))
        notify_json = list()
        for n in notify:
            notify_json.append(n.convert_to_json())
        return notify_json, 200
    
    @jwt_required()
    def post(self, chap_id):
        user = get_jwt_identity()
        if user.get('isadmin'):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        if not data.get('time'):
            return {'message':'Please provide time.'}, 400
        try: 
            time = datetime.strptime(data.get('time').strip(), "%H:%M").time()
        except ValueError:
            return {'message': 'Invalid time format. Use HH:MM for time.'}, 400
        notify = Notify(chap_id=chap_id,time=time,user_id = user.get('user_id'))
        db.session.add(notify)
        db.session.commit()
        return notify.convert_to_json(), 201

    @jwt_required()
    def delete(self, notify_id):
        user = get_jwt_identity()
        if user.get('isadmin'):
            return {'message':'Unauthorized Access'}, 401
        notify = Notify.query.filter_by(id=notify_id).first()
        if not notify:
            return {'message':'Notify not found'}, 404
        db.session.delete(notify)
        db.session.commit()
        return {'message':'Notify deleted successfully.'}, 200
class UserAPI(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        if not user.get('isadmin'):
            return {'message':'Unauthorized Access'}, 401
        user = User.query.all()
        user_json = list()
        for u in user:
            user_json.append(u.convert_to_json())
        return user_json, 200
    
class LoginAPI(Resource):
    def post(self):
        data = request.json
        if not((data.get('email') or data.get('username')) and data.get('password')):
            return {'message':'Please fill all the required fields.'}, 400
        if data.get('email'):
            if '@' not in data.get('email') or '.com' not in data.get('email'):
                return {'message':'Please give the correct format of email.'}, 400
            user = User.query.filter_by(email=data.get('email').strip()).first()
        elif data.get('username'):
            user = User.query.filter_by(username=data.get('username').strip()).first()
        if not user:
            return {'message':'User not Found'}, 404
        if user:
            if user.password == data.get('password').strip():
                token = create_access_token({'isadmin':user.is_admin, 'user_id':user.id,'username':user.username})
                return {'message':'user logged in sucessfully.',
                        'token':token,
                        'user_id':user.id,
                        'isadmin':user.is_admin,
                        'username':user.username}, 200
            return {'message':'Incorrect Password.'}, 400
        return {'message':'User not Found'}, 404
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        return {'isadmin': user.get('isadmin')}, 200

class SignupAPI(Resource):
    def post(self):
        data = request.json
        if not(data.get('name') and data.get('email') and data.get('password') and data.get('username')):
            return {'message':'Please fill all the required fields.'}, 400
        if len(data.get('username').strip()) < 3 or len(data.get('username').strip()) > 32:
            return {'message':'Username length must be greater than 3 and leass than 32 character.'}, 400
        if len(data.get('password').strip()) < 3 or len(data.get('password').strip()) > 32:
            return {'message':'Password length must be greater than 3 and leass than 32 character.'}, 400
        if len(data.get('name').strip()) < 3 or len(data.get('name').strip()) > 64:
            return {'message':'Name length must be greater than 3 and leass than 64 character.'}, 400
        if len(data.get('email').strip()) < 3 or len(data.get('email').strip()) > 64 or '@' not in data.get('email') or '.com' not in data.get('email'):
            return {'message':'Email length must be greater than 3 and leass than 64 character and must contain "@" and ".com"'}, 400
        user = User.query.filter_by(email=data.get('email').strip()).first()
        username = User.query.filter_by(username=data.get('username').strip()).first()
        if user:
            return {'message':'Email already Exist'}, 400
        if username:
            return {'message':'Username already Exist, Please choose different user name'}, 400
        new_user = User(name=data.get('name').strip(),email=data.get('email').strip(),password=data.get('password').strip(), username=data.get('username').strip())
        db.session.add(new_user)
        db.session.commit()
        return {'message':'user sign up sucessfully.'}, 200
    
    def get(self,username):

        if not username:
            return {'message': 'Username is required'}, 400
        user = User.query.filter_by(username=username.strip()).first()
        if user:
            return {'message': 'Username already taken'}, 400
        return {'message': 'Username is available'}, 200

class SubjectAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=20)
    def get(self,subject_id=None):
        subject=Subject.query.all()
        if subject_id:
            subject = Subject.query.filter_by(id=subject_id).first()
            if subject:
                return subject.convert_to_json(), 200
        print(subject)
        sub_json = list()
        for sub in subject:
            sub_json.append(sub.convert_to_json())
        return sub_json, 200

    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        if not(data.get('sname')):
            return {'message':'Please fill all the required fields.'}, 400
        subject =Subject.query.filter_by(sname=data.get('sname')).first()
        if subject:
            return {'message':'Subject already Exist'}, 400
        if data.get('description'):
            new_subject = Subject(sname=data.get('sname').strip(),description=data.get('description').strip())
        if not (data.get('description')):
            new_subject = Subject(sname=data.get('sname').strip())
        db.session.add(new_subject)
        db.session.commit()
        return {'message':'subject added sucessfully.'}, 200
    
    @jwt_required()
    def put(self, subject_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        subject = Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {'message':'Subject not found'}, 404
        new_sname = data.get('sname')
        if new_sname.strip() != subject.sname:
            existing_subject = Subject.query.filter_by(sname=new_sname.strip()).first()
            if existing_subject:
                return {'message': 'Subject name already exists'}, 400
            subject.sname= new_sname.strip()
        subject.description = data.get('description').strip() if data.get('description') else subject.description
        db.session.commit()
        return {'message':'Subject edited sucessfully.'}, 200
    
    @jwt_required()
    def delete(self, subject_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        subject = Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {'message':'Subject not found'}, 404
        db.session.delete(subject)
        db.session.commit()
        return {'message':'Subject deleted sucessfully.'}, 200
    
class ChapterAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=20)
    def get(self, sname=None, chapter_id=None):
        if chapter_id:
            chapter = Chapter.query.filter_by(id=chapter_id).first()
            if not chapter:
                return {'message': 'Chapter not found'}, 404
            return chapter.convert_to_json(), 200 

        chapters = Chapter.query.filter_by(sname=sname).all()
        if not chapters:
            return {'message': 'No chapters found for the given subject'}, 404

        return [chap.convert_to_json() for chap in chapters], 200  


    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        if not(data.get('sname') and data.get('chname')):
            return {'message':'Please fill all the required fields.'}, 400
        chapter =Chapter.query.filter_by(chname=data.get('chname')).first()
        if chapter:
            return {'message':'Chapter already Exist'}, 400
        if data.get('description'):
            new_chapter = Chapter(chname=data.get('chname').strip(),sname=data.get('sname').strip(),description=data.get('description').strip())
        if not (data.get('description')):
            new_chapter = Chapter(chname=data.get('chname').strip(),sname=data.get('sname').strip())
        db.session.add(new_chapter)
        db.session.commit()
        return {'message':'Chapter added sucessfully.'}, 200
    
    @jwt_required()
    def put(self, chapter_id):
        user = get_jwt_identity()
        if not user.get('isadmin'):
            return {'message': 'Unauthorized Access'}, 401
    
        data = request.json
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        new_chname = data.get('chname')
        if new_chname and new_chname.strip() != chapter.chname:
            existing_chapter = Chapter.query.filter_by(chname=new_chname.strip()).first()
            if existing_chapter:
                return {'message': 'Chapter name already exists'}, 400
            chapter.chname = new_chname.strip()

        chapter.description = data.get('description', chapter.description).strip()

        db.session.commit()
        return {'message': 'Chapter edited successfully.'}, 200

    @jwt_required()
    def delete(self, chapter_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message':'Chapter not found'}, 404
        db.session.delete(chapter)
        db.session.commit()
        return {'message':'Chapter deleted sucessfully.'}, 200
    
class QuizAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=20)
    def get(self, chname=None, quiz_id=None):
        if quiz_id:
            quizz = Quizz.query.filter_by(id=quiz_id).first()
            if not quizz:
                return {'message': 'Quiz not found'}, 404
            return quizz.convert_to_json(), 200 

        quizz = Quizz.query.filter_by(chname=chname).all()
        if not quizz:
            return {'message': 'No Quiz found for the given Chapter'}, 404

        return [quiz.convert_to_json() for quiz in quizz], 200  

    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        if not(data.get('topic') and data.get('chname') and data.get('date') and data.get('duration')):
            return {'message':'Please fill all the required fields.'}, 400
        try:
            quiz_date = datetime.strptime(data.get('date').strip(), "%Y-%m-%d").date()
            duration_time = datetime.strptime(data.get('duration').strip(), "%H:%M").time()
        except ValueError:
            return {'message': 'Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.'}, 400
        if data.get('remarks'):
            new_quiz = Quizz(topic=data.get('topic').strip(),date=quiz_date,chname=data.get('chname').strip(),duration=duration_time,remarks=data.get('remarks').strip())
        if not (data.get('remarks')):
            new_quiz = Quizz(topic=data.get('topic').strip(),date=quiz_date,chname=data.get('chname').strip(),duration=duration_time)
        db.session.add(new_quiz)
        db.session.commit()
        notify = Notify.query.filter_by(chap_id=data.get('chname')).all()
        for n in notify:
            response = notify.delay(n.user_name)
        return {'message':'Quizz added sucessfully.'}, 200
    
    @jwt_required()
    def put(self, quiz_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        quiz =Quizz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message':'Quiz not found'}, 404
        quiz.remarks = data.get('remarks').strip() if data.get('remarks') else quiz.remarks
        try:
            quiz_date = datetime.strptime(data.get('date').strip(), "%Y-%m-%d").date()
            duration_time = datetime.strptime(data.get('duration').strip(), "%H:%M").time()
        except ValueError:
            return {'message': 'Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.'}, 400
       
        quiz.topic = data.get('topic').strip() if data.get('topic') else quiz.topic
        quiz.date = quiz_date if quiz_date else quiz.date
        quiz.duration = duration_time if duration_time else quiz.stime
        db.session.commit()
        return {'message':'Chapter edited sucessfully.'}, 200
    
    @jwt_required()
    def delete(self, quiz_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        quiz =Quizz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message':'Quiz not found'}, 404
        db.session.delete(quiz)
        db.session.commit()
        return {'message':'Quiz deleted sucessfully.'}, 200

class QuestionAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=5)
    def get(self, ques_id=None, quiz_id=None):
        if ques_id:
            ques = Question.query.filter_by(id=ques_id).first()
            return ques.convert_to_json(), 200
        ques = Question.query.filter_by(quiz_id=quiz_id).all()
        if not ques:
            return {'message': 'No Question found for the given Quiz'}, 404
        
        return [q.convert_to_json() for q in ques], 200


    @jwt_required()
    def post(self,quiz_id=None):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        if not( data.get('question')):
            return {'message':'Please fill all the required fields.'}, 400
        ques = Question.query.filter_by(question=data.get('question').strip()).first()
        if ques:
            return {'message':'Question already Exist'}, 400
        new_ques = Question(quiz_id=quiz_id,question=data.get('question').strip())
        db.session.add(new_ques)
        db.session.commit()
        return {'message':'Question added sucessfully.'}, 200
    
    @jwt_required()
    def put(self, ques_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        ques =Question.query.filter_by(id=ques_id).first()
        if not ques:
            return {'message':'Question not found'}, 404
        quess = Question.query.filter_by(question=data.get('question').strip()).first()
        if quess:
            return {'message':'Question already Exist'}, 400
        ques.quiz_id = data.get('quiz_id').strip() if data.get('quiz_id') else ques.quiz_id
        ques.question = data.get('question').strip() if data.get('question') else ques.question
        db.session.commit()
        return {'message':'Question edited sucessfully.'}, 200
    
    @jwt_required()
    def delete(self, ques_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        ques =Question.query.filter_by(id=ques_id).first()
        if not ques:
            return {'message':'Question not found'}, 404
        db.session.delete(ques)
        db.session.commit()
        return {'message':'Question deleted sucessfully.'}, 200

class AnswerAPI(Resource):
    @jwt_required()
    def get(self, ques_id=None, ans_id=None):
        if ans_id:
            ans = Answer.query.filter_by(id=ans_id).first()
            return ans.convert_to_json(), 200
        ans = Answer.query.filter_by(ques_id=ques_id).all()
        if not ans:
            return {'message': 'No Answer found for the given Question'}, 404
        
        return [a.convert_to_json() for a in ans], 200


    @jwt_required()
    def post(self,ques_id=None):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        if not(ques_id and data.get('answer')):
            return {'message':'Please fill all the required fields.'}, 400
        if data.get('is_true'):
            new_ans = Answer(ques_id=ques_id,answer=data.get('answer').strip(),is_true=data.get('is_true'))
        if not(data.get('is_true')):
            new_ans = Answer(ques_id=ques_id,answer=data.get('answer').strip())
        db.session.add(new_ans)
        db.session.commit()
        return {'message':'Answer added sucessfully.'}, 200
    
    @jwt_required()
    def put(self, ans_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        data = request.json
        answer =Answer.query.filter_by(id=ans_id).first()
        if not answer:
            return {'message':'Answer not found'}, 404
        answer.is_true = data.get('is_true') if data.get('is_true') else answer.is_true
        answer.answer = data.get('answer').strip() if data.get('answer') else answer.answer
        db.session.commit()
        return {'message':'Answer edited sucessfully.'}, 200
    
    @jwt_required()
    def delete(self, ans_id):
        user = get_jwt_identity()
        if not(user.get('isadmin')):
            return {'message':'Unauthorized Access'}, 401
        answer =Answer.query.filter_by(id=ans_id).first()
        if not answer:
            return {'message':'Answer not found'}, 404
        db.session.delete(answer)
        db.session.commit()
        return {'message':'Answer deleted sucessfully.'}, 200

class ScoreAPI(Resource):
    @jwt_required()
    def get(self, score_id=None,user_id=None,quiz_id=None):
        user = get_jwt_identity()

        if score_id:
            score = Scores.query.filter_by(id=score_id).first()
            if not score:
                return {'message': 'Score not found'}, 404
            return score.convert_to_json(), 200
        elif user_id and quiz_id:
            score = Scores.query.filter_by(user_id=user_id, quiz_id=quiz_id).all()
            if not score:
                return {'message': 'Score not found'}, 404
            return [sc.convert_to_json() for sc in score], 200
        elif user_id:
            scores = Scores.query.filter_by(user_id=user_id).all()
            if not scores:
                return {'message': 'No scores found for the given user'}, 404
            return [sc.convert_to_json() for sc in scores], 200
        else:
            scores = Scores.query.all()

            if not scores:
                return {'message': 'No scores found'}, 404

        return [sc.convert_to_json() for sc in scores], 200

    @jwt_required()
    def post(self, quiz_id=None):
        user = get_jwt_identity()
        if user.get('isadmin'):
            return {'message': 'Unauthorized Access'}, 401

        data = request.json
        if not (quiz_id and data.get('username') and data.get('attempt') and data.get('user_id')):
            return {'message': 'Please fill all the required fields.'}, 400

        new_score = Scores(quiz_id=quiz_id,score=data.get('score') if data.get('score') else 0,username=data.get('username'),
            attempt=data.get('attempt'),user_id=data.get('user_id'))
        db.session.add(new_score)
        db.session.commit()
        return {'message': 'Score added successfully.'}, 201


    @jwt_required()
    def delete(self, score_id):
        user = get_jwt_identity()
        if user.get('isadmin'):
            return {'message': 'Unauthorized Access'}, 401

        score = Scores.query.filter_by(id=score_id).first()
        if not score:
            return {'message': 'Score not found'}, 404

        db.session.delete(score)
        db.session.commit()
        return {'message': 'Score deleted successfully.'}, 200
