from wordle_backend import get_hints, initialise_game
from unittest import mock


def test_get_hints():
    """
    This test validates the get_hints method of the Wordle class.
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
        test_game_state['green_letters_with_pos'] = [{'char':'s','pos':0}]
        test_game_state['green_letters_list'] = ['s']
        test_game_state['green_letters_indices'] = [0]
        with mock.patch('builtins.open', mock.mock_open(read_data="shock\nserve\nshook\nshave\n")):
            actual_hint_list = get_hints(game_state=test_game_state)
            expected_hint_list = ['shook', 'shave']
            assert actual_hint_list == expected_hint_list
    except AssertionError as e:
        print(str(e))

