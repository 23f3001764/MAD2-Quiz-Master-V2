from celery import shared_task
import os
import requests
import json
import csv
from model import db, Scores, User, Quizz  
from email_utils import send_email
from jinja2 import Template
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import shared_task

def avgscore(user_id):
    avg_scores = {}

    # Get all quiz IDs attempted by the user
    user_scores = Scores.query.filter_by(user_id=user_id).all()
    quiz_ids = set(score.quiz_id for score in user_scores)

    for quiz_id in quiz_ids:
        user_quiz_scores = Scores.query.filter_by(user_id=user_id, quiz_id=quiz_id).all()
        
        total_score = sum(s.score for s in user_quiz_scores)
        count = len(user_quiz_scores)
        
        avg_scores[quiz_id] = round(total_score / count, 2) if count else 0  # Rounded for cleaner CSV

    return avg_scores

@shared_task(ignore_result=False, name="download_csv")
def download_csv(user_id):
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return "User not found"

    # Ensure the 'static' directory exists
    static_dir = "static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    csv_file = f'{static_dir}/{user.name}_report.csv'

    with open(csv_file, 'w', newline='') as f:
        trans_csv = csv.writer(f, delimiter=',')
        trans_csv.writerow(['Sr.No.', 'Quiz Title', 'Score', 'AvgScore', 'Attempt'])

        # Get user-specific average scores per quiz
        avg_scores = avgscore(user.id) 

        # Fetch user scores
        scores = Scores.query.filter_by(user_id=user.id).all()
        sr_no = 1

        for score in scores:
            quiz = Quizz.query.filter_by(id=score.quiz_id).first()
            trans_csv.writerow([sr_no, quiz.topic, score.score, avg_scores.get(score.quiz_id, 0), score.attempt])
            sr_no += 1

    return f"{user.name}_report.csv"



template_path = "templates/report_template.html"

def render_template(user,template_path=template_path):
    if not os.path.exists(template_path):
        return "Template not found"
    
    with open(template_path, "r") as file:
        template = Template(file.read())
    
    # Calculate average scores before rendering
    user_avg_scores = avgscore(user.id)
    
    # Add calculated values to user object for template rendering
    user_data = {
        "name": user.name,
        "email": user.email,
        "scores": []
    }
    scores = Scores.query.filter_by(user_id=user.id).all()
    for score in scores:
        quiz = Quizz.query.filter_by(id=score.quiz_id).first()
        user_data["scores"].append({
            "quiz_title": quiz.topic,
            "score": score.score,
            "avg_score": user_avg_scores.get(score.quiz_id, 0),
            "attempt": score.attempt
        })
    
    return template.render(user=user_data)

@shared_task(ignore_result=False, name="send_monthly_report")
def send_monthly_report():
    users = User.query.all()
    users = users[1:]
    if not users:
        return "No users found"
    
    for user in users:
        email_content = render_template(user)
        subject = f"Monthly Report for {user.name}"
        to_address = user.email
        
        send_email(to_address, subject, email_content, content="html")
        
    return "Monthly reports sent to all users"


@shared_task(ignore_result=False, name= "Notification")
def notify(username):
    text = f"Hi {username}, The chapter which you are intrested in have new quizzes. Please check the app at http://127.0.0.1:5000"
    
    url = "https://chat.googleapis.com/v1/spaces/AAAAhr23WlM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fQ5pAbeWcLecsKVGFd-1tlsb0mblfcx2LpcD2Pyv_as"

    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return 'message sent to the user'
