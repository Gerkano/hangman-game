from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from web_app.hangman_utils import GameStateUpdate
from web_app.data_output import DataGenerator, ArchiveGames
from web_app.models import User, GameState, ArchiveData
from web_app.forms import LoginForm, RegistrationForm, StartNewGame
from web_app import app, bcrypt, db
from random_word import RandomWords
from web_app.game_new_continue_end import StartContinueEnd
from flask.logging import default_handler

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
    data_colector = DataGenerator(current_user.id)
    hidden_word = hangman.hide_word(word)
    game_progress = StartContinueEnd(current_user.id, hidden_word, word)

    if data_colector.new_game_check() == True:
        game_progress.new_entrie()
    elif game_progress.won() == True:
        return redirect(url_for("menu"))
    elif game_progress.lost() == True:
        return redirect(url_for("menu"))
    else:
        hidden_word = game_progress.hidden_word()

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if request.method == 'POST':
        for i in alphabet:
            if request.form["letter"] == i:
                word = data_colector.all_turns[-1].word
                guess_letter = i
                if data_colector.used_letter_check(guess_letter):
                    flash(f' {guess_letter}  already ussed')
                    continue
                previous_hidden_word = data_colector.all_turns[-1].hidden_word
                print(previous_hidden_word)
                game_checker = hangman.game_state(guess_letter, previous_hidden_word, word)
                hidden_word = game_checker["hidden_word"]

                data_colector.add_collected_data(
                    guess_letter, 
                    game_checker["correct_guess"], 
                    hidden_word, 
                    word)
    return render_template('hangman.html', username=current_user.username.upper(), hangman=hidden_word)

@app.route('/fetch', methods=['GET', 'POST'])
@login_required
def fetch():
    data_colector = DataGenerator(current_user.id)
    used_letters = [i.guess for i in data_colector.all_turns]
    wrong_guess_count = len([i.correct_guess for i in data_colector.all_turns if i.correct_guess == "0"])
    guess_count_message = 9 - wrong_guess_count
    message = f"Mistakes allowed: {guess_count_message}"
    if guess_count_message < 0:
        message = "Game is lost"
    flash(message)
    last_guess = data_colector.all_turns[-1].correct_guess
    return jsonify(used_letters[1:], wrong_guess_count, last_guess)


@app.route('/menu', methods=["GET", "POST"])
@login_required
def menu():
    form = StartNewGame()
    archive = ArchiveGames(current_user.id)
    data_colector = DataGenerator(current_user.id)
    all_games = ArchiveData.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        try:
            archive.archive_data(f"{data_colector.game_lost_check()}")
            archive.clear_gamestate()
        except:
            return redirect(url_for("hangman"))
        else:
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