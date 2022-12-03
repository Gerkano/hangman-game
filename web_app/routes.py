from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from web_app.hangman import GameApp, WordGenerator, DataGenerator, ArchiveGames
from web_app.models import User, GameState
from web_app.forms import LoginForm, RegistrationForm, GameStart, StartNewGame
from web_app import app, bcrypt, db, hangman_image
import time
import os

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

@app.route(f'/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    form = GameStart()
    word_class = WordGenerator()
    word = word_class.generate_word().upper()
    hangman = GameApp()
    data_colector = DataGenerator()
    hidden_word = word_class.hide_word(word)
    if len(GameState.query.filter_by(user_id=current_user.id).all())==0:
        data_colector.add_collected_data(
            "None", 
            "None", 
            hidden_word, 
            word, 
            current_user.id)
    elif "_" not in data_colector.game_filter(current_user.id).hidden_word:
        flash(f'You win, much praise!')
        # time.sleep(1)
        return redirect(url_for("menu"))
    elif data_colector.game_lost_check(current_user.id) == False:
        flash(f'You dieded ;/')
        return redirect(url_for("menu"))
    else:
        hidden_word = data_colector.game_filter(current_user.id).hidden_word
        print(hidden_word)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if request.method == 'POST':
        for i in alphabet:
            if request.form["letter"] == i:
                word = data_colector.game_filter(current_user.id).word
                guess_letter = i
                if data_colector.used_letter_check(current_user.id, guess_letter):
                    flash(f' {guess_letter}  already ussed')
                    continue
                previous_hidden_word = data_colector.game_filter(current_user.id).hidden_word
                print(previous_hidden_word)
                game_checker = hangman.game_object(guess_letter, previous_hidden_word, word)
                hidden_word = game_checker["hidden_word"]
                data_colector.add_collected_data(
                    guess_letter, 
                    game_checker["guessXV"], 
                    hidden_word, 
                    word, 
                    current_user.id)

                # return render_template('dashboard.html', username=current_user.username.upper(), hangman=hidden_word)
    return render_template('dashboard.html', username=current_user.username.upper(), hangman=hidden_word) #, image=pic , form=form

@app.route('/fetch', methods=['GET', 'POST'])
@login_required
def fetch():
    used_letters = [i.guess for i in GameState.query.filter_by(user_id=current_user.id).all()]
    wrong_guess_count = len([i.correct_guess for i in GameState.query.filter_by(user_id=current_user.id).all() if i.correct_guess == "0"])
    last_guess = GameState.query.filter_by(user_id=current_user.id).all()[-1].correct_guess
    print(wrong_guess_count)
    return jsonify(used_letters[1:], wrong_guess_count, last_guess)

@app.route('/menu', methods=["GET", "POST"])
@login_required
def menu():
    form = StartNewGame()
    archive = ArchiveGames()
    data_colector = DataGenerator()
    if form.validate_on_submit():
        flash(f'New game started')
        try:
            archive.archive_data(current_user.id, f"{data_colector.game_lost_check(current_user.id)}")
            archive.clear_gamestate(current_user.id)
        except:
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("dashboard"))
    return render_template('menu.html', form=form)

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