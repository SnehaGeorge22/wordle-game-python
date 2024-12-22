from wordle_backend import process_command, initialise_game


def test_message_for_game_won():
    """
    This test validates the popup message when the game is won
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
        expected_game_message = 'You won!'
        actual_process_ind = process_command(game_state=test_game_state, command='enter')
        actual_game_message = test_game_state['popup_queue'][0][0]
        assert actual_process_ind == expected_process_ind
        assert actual_game_message == expected_game_message
    except AssertionError as e:
        print(str(e))

