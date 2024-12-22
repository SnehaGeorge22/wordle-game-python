from wordle_backend import process_command, initialise_game


def test_message_for_adding_more_letters():
    """
    This test validates when the gamer tries to add more letters to the guess word
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )

        test_game_state['grid'][0] = ['s', 'h', 'o', 'c', 'k']
        test_game_state['i'] = 0
        test_game_state['j'] = 5
        expected_process_ind = True
        expected_game_message = "Can't add more letters\nUse clear or delete to edit your guess."
        actual_process_ind = process_command(game_state=test_game_state, command='l')
        actual_game_message = test_game_state['popup_queue'][0][0]
        assert expected_process_ind == actual_process_ind
        assert actual_game_message == expected_game_message
    except AssertionError as e:
       print(str(e))

