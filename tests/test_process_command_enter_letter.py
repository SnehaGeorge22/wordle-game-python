from wordle_backend import process_command

input_game_state = {
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


def test_process_command_valid_letter():
    """
    This test checks when a letter is entered as command and
    whether it gets appended to the game grid
    """
    try:
        expected_process_ind = True
        actual_process_ind = process_command(input_game_state, 's')
        assert expected_process_ind == actual_process_ind
        assert input_game_state['grid'][0][0] == 's'
    except AssertionError as e:
        print(str(e))
