from typing import Tuple
from web_app.models import GameState, ArchiveData
from web_app import db
import logging
import logging.config

logging.config.fileConfig('logging.conf',defaults={'logfilename': 'logs.log'})
logger = logging.getLogger('gameLogger')


class DataGenerator:
    def __init__(self, user: str) -> None:
        self.user = user
        self.all_turns: list = GameState.query.filter_by(user_id=self.user).all()

    def new_game_check(self) -> bool:
        turns=len(self.all_turns)
        if turns==0:
            logger.info("New game")
        return True if turns==0 else False

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

    def used_letter_check(self, guess_letter: str) -> bool:
        for item in range(0, len(self.all_turns)):
            if self.all_turns[item].guess == guess_letter:
                return True
            else:
                continue
        return False

    def game_lost_check(self) -> bool:
        list_of_games =  GameState.query.filter_by(user_id=self.user).filter_by(correct_guess="0").all()
        check = True if len(list_of_games) >= 10 else False
        return check
        

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

    def clear_gamestate(self) -> None:
        for _ in range(0, len(self.list_of_moves)):
            GameState.query.filter_by(user_id=self.user).delete()
            db.session.commit()