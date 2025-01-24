from flask import Flask
app = Flask(__name__)
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
import model

if __name__=="__main__":
    app.run(debug=True)