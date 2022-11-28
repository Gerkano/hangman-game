from web_app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    game_id = db.relationship('GameState', backref='user')

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String(40), nullable=False)
    true_or_false = db.Column(db.String(40), nullable=False)
    hidden_word = db.Column(db.String(40), nullable=False)
    word = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ArchiveData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guess_list = db.Column(db.String(20), nullable=False)
    win_lose = db.Column(db.String(20), nullable=False)
    correct_guess_count = db.Column(db.String(20), nullable=False)
    incorrect_guess_count = db.Column(db.String(20), nullable=False)
    word = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))