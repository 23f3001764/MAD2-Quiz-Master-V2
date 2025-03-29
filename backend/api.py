from flask import Flask,request,redirect
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_caching import Cache
from datetime import datetime
from model import db, User, Subject, Chapter, Quizz, Question, Answer, Scores, Notify

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