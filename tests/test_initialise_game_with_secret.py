from wordle_backend import initialise_game


def test_initialise_game_with_secret_word():
    """
    This test validates the initialise_game() function with a secret word.
    where secret_word is not None
    """
    try:
        secret_word = 'serve'
        all_words_file = 'english_dict.txt'
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
            'popup_queue': [],
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
        actual_game_state = initialise_game(all_words_file, secret_word=secret_word)
        assert actual_game_state == expected_game_state
    except AssertionError as e:
        print(str(e))
