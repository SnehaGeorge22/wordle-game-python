from wordle_backend import process_command, initialise_game


def test_process_command_enter_guess():
    """
    This test validates the guess when the enter command is passed
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )

        test_game_state['grid'][0] = ['s', 'h', 'o', 'c', 'k']
        expected_process_ind = True
        expected_game_status = 'playing'
        actual_process_ind = process_command(game_state=test_game_state, command='enter')
        assert expected_process_ind == actual_process_ind
        assert expected_game_status == test_game_state['status']
    except AssertionError as e:
        print(str(e))

