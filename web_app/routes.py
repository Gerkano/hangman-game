from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from web_app.hangman_utils import GameStateUpdate
from web_app.data_output import CurrenGameData, ArchiveGames
from web_app.models import User, ArchiveData
from web_app.forms import LoginForm, RegistrationForm, StartNewGame
from web_app import app, bcrypt, db
from random_word import RandomWords
from web_app.game_new_continue_end import StartContinueEnd, WinLost
from flask.logging import default_handler
import re

app.logger.removeHandler(default_handler)

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
                return redirect(url_for('hangman'))
    return render_template('login.html', form=form)

@app.route(f'/hangman', methods=["GET", "POST"])
@login_required
def hangman():
    random_word = RandomWords()
    word = random_word.get_random_word().upper()
    hangman = GameStateUpdate()
    game = CurrenGameData(current_user.id)
    hidden_word = hangman.hide_word(word)
    game_progress = StartContinueEnd(current_user.id, hidden_word, word)
    won_or_lost = WinLost(current_user.id)

    if game_progress.new_game_check() == True:
        game_progress.new_entrie()
    elif won_or_lost.won() == True:
        return redirect(url_for("menu"))
    elif won_or_lost.lost() == True:
        return redirect(url_for("menu"))
    else:
        hidden_word = game_progress.continue_game()
    if request.method == 'POST':
        pattern_upper_letter = r"[A-Z]"
        if re.search(pattern_upper_letter, request.form["letter"]):
            word = game_progress.all_turns[-1].word
            guess_letter = request.form["letter"]
            previous_hidden_word = game_progress.all_turns[-1].hidden_word
            game_checker = hangman.game_state(guess_letter, previous_hidden_word, word)
            hidden_word = game_checker["hidden_word"]

            game.add_collected_data(
                guess_letter, 
                game_checker["correct_guess"], 
                hidden_word, 
                word)
    return render_template('hangman.html', username=current_user.username.upper(), hangman=hidden_word)

@app.route('/fetch', methods=['GET', 'POST'])
@login_required
def fetch():
    game = CurrenGameData(current_user.id)
    used_letters = [i.guess for i in game.all_turns]
    wrong_guess_count = len([i.correct_guess for i in game.all_turns if i.correct_guess == "0"])
    guess_count_message = 9 - wrong_guess_count
    message = f"Mistakes allowed: {guess_count_message}"
    if guess_count_message < 0:
        message = "Game is lost"
    flash(message)
    last_guess = game.all_turns[-1].correct_guess
    return jsonify(used_letters[1:], wrong_guess_count, last_guess)


@app.route('/menu', methods=["GET", "POST"])
@login_required
def menu():
    form = StartNewGame()
    archive = ArchiveGames(current_user.id)
    won_or_lost = WinLost(current_user.id)
    try:
        archive.archive_data(f"{won_or_lost.won()}")
    except:
        return redirect(url_for("hangman"))
    all_games = ArchiveData.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        return redirect(url_for("hangman"))
    return render_template('menu.html', form=form, games=all_games)


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