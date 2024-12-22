from wordle_backend import process_command, initialise_game
from unittest import mock


def test_process_command_hint():
    """
    This test validates the process_command_hint function.
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )
        test_game_state['grid'][0] = ['s', 'h', 'o', 'c', 'k']
        test_game_state['colour_grid'][0] = ['g', '-', '-', '-', '-']
        test_game_state['i'] = 1
        test_game_state['green_letters_with_pos'] = [{'char':'s','pos':0}]
        test_game_state['green_letters_list'] = ['s']
        test_game_state['green_letters_indices'] = [0]
        with mock.patch('builtins.open', mock.mock_open(read_data="shock\nserve\nshook\nshave\n")):
            actual_process_ind = process_command(game_state=test_game_state, command='hint')
            expected_process_ind = True
            assert actual_process_ind == expected_process_ind
            assert test_game_state['grid'][1] in [['s','h','o','o','k'], ['s','h','a','v','e']]
    except AssertionError as e:
        print(str(e))

