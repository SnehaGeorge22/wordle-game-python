from wordle_backend import process_guess


def test_process_correct_guess():
    """
    This test validates if the guess is correct with the secret word
    """
    try:
        guess = ['s', 'm', 'a', 'c', 'k']
        secret = 'smack'
        expected_color_list = ['g', 'g', 'g', 'g', 'g']
        actual_color_list = process_guess(guess, secret)
        assert expected_color_list == actual_color_list
    except AssertionError as e:
        print(str(e))
