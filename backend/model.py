from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, Column, Date, Time, DateTime, ForeignKey, Text

db = SQLAlchemy()

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True,nullable=False)
    password = Column(String(32),nullable=False)
    name = Column(String(64),nullable=False)
    is_admin = Column(Boolean,nullable=False, default=False)
    email = Column(String(64),nullable=False)

    score = db.relationship('Scores', backref='user', lazy=True, cascade='all, delete-orphan')
    notify = db.relationship('Notify', backref='user', lazy=True, cascade='all, delete-orphan')
    def convert_to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'is_admin': self.is_admin,
            'email': self.email
        }

class Subject(db.Model):
    id = Column(Integer, primary_key=True)
    sname = Column(String(32), unique=True,nullable=False)
    description = Column(Text, default='No Description')
    
    chapter = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

    def convert_to_json(self):
        return {
            'id': self.id,
            'sname': self.sname,
            'description': self.description 
        }

class Chapter(db.Model):
    id = Column(Integer, primary_key=True)
    chname = Column(String(32), unique=True,nullable=False)
    description = Column(Text, default='No Description')
    sname = Column(String(32),ForeignKey('subject.sname'),nullable=False)
    
    quizz = db.relationship('Quizz', backref='chapter', lazy=True, cascade='all, delete-orphan')
    notify = db.relationship('Notify', backref='chapter', lazy=True, cascade='all, delete-orphan')

    def convert_to_json(self):
        return {
            'id': self.id,
            'chname': self.chname,
            'description': self.description, 
            'sname': self.sname
        }

class Quizz(db.Model):
    id = Column(Integer, primary_key=True)
    topic = Column(String(32), unique=True,nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Time, nullable=False)
    chname = Column(String(32),ForeignKey('chapter.chname'),nullable=False)
    remarks = Column(Text, default='No Remarks')

    score = db.relationship('Scores', backref='quizz', lazy=True, cascade='all, delete-orphan')
    question = db.relationship('Question', backref='quizz', lazy=True, cascade='all, delete-orphan')

    def convert_to_json(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "chname": self.chname,
            "date": self.date.strftime("%Y-%m-%d"),  
            "duration": self.duration.strftime("%H:%M"),  
            "remarks": self.remarks if self.remarks else ""
        }
    
class Question(db.Model):
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer,ForeignKey('quizz.id'),nullable=False)
    question = Column(Text, unique=True, nullable=False)

    answer = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')

    def convert_to_json(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question': self.question
        }

class Answer(db.Model):
    id = Column(Integer, primary_key=True)
    ques_id = Column(Integer,ForeignKey('question.id'),nullable=False)
    answer = Column(Text, nullable=False)
    is_true = Column(Boolean, nullable=False, default=False)

    def convert_to_json(self):
        return {
            'id': self.id,
            'ques_id': self.ques_id,
            'answer': self.answer,
            'is_true': self.is_true
        }

class Scores(db.Model):
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    username = Column(String(32),nullable=False)
    attempt = Column(Integer, nullable=False)
    quiz_id = Column(Integer,ForeignKey('quizz.id'),nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'),nullable=False)

    def convert_to_json(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'score': self.score,
            'username': self.username,
            'attempt': self.attempt
        }

class Notify(db.Model):
    id = Column(Integer, primary_key=True)
    time = Column(Time, nullable=False)
    chap_id = Column(Integer,ForeignKey('chapter.id'),nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'),nullable=False)
    def convert_to_json(self):
        
        return {
            'id' : self.id,
            'time' : self.time.strftime("%H:%M"),
            'chap_id' : self.chap_id,
            'user_id' : self.user_id,
        }