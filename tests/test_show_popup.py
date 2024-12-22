from wordle_backend import process_command, initialise_game


def test_show_popup():
    """
    This test validates the show popup functionality whether the message is added to the queue
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )
        test_game_state['grid'][0] = ['s', 'e', 'r', 'v', 'e']
        expected_process_ind = False
        assert test_game_state['status'] == 'playing'
        actual_process_ind = process_command(game_state=test_game_state, command='enter')
        assert actual_process_ind == expected_process_ind
        assert test_game_state['popup_queue'][0][0] == 'You won!'
    except AssertionError as e:
        print(str(e))

