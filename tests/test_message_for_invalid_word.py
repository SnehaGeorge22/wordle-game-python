from wordle_backend import validate_guess


def test_message_for_invalid_word():
    """
    This test validates the invalid error message
    """
    try:
        test_game_state = {'all_words_file': 'english_dict.txt',
                           'word_length': 5,
                           'i': 0,
                           'grid': [['t', 'm', 'a', 'c', 'k']],
                           'popup_queue':[]}
        expected_guess_ind = False
        expected_game_message = "Invalid word\nUse clear or delete to edit your guess"
        actual_guess_ind = validate_guess(test_game_state)
        assert actual_guess_ind == expected_guess_ind
        assert expected_game_message == test_game_state['popup_queue'][0][0]
    except AssertionError as e:
        print(str(e))


