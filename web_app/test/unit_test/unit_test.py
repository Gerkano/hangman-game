from web_app.hangman_utils import GameStateUpdate
import unittest


class TestScoreCalc(unittest.TestCase):


    def test_check_guess(self):
        result1 = GameStateUpdate.check_guess("W", "WALK")
        result2 = GameStateUpdate.check_guess("X", "LEMON")
        self.assertEqual(result1, True)
        self.assertEqual(result2, False)

    def test_show_letter(self):
        result1 = GameStateUpdate.show_letter("W", "______", "WALKER")
        result2 = GameStateUpdate.show_letter("X", "______", "WALKER")
        self.assertEqual(result1, "W_____")
        self.assertEqual(result2, "______")

    def test_hide_word(self):
        result1 = GameStateUpdate.hide_word("WALKER")
        result2 = GameStateUpdate.hide_word("VACUUM")
        self.assertEqual(result1, "______")
        self.assertEqual(result2, "______")
