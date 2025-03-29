from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from model import db,User
import os
from datetime import timedelta
from api import LoginAPI, SignupAPI, cache

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

if __name__=="__main__":
    db.create_all()
    add_admin()
    app.run(debug=True)