from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from model import db,User
import os
from datetime import timedelta
from api import LoginAPI, SignupAPI, cache, NotifyAPI, UserAPI, SubjectAPI, ChapterAPI, QuizAPI, QuestionAPI, AnswerAPI, ScoreAPI

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


api = Api(app)
jwt = JWTManager(app)
app.app_context().push()
cache.init_app(app)
db.init_app(app)

def add_admin():
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(username='admin', password=2025, name='Admin', is_admin=True ,email="23f3001764@ds.study.iitm.ac.in")
        db.session.add(admin)
        db.session.commit()

api.add_resource(SignupAPI, '/api/signup', '/api/signup/<string:username>')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(NotifyAPI,  '/api/notify','/api/notify/<int:notify_id>'  ,'/api/notifies/<int:chap_id>')
api.add_resource(UserAPI, '/api/user')
api.add_resource(SubjectAPI, '/api/subject', '/api/subject/<int:subject_id>')
api.add_resource(ChapterAPI, '/api/chapter', '/api/chapter/<string:sname>','/api/chapter/<int:chapter_id>')
api.add_resource(QuizAPI, '/api/quiz', '/api/quiz/<string:chname>', '/api/quiz/<int:quiz_id>')
api.add_resource(QuestionAPI, '/api/ques', '/api/ques/<int:quiz_id>', '/api/question/<int:ques_id>')
api.add_resource(AnswerAPI, '/api/ans', '/api/ans/<int:ans_id>', '/api/answer/<int:ques_id>')
api.add_resource(ScoreAPI, '/api/score', '/api/score/<int:score_id>' ,'/api/scores/<int:quiz_id>', '/api/scores/<int:quiz_id>/<int:user_id>' , '/api/sco/<int:user_id>')

if __name__=="__main__":
    db.create_all()
    add_admin()
    app.run(debug=True)