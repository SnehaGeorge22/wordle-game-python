from wordle_backend import update_game_history, initialize_game_history, update_guess_limit_in_hist
import pytest


@pytest.fixture(autouse=True)
def setup_game_state(monkeypatch):
    # Initialize game_state before each test
    global game_state, game_history
    game_state = {
        'status': 'lost',
        'max_guesses': 8
    }
    game_history = [{'game_hist_length': 6,
                    'game_hist_list': [0, 0, 0, 0, 0, 0, 0],
                    'old_game_hist_list': []
                    }]
    monkeypatch.setattr('wordle_backend.game_state', game_state)
    monkeypatch.setattr('wordle_backend.game_history', game_history)
    yield


def test_update_guess_limit_in_game_history():
    """
    This test validates the fucntion update_guess_limit_in_hist when max_guesses is changed.
    """
    try:
        initialize_game_history(max_guesses=6)
        with open('game_history.txt', 'r') as file:
            before_update_guess_limit = file.read()
            expected_content = "0,0,0,0,0,0,0"
            assert before_update_guess_limit == expected_content
        update_guess_limit_in_hist()
        with open('game_history.txt', 'r') as file:
            after_update_guess_limit = file.read()
            expected_content = "0,0,0,0,0,0,0,0,0"
            assert after_update_guess_limit == expected_content
    except AssertionError as e:
        print(str(e))
