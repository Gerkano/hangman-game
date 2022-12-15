from web_app.data_output import CurrenGameData
from web_app.models import GameState
import logging
import logging.config


logging.config.fileConfig('logging.conf',defaults={'logfilename': 'logs.log'})
logger = logging.getLogger('gameLogger')

class StartContinueEnd:
    def __init__(self, user: str, hidden: str, word: str) -> None:
        self.user = user
        self.data_add = CurrenGameData(self.user)
        self.word = word
        self.hidden = hidden
        self.all_turns: list = self.data_add.all_turns

    def new_game_check(self) -> bool:
        turns=len(self.all_turns)
        if turns==0:
            logger.info("New game")
        return True if turns==0 else False

    def new_entrie(self) -> None:
        self.data_add.add_collected_data(
            "None", 
            "None", 
            self.hidden, 
            self.word,
            )

    def continue_game(self) -> str:
        hidden_word = self.all_turns[-1].hidden_word
        logger.info("Unfinished game, continuing")
        return hidden_word
    

class WinLost():
    def __init__(self, user: str) -> None:
        self.user = user
        self.data_add = CurrenGameData(self.user)
        self.all_turns: list = self.data_add.all_turns

    def won(self) -> bool:
        if "_" not in self.all_turns[-1].hidden_word:
            logger.info("There was a win")
            return True
        else: 
            return False

    def lost(self) -> bool:
        lost_games =  GameState.query.filter_by(user_id=self.user).filter_by(correct_guess="0").all()
        check = True if len(lost_games) >= 10 else False
        logger.info(f"Game Lost: {check}")
        return check

    