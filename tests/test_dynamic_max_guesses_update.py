from wordle_backend import initialise_game


def test_dynamic_max_guesses_update():
    """
    This test validates the max_guesses variable.
    if this is updated, does the game_state grid updates to accommodate the change
    other than default value - 6.
    """
    mock_all_words = 'english_dict.txt'
    mock_wordle_words = 'wordle_words.txt'
    custom_max_guesses = 7
    custom_word_length = 5

    game_state = initialise_game(
            mock_all_words,
            mock_wordle_words,
            max_guesses=custom_max_guesses,
            word_length=custom_word_length
        )

    assert game_state['max_guesses'] == custom_max_guesses
    assert len(game_state['grid']) == custom_max_guesses
