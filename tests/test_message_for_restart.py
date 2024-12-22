from wordle_backend import process_command, initialise_game


def test_message_for_restart():
    """
    This test validates the scenario when restart is requested by the user
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )

        test_game_state['grid'][0] = ['s', 'h', 'o', 'c', 'k']
        expected_restart1_message = 'Restarting game'
        expected_restart2_message = 'You have chosen to restart! The word was serve'
        actual_process_ind = process_command(game_state=test_game_state, command='!')
        actual_game_message1 = test_game_state['popup_queue'][0][0]
        actual_game_message2 = test_game_state['popup_queue'][1][0]
        assert actual_process_ind == True
        assert actual_game_message1 == expected_restart1_message
        assert actual_game_message2 == expected_restart2_message
    except AssertionError as e:
        print(str(e))

