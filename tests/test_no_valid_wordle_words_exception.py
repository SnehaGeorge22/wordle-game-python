from wordle_backend import initialise_game
import pytest


def test_no_valid_wordle_words_exception():
    """
    This test checks whether Exception is raised when there are no valid wordle words.
    Exception: "No valid words in wordle words file"
    """
    all_words_file = 'english_dict.txt'
    wordle_words_file = 'wordle_words.txt'

    with pytest.raises(Exception, match="No valid words in wordle words file"):
        initialise_game(all_words_file, wordle_words_file=wordle_words_file, word_length=8)
