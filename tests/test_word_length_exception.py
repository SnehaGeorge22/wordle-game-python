from wordle_backend import initialise_game
import pytest


def test_incorrect_word_length_exception():
    """
    This test checks if the word length is incorrect and zero
    """
    try:
        all_words_file = 'english_dict.txt'
        wordle_words_file = 'wordle_words.txt'
        word_length = 0

        with pytest.raises(Exception, match="Word length must be 1 letter or more"):
            initialise_game(
                all_words_file,
                wordle_words_file=wordle_words_file,
                word_length=word_length
            )
    except AssertionError as e:
        print(str(e))
