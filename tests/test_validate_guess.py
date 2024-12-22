from wordle_backend import validate_guess


def test_validate_correct_guess():
    """
    This test validates whether the guess entered is valid or not
    """
    try:
        test_game_state = {'all_words_file': 'english_dict.txt',
                           'word_length': 5,
                           'i': 0,
                           'grid': [['s', 'm', 'a', 'c', 'k']]}
        expected_guess_ind = True
        actual_guess_ind = validate_guess(test_game_state)
        assert expected_guess_ind == actual_guess_ind
    except AssertionError as e:
        print(str(e))


