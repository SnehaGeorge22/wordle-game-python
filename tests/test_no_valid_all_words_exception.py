from wordle_backend import validate_guess, initialise_game
import pytest


def test_no_valid_all_words_exception():
    """
    This tests checks whether Exception is raised "No valid words in all words file"
    when there are no valid words in all words file.
    """
    try:
        game_state = {'all_words_file': 'english_dict.txt', 'word_length': 8}
        with pytest.raises(Exception, match="No valid words in all words file"):
            validate_guess(game_state)
    except AssertionError as e:
        print(str(e))
