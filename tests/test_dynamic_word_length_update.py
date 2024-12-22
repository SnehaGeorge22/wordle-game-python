from wordle_backend import initialise_game
from unittest import mock


def test_dynamic_word_length_update():
    """
    This test validates the word length variable.
    if this is updated, does the game_state grid updates to accommodate the change
    other than default value - 5.
    """
    mock_all_words = 'english_dict.txt'
    mock_wordle_words = 'wordle_words.txt'
    custom_max_guesses = 6
    custom_word_length = 7

    with mock.patch('builtins.open', mock.mock_open(read_data="command\nbackend\nprocess")):
        game_state = initialise_game(mock_all_words,
                                     mock_wordle_words,
                                     max_guesses=custom_max_guesses,
                                     word_length=custom_word_length)

    # Assert the game state has the expected values
    assert game_state['word_length'] == custom_word_length
    assert len(game_state['grid'][0]) == custom_word_length
