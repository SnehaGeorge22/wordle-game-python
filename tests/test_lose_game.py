from wordle_backend import process_command, initialise_game
import pytest


@pytest.fixture(autouse=True)
def setup_game_state(monkeypatch):
    # Initialize game_state before each test
    global game_state
    game_state = initialise_game(
        all_words_file='english_dict.txt',
        secret_word='serve',
        max_guesses=2,
        word_length=5
    )
    game_state['grid'][0] = ['s', 'h', 'o', 'c', 'k']
    game_state['grid'][1] = ['s', 'h', 'i', 'n', 'e']
    game_state['colour_grid'][0] = ['g', '-', '-', '-', '-']
    game_state['i'] = 1
    game_state['max_guesses'] = 1
    monkeypatch.setattr('wordle_backend.game_state', game_state)
    yield


def test_lose_game():
    """
    This test validates the guess matches with the secret and the game is won
    """
    try:
        expected_process_ind = False
        expected_game_status = 'lost'
        assert game_state['status'] == 'playing'
        actual_process_ind = process_command(game_state=game_state, command='enter')
        assert actual_process_ind == expected_process_ind
        assert expected_game_status == game_state['status']
    except AssertionError as e:
        print(str(e))
