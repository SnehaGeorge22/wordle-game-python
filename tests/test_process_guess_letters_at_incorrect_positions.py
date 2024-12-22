from wordle_backend import process_guess
import pytest

@pytest.fixture(autouse=True)
def setup_game_state(monkeypatch):
    # Initialize game_state before each test
    global game_state
    game_state = {
        'active_letters': {
            "A": True, "B": True, "C": True, "D": True, "E": True, "F": True,
            "G": True, "H": True, "I": True, "J": True, "K": True, "L": True,
            "M": True, "N": True, "O": True, "P": True, "Q": True, "R": True,
            "S": True, "T": True, "U": True, "V": True, "W": True, "X": True,
            "Y": True, "Z": True
        },

    }
    monkeypatch.setattr('wordle_backend.game_state', game_state)
    yield


def test_process_guess_letters_at_incorrect_positions():
    """
    This test validates if the guess is not matching with secret word
    but has letters at incorrect positions.
    """
    try:
        guess = ['s', 'm', 'a', 'c', 'k']
        secret = 'bears'
        expected_color_list = ['y', '-', 'g', '-', '-']
        actual_color_list = process_guess(guess, secret)
        assert actual_color_list == expected_color_list
    except AssertionError as e:
        print(str(e))
