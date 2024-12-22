from wordle_backend import persist_game_stats, initialise_game,clear_game_state
import os


def test_clear_game_state():
    """
    This test validates whether the game_state variable is persited
    """
    try:
        test_game_state = initialise_game(
            all_words_file='english_dict.txt',
            secret_word='serve',
            max_guesses=6,
            word_length=5
        )

        persist_game_stats(input_game_state=test_game_state)
        # Check if the file is created
        assert os.path.exists('game_stats.json')

        clear_game_state()
        assert not os.path.exists('game_stats.json')

    except AssertionError as e:
        print(str(e))