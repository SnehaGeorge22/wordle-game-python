from wordle_backend import initialise_game
import pytest


def test_secret_word_incorrect_length_exception():
    """
    This test checks the secret word if the length of the secret word is incorrect.
    """
    try:
        all_words_file = 'english_dict.txt'
        wordle_words_file = 'wordle_words.txt'
        word_length = 6
        secret = 'smack'

        with pytest.raises(Exception, match="The secret word is not of the correct length"):
            initialise_game(all_words_file,
                            wordle_words_file=wordle_words_file,
                            secret_word=secret,
                            word_length=word_length)
    except AssertionError as e:
        print(str(e))
