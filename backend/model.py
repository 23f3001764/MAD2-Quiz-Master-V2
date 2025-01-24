from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,Boolean, Column, Date, Time, DateTime, ForeignKey, Text
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True,nullable=False)
    password = Column(String(256),nullable=False)
    name = Column(String(32),nullable=False)
    is_admin = Column(Boolean,nullable=False, default=False)
    email = Column(String(32),nullable=False)

    score = db.relationship('Scores', backref='user', lazy=True, cascade='all, delete-orphan')

class Subject(db.Model):
    id = Column(Integer, primary_key=True)
    sname = Column(String(32), unique=True,nullable=False)
    score = db.relationship('Scores', backref='subject', lazy=True, cascade='all, delete-orphan')
    quizz = db.relationship('Quizz', backref='subject', lazy=True, cascade='all, delete-orphan')

class Quizz(db.Model):
    id = Column(Integer, primary_key=True)
    topic = Column(String(32), unique=True,nullable=False)
    date = Column(Date, nullable=False)
    stime = Column(Time, nullable=False)
    etime = Column(Time, nullable=False)
    subject_id = Column(Integer,ForeignKey('subject.id'),nullable=False)
    score = db.relationship('Scores', backref='quizz', lazy=True, cascade='all, delete-orphan')
    score = db.relationship('Question', backref='quizz', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer,ForeignKey('quizz.id'),nullable=False)
    question = Column(Text, unique=True, nullable=False)

    answer = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')

class Answer(db.Model):
    id = Column(Integer, primary_key=True)
    ques_id = Column(Integer,ForeignKey('question.id'),nullable=False)
    answer = Column(Text, nullable=False)
    is_true = Column(Boolean, nullable=False, default=False)

class Scores(db.Model):
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    username = Column(String(32), unique=True,nullable=False)
    rank = Column(Integer, nullable=False)
    quiz_id = Column(Integer,ForeignKey('quizz.id'),nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'),nullable=False)
    subject_id = Column(Integer,ForeignKey('subject.id'),nullable=False)

with app.app_context():
    db.create_all()
    
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(username='admin', password=2025, name='Admin', is_admin=True ,email="23f3001764@ds.study.iitm.ac.in")
        db.session.add(admin)
        db.session.commit()