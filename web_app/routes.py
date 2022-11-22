from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from web_app.hangman import GameApp
from web_app.models import User
from web_app.forms import LoginForm, RegistrationForm
from web_app import app, bcrypt, db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    hangman = GameApp("makaka")
    return render_template('dashboard.html', username=current_user.username, hangman=hangman.game_object()["hidden_word"])

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account successfully created: {form.username.data}!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)