from random_word import RandomWords


class GameApp:

    def __init__(self, word):
        self.word = word.upper()
        self.word_length = len(word)

    def check_occurances(self, guess = ""):
        guess_occurances = list(self.word).count(guess)
        return guess_occurances

    def hangman(self, guess = "", word_hidden = ""):
        for i in range(0, len(self.word)):
            if self.word[i] != guess and len(word_hidden) == i:
                word_hidden=word_hidden + "_"
            elif self.word[i] == guess:
                word_hidden = list(word_hidden)
                word_hidden[i]=guess              
        return "".join(word_hidden)

    def letters_left(self):
        return self.word_length - self.check_occurances()

    def check_guess(self, guess):
        if guess in self.word and guess != "":
            return True
        elif guess == "":
            return None
        else:
            return False

    def game_object(self, guess = "", word_hidden = ""):
        game_turn_data = {
            "guess":guess,
            "guessXV": self.check_guess(guess),
            "guess_occur": self.check_occurances(guess),
            "hidden_word": self.hangman(guess, word_hidden)
        }
        return game_turn_data



# app = GameApp("sonkauliukai")
# print(app.game_object())
# # print(app.game_object("K", '____________'))
# print(app.game_object("S", "____________"))

