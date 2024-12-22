from wordle_backend import initialise_game
import pytest


def test_max_guesses_exception():
    """
    This test check when the value for max_guesses variable is passed as 0 and whether
    an Exception is triggered or not.
    """
    try:
        all_words_file = 'english_dict.txt'
        wordle_words_file = 'wordle_words.txt'
        max_guess = 0

        with pytest.raises(Exception, match="Max guesses must be 1 or more"):
            initialise_game(all_words_file, wordle_words_file=wordle_words_file, max_guesses=max_guess)
    except AssertionError as e:
        print(str(e))
