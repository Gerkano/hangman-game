from typing import Tuple
from web_app.models import GameState, ArchiveData
from web_app import db
import logging
import logging.config

logging.config.fileConfig('logging.conf',defaults={'logfilename': 'logs.log'})
logger = logging.getLogger('gameLogger')


class CurrenGameData:
    def __init__(self, user: str) -> None:
        self.user = user
        self.all_turns: list = GameState.query.filter_by(user_id=self.user).all()

    def add_collected_data(self, guess_letter: str, correct_guess: str, hidden_word: str, word: str) -> None:
        game_state = GameState(
            guess=guess_letter, 
            correct_guess=correct_guess, 
            hidden_word=hidden_word, 
            word=word, 
            user_id=self.user
            )
        db.session.add(game_state)
        db.session.commit()

class ArchiveGames:

    def __init__(self, user: str) -> None:
        self.user = user
        self.list_of_moves: list = GameState.query.filter_by(user_id=self.user).all()

    def correct_and_incorrect_count(self) -> Tuple[list, int, int]:
        guess_list = []
        correct_guesses = 0
        incorrect_guesses = 0
        
        for item in range(1, len(self.list_of_moves)):
            guess_list.append(self.list_of_moves[item].guess)
            if self.list_of_moves[item].correct_guess == "1":
                correct_guesses += 1
            elif self.list_of_moves[item].correct_guess == "0":
                incorrect_guesses += 1
            else:
                continue
        return guess_list, correct_guesses, incorrect_guesses

    def archive_data(self, win: bool) -> None:

        word = self.list_of_moves[1].word

        archive = ArchiveData(
            guess_list=", ".join(self.correct_and_incorrect_count()[0]), 
            win=win, 
            correct_guess_count=str(self.correct_and_incorrect_count()[1]), 
            incorrect_guess_count=str(self.correct_and_incorrect_count()[2]),
            word=word, 
            user_id=self.user
            )
        db.session.add(archive)
        db.session.commit()
        self.clear_gamestate()
        
    def clear_gamestate(self) -> None:
        for _ in range(0, len(self.list_of_moves)):
            GameState.query.filter_by(user_id=self.user).delete()
            db.session.commit()