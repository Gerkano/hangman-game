from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
app.config['SECRET_KEY'] = '5sfJAid482fdKhdfs'
db = SQLAlchemy(app)
hangman_image = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = hangman_image

from web_app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from web_app import routes

