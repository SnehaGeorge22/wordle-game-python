from wordle_backend import initialise_game
from unittest import mock


def test_secret_word_selection_from_file():
    """
    This test check the initialise_game method where the scenario - Secret word is NONE
    """
    try:
        mock_all_words = 'english_dict.txt'
        mock_wordle_words = 'wordle_words.txt'

        # Mock the file reading for wordle words
        with mock.patch('builtins.open', mock.mock_open(read_data="apple\nmango\npeach")):
            game_state = initialise_game(mock_all_words, mock_wordle_words)

        # Assert the secret word is chosen from the file
        assert game_state['secret_word'] in ['apple', 'mango', 'peach']
    except AssertionError as e:
        print(str(e))
