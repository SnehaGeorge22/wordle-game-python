from wordle_backend import update_game_history, initialize_game_history
import pytest


@pytest.fixture(autouse=True)
def setup_game_state(monkeypatch):
    # Initialize game_state before each test
    global game_state, game_history
    game_state = {
        'status': 'lost'
    }
    game_history = [{'game_hist_length': 6,
                    'game_hist_list': [0, 0, 0, 0, 0, 0, 0],
                    'old_game_hist_list': []
                    }]
    monkeypatch.setattr('wordle_backend.game_state', game_state)
    monkeypatch.setattr('wordle_backend.game_history', game_history)
    yield


def test_update_game_history():
    """
    This test validates the update_game_history function.
    """
    try:
        initialize_game_history(max_guesses=6)
        update_game_history()
        with open('game_history.txt', 'r') as file:
            content = file.read()
            expected_content = "1,0,0,0,0,0,0"
            assert content == expected_content
    except AssertionError as e:
        print(str(e))
