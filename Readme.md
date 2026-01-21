# 🎯 Quiz Master App

A full-stack quiz management system built as part of the App Development Project for the IIT Madras BS Degree Program.

---

## 👤 Author

**Sahil Raj**  
BS in Data Science and Applications  
IIT Madras  
Email: 23f3001764@ds.study.iitm.ac.in  

---

## 📌 Project Description

Quiz Master App is a complete quiz management platform with both frontend and backend implementation.

The application allows users to:
- Register and login securely
- Attempt quizzes across different subjects and chapters
- Participate in time-bound quizzes
- Track scores and attempts
- Receive quiz notifications

Admins can:
- Create subjects, chapters, and quizzes
- Add questions and answers
- Monitor user scores
- Send quiz notifications

---

## 🛠️ Tech Stack

### Backend
- Flask (3.0.3)
- Flask-SQLAlchemy (3.1.1)
- Flask-RESTful (0.3.10)
- Flask-JWT-Extended (4.6.0)
- Flask-Caching (2.3.1)
- Celery (5.4.0)
- Redis (5.2.1)

### Frontend
- Vue.js (Vue 3 CLI)
- JavaScript
- HTML
- CSS
- Bootstrap CDN

### Database
- SQLite / SQLAlchemy ORM

---

## ⚙️ Features

- Secure JWT Authentication
- Timed Quizzes
- Multiple Subjects & Chapters
- MCQ Based Questions
- Score Tracking
- Admin Panel
- Quiz Notifications
- Background Tasks using Celery
- Redis Caching

---

## 🧱 Database Schema

Tables:
- User
- Subject
- Chapter
- Quizz
- Question
- Answer
- Scores
- Notify

Each table is designed with proper relationships using Flask-SQLAlchemy ORM.

---

## 🔗 API Design

- RESTful API built using Flask-RESTful
- JSON based request/response
- JWT protected routes
- Proper HTTP status codes (200, 400, 500)
- CORS enabled

---

## 🏗️ Architecture

- Frontend: Vue.js SPA
- Backend: Flask REST API
- Task Queue: Celery + Redis
- Database: SQLAlchemy ORM

---

## 📽️ Demo Video

Google Drive Demo:  
https://drive.google.com/file/d/1j4ucTxb0sWXj4zQ3Y2ocUeqFPNRgiK9U/view

---

## 🚀 How to Run

### Backend

```bash
pip install -r requirements.txt
python app.py
celery -A app.celery worker --loglevel=info
```

### Frontend

```bash
npm install
npm run serve
```

---

## ⭐ Acknowledgement

This project was developed as part of the App Development course under the IIT Madras BS Degree Program.

---

If you like this project, feel free to ⭐ the repository!


## Other details for running the servers

backend setting
cd backend
python3 -m venv venv
pip install -r requirements.txt

for mailhog
cd ..
 ~/go/bin/MailHog
 in linux to run the server

for redis
ps aux | grep 
sudo kill -9 950 or
redis-cli shutdown
start : redis-server

sudo systemctl stop redis
sudo lsof -i :6379


celery -A app beat --detach
celery -A app worker --detach
celery -A app worker --loglevel=info

celery -A app beat --loglevel=info
celery -A app.celery worker --loglevel=info
