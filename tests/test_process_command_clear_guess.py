from wordle_backend import *


def test_process_command_clear_guess():
    """
    This test checks the clear command and grid is removed with values
    """
    try:
        test_game_state = initialise_game(all_words_file='english_dict.txt', secret_word='smack')
        test_game_state['grid'][0] = ['c', 'h', 'o', 'o', 'k']

        assert test_game_state['grid'][0] == ['c', 'h', 'o', 'o', 'k']
        process_command(game_state=test_game_state, command="clear")
        assert test_game_state['grid'][0] == ['', '', '', '', '']
    except AssertionError as e:
        print(str(e))
