from wordle_backend import process_command
import pytest
from unittest import mock


@pytest.fixture(autouse=True)
def setup_game_state(monkeypatch):
    # Initialize game_state before each test
    global game_state
    game_state = {'secret_word': 'smack',
                  'word_length': 5,
                  'max_guesses': 4,
                  'grid': [['c', 'h', 'o', 'o', 'k'],
                           ['s', 'm', 'a', 'c', 'k'],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']],
                  'colour_grid': [['-', '-', '-', '-', '-'],
                                  ['g', 'g', 'g', 'g', 'g'],
                                  ['w', 'w', 'w', 'w', 'w'],
                                  ['w', 'w', 'w', 'w', 'w'],
                                  ['w', 'w', 'w', 'w', 'w'],
                                  ['w', 'w', 'w', 'w', 'w']],
                  'i': 2,
                  'j': 0,
                  'status': 'won',
                  'wordle_words_file': 'wordle_words.txt',
                  'all_words_file': 'english_dict.txt',
                  'popup_queue': [],
                  'active_letters': {"A": False, "B": True, "C": False, "D": True, "E": True, "F": True,
                                     "G": True, "H": False, "I": True, "J": True, "K": True, "L": True,
                                     "M": False, "N": True, "O": False, "P": True, "Q": True, "R": True,
                                     "S": True, "T": True, "U": True, "V": True, "W": True, "X": True,
                                     "Y": True, "Z": True},
                  }
    monkeypatch.setattr('wordle_backend.game_state', game_state)
    yield


def test_process_command_history():
    """
    This test validates history command and checks whether it display the history
    """
    try:
        with mock.patch('builtins.open', mock.mock_open(read_data="0,1,0,4,0,6,3")):
            actual_process_ind = process_command(game_state=game_state, command='history')
            assert actual_process_ind == True
            assert game_state['popup_queue'][0][0] == [0, 1, 0, 4, 0, 6, 3]
            assert game_state['popup_queue'][0][1] == 'history'
    except AssertionError as e:
        print(str(e))
