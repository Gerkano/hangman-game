from typing import Optional
from random_word import RandomWords
from web_app.models import GameState, ArchiveData
from web_app import db

class GameApp:
    def __init__(self):
        pass

    def check_occurances(self, guess: str, word: str) -> int:
        guess_occurances = list(word).count(guess)
        return guess_occurances

    def hangman(self, guess: str, hidden_word: str, word: str) -> str:
        hidden_word = list(hidden_word)
        for i in range(0, len(word)):
            if word[i] == guess:
                hidden_word[i]=guess              
        return "".join(hidden_word)

    def letters_left(self, word: str) -> int:
        return len(word) - self.check_occurances()

    def check_guess(self, guess: str, word: str) -> bool:
        if guess in word:
            return True
        else:
            return False

    def game_object(self, guess: str, hidden_word: str, word: str) -> dict:
        word = word.upper()
        game_turn_data = {
            "guess":guess,
            "guessXV": self.check_guess(guess, word),
            "guess_occur": self.check_occurances(guess, word),
            "hidden_word": self.hangman(guess, hidden_word, word),
            "word": word
        }
        print(game_turn_data)
        return game_turn_data



class WordGenerator:
    def __init__(self) -> None:
        self.r = RandomWords()
        
    def generate_word(self) -> str:
        while True:
            word = self.r.get_random_word()
            if len(word) > 7:
                continue
            else:
                break
        return word

    def hide_word(self, word: str) -> str:
        word = list(word)
        for i in range(0, len(word)):
            word[i] = "_"
        return "".join(word)

class DataGenerator:

    @staticmethod
    def add_collected_data(guess_letter: str, correct_guess: int, hidden_word: str, word: str, user_id: int):
        game_state = GameState(
            guess=guess_letter, 
            correct_guess=correct_guess, 
            hidden_word=hidden_word, 
            word=word, 
            user_id=user_id
            )
        db.session.add(game_state)
        db.session.commit()
        
    @staticmethod
    def game_filter(user_id: int) -> bool:
        return GameState.query.filter_by(user_id=user_id).all()[-1]
    @staticmethod    
    def used_letter_check(user_id: int, guess_letter: str) -> bool:
        list_of_moves = GameState.query.filter_by(user_id=user_id).all()
        for i in range(0, len(list_of_moves)):
            print(list_of_moves[i].guess)
            if list_of_moves[i].guess == guess_letter:
                print("Letter already used")
                return True
            else:
                continue
        return False
    @staticmethod
    def game_lost_check(user_id: int) -> bool:
        list_of_games =  GameState.query.filter_by(user_id=user_id).all()
        print(list_of_games[0].correct_guess)
        counter = 0
        if len(list_of_games) > 1:
            for i in range(1, len(list_of_games)):
                if list_of_games[i].correct_guess == "0":
                    counter += 1
        if counter >= 10:
            return False
        else:
            return True
        

class ArchiveGames:
    def __init__(self) -> None:
        pass

    def archive_data(self, user_id: int, win_lose: bool):
        list_of_moves = GameState.query.filter_by(user_id=user_id).all()
        guess_list = []
        correct_guesses = 0
        incorrect_guesses = 0
        word = list_of_moves[1].word
        for i in range(1, len(list_of_moves)):
            guess_list.append(list_of_moves[i].guess)
            if list_of_moves[i].correct_guess == "1":
                correct_guesses += 1
            elif list_of_moves[i].correct_guess == "0":
                incorrect_guesses += 1
            else:
                continue
        archive = ArchiveData(
            guess_list=", ".join(guess_list), 
            win_lose=win_lose, 
            correct_guess_count=str(correct_guesses), 
            incorrect_guess_count=str(incorrect_guesses),
            word=word, 
            user_id=user_id
            )
        db.session.add(archive)
        db.session.commit()

    def clear_gamestate(self, user_id: int):
        list_of_moves = GameState.query.filter_by(user_id=user_id).all()
        for i in range(0, len(list_of_moves)):
            print(i)
            GameState.query.filter_by(user_id=user_id).delete()
            db.session.commit()