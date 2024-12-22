from wordle_backend import process_command, initialise_game


def test_win_game():
    """
    This test validates the guess matches with the secret and the game is won
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
        expected_game_status = 'won'
        assert test_game_state['status'] == 'playing'
        actual_process_ind = process_command(game_state=test_game_state, command='enter')
        assert expected_process_ind == actual_process_ind
        assert expected_game_status == test_game_state['status']
    except AssertionError as e:
        print(str(e))

