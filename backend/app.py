from flask import Flask, send_from_directory,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from model import db, User, Scores  # ✅ Added Scores
from api import (
    LoginAPI, SignupAPI, SubjectAPI, QuizAPI, QuestionAPI,
    AnswerAPI, ScoreAPI, ChapterAPI, UserAPI, NotifyAPI, ExportAPT, cache
)
from worker import celery_init_app
from task import send_monthly_report  # ✅ Added missing import
import os
from datetime import timedelta
from celery.result import AsyncResult
from celery.schedules import crontab

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
app.config["JWT_SECRET_KEY"] = "879456123"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_DEFAULT_TIMEOUT'] = 500

celery = celery_init_app(app)  # ✅ No autodiscover_tasks()

api = Api(app)
jwt = JWTManager(app)
app.app_context().push()  # ✅ Ensure context before setting celery schedule
cache.init_app(app)
db.init_app(app)

def add_admin():
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(username='admin', password=2025, name='Admin', is_admin=True, email="23f3001764@ds.study.iitm.ac.in")
        db.session.add(admin)
        db.session.commit()

api.add_resource(SignupAPI, '/api/signup', '/api/signup/<string:username>')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(ExportAPT, '/api/export')
api.add_resource(NotifyAPI, '/api/notify', '/api/notify/<int:notify_id>', '/api/notifies/<int:chap_id>')
api.add_resource(UserAPI, '/api/user')
api.add_resource(SubjectAPI, '/api/subject', '/api/subject/<int:subject_id>')
api.add_resource(ChapterAPI, '/api/chapter', '/api/chapter/<string:sname>', '/api/chapter/<int:chapter_id>')
api.add_resource(QuizAPI, '/api/quiz', '/api/quiz/<string:chname>', '/api/quiz/<int:quiz_id>')
api.add_resource(QuestionAPI, '/api/ques', '/api/ques/<int:quiz_id>', '/api/question/<int:ques_id>')
api.add_resource(AnswerAPI, '/api/ans', '/api/ans/<int:ans_id>', '/api/answer/<int:ques_id>')
api.add_resource(ScoreAPI, '/api/score', '/api/score/<int:score_id>', '/api/scores/<int:quiz_id>', '/api/scores/<int:quiz_id>/<int:user_id>', '/api/sco/<int:user_id>')

@app.route('/api/check/<id>/<quiz_id>')
def check_answer(id, quiz_id):
    score = Scores.query.filter_by(user_id=id, quiz_id=quiz_id).first()
    if not score:
        return {'message': 'False'}, 200
    return {'message': 'True'}, 200

@app.route('/api/csv_result/<id>')
def csv_result(id):
    res = AsyncResult(id, app=celery)

    if not res.successful():
        return jsonify({'error': 'File not ready or task failed'}), 400
    file_name = res.result

    if not isinstance(file_name, str) or not file_name.endswith('.csv'):
        return jsonify({'error': 'Invalid file result'}), 500

    file_path = os.path.join('static', file_name)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    return send_from_directory(directory='static', path=file_name, as_attachment=True)
celery.conf.beat_schedule = {
    'send_monthly_report_task': {
        'task': 'send_monthly_report',
        'schedule': crontab(minute='*/2'), 
        # 'schedule': crontab(hour=0, minute=0,day_of_month=1, month_of_year='*'), 
    },
}

@app.route('/api/email')
def email():
    res = send_monthly_report.delay()
    return {'task_id': res.id, 'status': res.status, 'result': res.result}

if __name__ == "__main__":
    with app.app_context():  # ✅ Ensures correct DB initialization
        db.create_all()
        add_admin()
    app.run(debug=True)
