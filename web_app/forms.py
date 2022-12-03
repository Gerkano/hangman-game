from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from web_app.models import User


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Password"})
    
    confirm_password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40), EqualTo('password', "Passwords do not match")], 
    render_kw={"placeholder": "Confirm password"})

    email = StringField(validators=[InputRequired(), Length(
        min=5, max=40), Email()], render_kw={"placeholder": "Email"})

    submit = SubmitField("Register")
    
    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            flash(f'Username already exists: {username.data}')
            raise ValidationError(
                "That username already exists. Please chose a different one.")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            flash(f'Email already exists: {email.data}')
            raise ValidationError(
                "That email already exists. Please chose a different one.")

class GameStart(FlaskForm):
    guess_word = StringField(validators=[InputRequired(), Length(
        min=1, max=8)], render_kw={"placeholder": "Guess the word"})
    submit = SubmitField("Guess")

class StartNewGame(FlaskForm):
    submit = SubmitField("Start new game")