from wordle_frontend import *
from wordle_backend import *

if __name__ == "__main__":
    game_state = initialise_game(all_words_file="english_dict.txt",
                                 wordle_words_file="wordle_words.txt",
                                 secret_word=None,
                                 max_guesses=6,
                                 word_length=5)

    run_game_terminal(game_state)
