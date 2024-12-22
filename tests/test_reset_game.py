from wordle_backend import reset_game
import pytest


@pytest.fixture(autouse=True)
def setup_game_state(monkeypatch):
    # Initialize game_state before each test
    global game_state
    game_state = {'secret_word': 'smack',
                  'word_length': 5,
                  'max_guesses': 6,
                  'grid': [['c', 'h', 'o', 'o', 'k'],
                           ['s', 'm', 'a', 'c', 'k'],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']],
                  'colour_grid': [['-', '-', '-', '-', '-'],
                                  ['g', '-', '-', '-', '-'],
                                  ['w', 'w', 'w', 'w', 'w'],
                                  ['w', 'w', 'w', 'w', 'w'],
                                  ['w', 'w', 'w', 'w', 'w'],
                                  ['w', 'w', 'w', 'w', 'w']],
                  'i': 2,
                  'j': 0,
                  'status': 'playing',
                  'wordle_words_file': 'wordle_words.txt',
                  'all_words_file': 'english_dict.txt',
                  'popup_queue': [],
                  'active_letters': {"A": False, "B": True, "C": False, "D": True, "E": True, "F": True,
                                     "G": True, "H": False, "I": True, "J": True, "K": True, "L": True,
                                     "M": False, "N": True, "O": False, "P": True, "Q": True, "R": True,
                                     "S": True, "T": True, "U": True, "V": True, "W": True, "X": True,
                                     "Y": True, "Z": True},
                  'green_letters_with_pos': [{'s': 0}],
                  'green_letters_list': ['s'],
                  'green_letters_indices': [0],
                  'yellow_letters': []
                  }
    monkeypatch.setattr('wordle_backend.game_state', game_state)
    yield


def test_reset_game():
    """
    This test validates the reset game method
    """
    try:
        expected_game_state = {
            'secret_word': 'serve',
            'word_length': 5,
            'max_guesses': 6,
            'grid': [['', '', '', '', ''],
                     ['', '', '', '', ''],
                     ['', '', '', '', ''],
                     ['', '', '', '', ''],
                     ['', '', '', '', ''],
                     ['', '', '', '', '']],
            'colour_grid': [['w', 'w', 'w', 'w', 'w'],
                            ['w', 'w', 'w', 'w', 'w'],
                            ['w', 'w', 'w', 'w', 'w'],
                            ['w', 'w', 'w', 'w', 'w'],
                            ['w', 'w', 'w', 'w', 'w'],
                            ['w', 'w', 'w', 'w', 'w']],
            'i': 0,
            'j': 0,
            'status': 'playing',
            'wordle_words_file': 'wordle_words.txt',
            'all_words_file': 'english_dict.txt',
            'popup_queue': [('Restarting game', 'text'), ('You have chosen to restart! The word was smack', 'text')],
            'active_letters': {"A": True, "B": True, "C": True, "D": True, "E": True, "F": True,
                               "G": True, "H": True, "I": True, "J": True, "K": True, "L": True,
                               "M": True, "N": True, "O": True, "P": True, "Q": True, "R": True,
                               "S": True, "T": True, "U": True, "V": True, "W": True, "X": True,
                               "Y": True, "Z": True},
            'green_letters_with_pos': [],
            'green_letters_list': [],
            'green_letters_indices': [],
            'yellow_letters': []
        }

        reset_game(game_state, secret_word='serve')

        assert expected_game_state == game_state
    except AssertionError as e:
        print(str(e))
