# #instance means  varible
# #route/endpoint/url
# #fetch/request/get same thing

# #flask,dlask_restful, redis, celery, flask_cors, flask_caching, flask_jwt_extended, flasl_sqlalchemy

# from flask import Flask,request
# app = Flask(__name__)

# @app.route('/api/', methods=['GET','POST'])#if methods not written default is GET
# def home():
#     return {"message": "This is a Route based api."},200
#     # return "<h1> hello world </h1>"

# class Home():
#     def get(self):
#         return {"message": "This is a Class based api."},200
    
#     def post(self):
#         return {"message": "This is a Class based post api."},200
#     # cannot creae another post or get
# house_api = Home()
# @app.route('/api/class')

# # class Auth():
# #     def post():
# #         #login
# # class Auth():
# #     def post():
# #         #signup
    
# def home_class():
#     if request.method == 'GET':
#         return house_api.get()
#     if request.method == 'POST':
#         return house_api.post()

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request
import os
from model import db,Users
from flask_restful import Api
from api import WelcomeAPI,LoginAPI, SignupAPI
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
db.init_app(app)
api = Api(app)
api.add_resource(WelcomeAPI, '/api/welcome')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(SignupAPI, '/api/signup')
app.app_context().push()

def add_admin():
    admin=Users.query.filter_by(role="admin").first()
    if not admin:
        admin = Users(name='Admin',email='Admin@gs.co',password='2030',role='admin')
        db.session.add(admin)
        db.session.commit()
        return 'admin added'
# preapare a record: prepare a object of that table
#add that object in the curren db session
# save the changes 
if __name__ == '__main__':
    db.create_all()
    add_admin()
    app.run(debug=True)
