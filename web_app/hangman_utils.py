import logging
import logging.config

logging.config.fileConfig('logging.conf',defaults={'logfilename': 'logs.log'})
logger = logging.getLogger('gameLogger')

class GameStateUpdate:

    @staticmethod
    def hide_word(word: str) -> str:
        hidden_word = list(word)
        for i in range(0, len(word)):
            hidden_word[i] = "_"
        return "".join(hidden_word)

    @staticmethod
    def show_letter(guess: str, hidden_word: str, word: str) -> str:
        hidden_word_list = list(hidden_word)
        for i in range(0, len(word)):
            if word[i] == guess:
                hidden_word_list[i]=guess              
        return "".join(hidden_word_list)

    @staticmethod
    def check_guess(guess: str, word: str) -> bool:
        check = True if guess in word else False
        logger.debug(f"Your guess is {check}")
        return check

    @staticmethod
    def game_state(guess: str, hidden_word: str, word: str) -> dict:
        word = word.upper()
        game_turn_data = {
            "guess":guess,
            "correct_guess": GameStateUpdate.check_guess(guess, word),
            "hidden_word": GameStateUpdate.show_letter(guess, hidden_word, word),
            "word": word
        }
        logger.debug(f"Game state sent: {game_turn_data}")
        return game_turn_data
