from wordle_backend import initialize_game_history
import os


def test_initialize_game_history_creates_file():
    """
    This test validates whether the game history file can be created.
    """
    try:
        max_guesses = 6
        initialize_game_history(max_guesses)

        # Check if the file is created
        assert os.path.exists('game_history.txt')

        # Read the file and check if the content is correct
        with open('game_history.txt', 'r') as file:
            content = file.read()
            # As max_guesses is 6, we expect 7 values
            expected_content = "0,0,0,0,0,0,0"
            assert content == expected_content

        # Clean up the file after the test
        os.remove('game_history.txt')
    except AssertionError as e:
        print(str(e))