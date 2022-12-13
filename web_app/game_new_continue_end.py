from web_app.data_output import DataGenerator
import logging
import logging.config

logging.config.fileConfig('logging.conf',defaults={'logfilename': 'logs.log'})
logger = logging.getLogger('gameLogger')

class StartContinueEnd:
    def __init__(self, user: str, hidden: str, word: str) -> None:
        self.user = user
        self.data_colector = DataGenerator(self.user)
        self.word = word
        self.hidden = hidden

    def new_entrie(self) -> None:
        self.data_colector.add_collected_data(
            "None", 
            "None", 
            self.hidden, 
            self.word,
            )

    def hidden_word(self) -> str:
        hidden_word = self.data_colector.all_turns[-1].hidden_word
        logger.info("Unfinished game, continuing")
        return hidden_word

    def won(self) -> bool:
        if "_" not in self.data_colector.all_turns[-1].hidden_word:
            logger.info("There was a win")
            return True
        else: 
            return False

    def lost(self) -> bool:
        if self.data_colector.game_lost_check() == True:
            logger.info("The game was lost")
            return True
        else:
            return False