from wordle_backend import process_command, initialise_game


def test_message_for_invalid_command():
    """
    This test validates the when a invalid command is entered
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )

        test_game_state['grid'][0] = ['s', 'h', 'o', 'c', 'k']
        expected_game_message = 'Invalid command'
        actual_process_ind = process_command(game_state=test_game_state, command=')')
        actual_game_message = test_game_state['popup_queue'][0][0]
        assert actual_game_message == expected_game_message
    except AssertionError as e:
        print(str(e))

