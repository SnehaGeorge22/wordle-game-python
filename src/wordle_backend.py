#############################################################################################
# Author : Sneha George
# Python Project: Wordle Game
#############################################################################################
import os
import random
import json
import regex as re
import logging
import time

logging.basicConfig(filename='game_log_v1.log',
                    filemode='w',
                    format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S %p', level=logging.DEBUG)
__logger__ = logging.getLogger('game_logger')

current_dir = os.path.dirname(os.path.realpath(__file__))

game_state = {}
game_history = []


def initialize_game_history(max_guesses: int) -> None:
    """
    This method initialize the game history list and writes it to a text file in current directory 
    at the initial stage of the game.

    Arguments:
    ----------
    max_guesses : int
    A integer value stating the max_guesses to be used in the game with the default being 6

    Returns : 
    ---------
    None 
    """
    try:
        # Include one position in the history list for games lost, hence adding by 1
        __logger__.debug(f"Initializing the game history..")
        game_hist_len = int(max_guesses) + 1

        # creating a list with values as 0 as per the above length
        game_hist_list = [0] * game_hist_len

        # Writing the details to a history text file in current directory
        with open('game_history.txt', 'w') as f:
            f.write(",".join(map(str, game_hist_list)))

        # Appending the values to the game history list
        global game_history
        game_history.append({
            'game_hist_length': game_hist_len,
            'game_hist_list': game_hist_list,
            'old_game_hist_list': []})
        __logger__.debug(f"Initial Game History : \n {game_history}")
    except Exception as e:
        __logger__.exception(str(e))


def update_game_history() -> None:
    """
    This method updates the game history list and text file accordingly 
    when the status of the wordle game is changed to 'won' or 'lost'

    Arguments:
    ----------
    None

    Returns : 
    ---------
    None 
    """
    try:

        __logger__.debug(f"Updating the game history..")
        global game_history, game_state
        # Getting the status of the game from game_state dictionary
        game_status = game_state['status']

        # Getting the size of game history list
        game_hist_len = len(game_history)

        # Making a copy of the value which contains the details of games lost /won for each guesses
        game_history_list = game_history[game_hist_len - 1]['game_hist_list'].copy()

        # Updating the counts for status - lost/won
        if game_status == 'lost':
            game_history_list[0] += 1
        elif game_status == 'won':
            guess_count = int(game_state['i']) + 1
            game_history_list[guess_count] += 1

        # Assigning the updated counts to the game history list
        game_history[game_hist_len - 1]['game_hist_list'] = game_history_list

        # Writing the updated counts to the game history text file
        with open('game_history.txt', 'w') as f:
            f.write(",".join(map(str, game_history_list)))
        __logger__.debug(f"Updated Game History : \n {game_history}")
    except Exception as e:
        __logger__.exception(str(e))


def update_guess_limit_in_hist() -> None:
    """
    This method updates the game history list with new positions if the max_guess is changed for a game

    Arguments:
    ----------
    None

    Returns : 
    ---------
    None 
    
    """
    try:
        __logger__.debug(f"Checking whether the guess limit has been changed..")
        global game_history, game_state

        # Getting the maximum guess limit from game_state dictionary
        max_guess_limit = game_state['max_guesses']

        # Getting the size of game history list
        game_hist_len = len(game_history)

        # Fetching the current limit of max guesses 
        max_guess_hist = game_history[game_hist_len - 1]['game_hist_length']

        # Making a copy of the value which contains the details of games lost /won for each guesses
        game_history_list = game_history[game_hist_len - 1]['game_hist_list'].copy()

        # checking whether current and new guess limit are equal and
        # new guess limit shouldn't be less than current guess limit
        if (max_guess_hist - 1 != max_guess_limit) and (max_guess_limit >= max_guess_hist - 1):
            # Creating a variable with new guess limit
            new_guess_hist_limit = int(max_guess_limit) + 1

            # Creating a variable with new list size
            new_list_size = new_guess_hist_limit - max_guess_hist

            # Creating a new list with above new size
            extendable_list = [0] * new_list_size

            # Copying the current history list to a new variable to avoid overriding
            old_game_hist_list = game_history_list.copy()

            # Extending the current list
            game_history_list.extend(extendable_list)

            # Appending the new values to the game history
            game_history.append({
                'game_hist_length': new_guess_hist_limit,
                'game_hist_list': game_history_list,
                'old_game_hist_list': old_game_hist_list
            })

            # Writing the updated counts to the game history text file
            with open('game_history.txt', 'w') as f:
                f.write(",".join(map(str, game_history_list)))
            __logger__.debug(f"Updated Game History : \n {game_history}")
    except Exception as e:
        __logger__.exception(str(e))


def show_popup(game_state, content, mode="text") -> None:
    """ 
    This method adds a "pop-up" message to the queue for the front end to display.

    Arguments:
    ----------
    game_state: dict
    A dictionary containing the current state of the game with all the details

    content: str or list based on mode type
    A variable storing the message to be displayed to the frontend

    mode: str
    A type of content to be displayed to the frontend

    Returns:
    --------
    None

    """
    try:
        # Checking the mode type
        __logger__.debug(f"Adding the message to the popup queue..")
        game_state['popup_queue'].append((content, mode))
        __logger__.debug(f"Show Popup Queue : \n {game_state['popup_queue']}")
        return
    except Exception as e:
        __logger__.exception(str(e))


def persist_game_stats(input_game_state: dict) -> None:
    """ 
    This method persists the current state of the game as a json file in the current directory

    Arguments:
    ----------
    game_state:dict 
    A dictionary containing the current state of the game with all the details

    Returns:
    --------
    None    
    """
    __logger__.debug(f"Persists the current game stats..")
    try:
        # Initializing the file name for game stats
        file_name = "game_stats.json"

        # Open the file in the write mode
        with open(file_name, "w") as file:

            # dump the game_state dictionary as a json object
            json.dump(input_game_state, file)
    except Exception as e:
        __logger__.exception(str(e))


def initialise_game(all_words_file: str,
                    wordle_words_file=None,
                    secret_word=None,
                    max_guesses=6,
                    word_length=5) -> dict:
    """ 
    This method create and fill the game_state dictionary with entries suitable for starting a game

    Arguments:
    ----------
    all_words_file: str
    A variable containing the file name for all words file

    wordle_words_file:str with default None
    A variable containing the file name for wordle words file

    secret_word: str with default None
    A string that contains the secret of the game

    max_guesses : int with default 6
    A integer that contains the maximum guesses for the game

    word_length : int with default 5
    A integer that contains the length of the word

    Returns:
    --------
    game_state: dict
    A dictionary containing the current state of the game with all the details
    """
    __logger__.debug(f"Initializing the game..")

    # initializing the game_state variable
    global game_state
    try:
        # Checking for any persisted game in the current directory for game_state.json
        if os.path.exists("game_state.json"):

            # if already a game is persisted, load the game from json file into game_state dictionary
            with open("game_state.json", "r") as file:
                game_state = json.load(file)
        else:

            # Set the wordle words file name if it is None
            if wordle_words_file is None:
                wordle_words_file = 'wordle_words.txt'

            # Set the all words file name if it is None
            if all_words_file is None:
                all_words_file = 'english_dict.txt'

            # if the maximum guesses is 0 , Raise the below exception
            if max_guesses == 0:
                raise Exception("Max guesses must be 1 or more")

            # if the word length is 0, raise the below exception
            if word_length == 0:
                raise Exception("Word length must be 1 letter or more")

            # if Secret word is not provided, load a word from the wordle's file
            secret = ''
            if secret_word is None:

                # Append the file path with the file name
                file_name = os.path.join(current_dir, wordle_words_file)

                # Check whether the file exists
                if os.path.isfile(file_name):

                    # Open the file in r mode
                    with open(file_name, 'r') as file:

                        # load the words from the wordle file by checking the length with the word length
                        lines = [line.strip() for line in file.readlines() if len(line.strip()) == word_length]

                        # if there are no words raise Exception
                        if len(lines) == 0:
                            raise Exception("No valid words in wordle words file")
                        else:
                            # Otherwise choose a random word from the list as secret
                            secret = random.choice(lines)
            else:

                # Check the secret word for length if provided explicitly
                if len(secret_word) == word_length:
                    secret = secret_word
                else:
                    # Raise an exception
                    raise Exception("The secret word is not of the correct length")

            # Initialize Game history object with the initial maximum guesses variable
            initialize_game_history(max_guesses)

            # Assigning the values to the game_state dictionary
            game_state['secret_word'] = secret
            game_state['word_length'] = word_length
            game_state['max_guesses'] = max_guesses

            # Based on the maximum guesses , building the grid of game state
            guess_nested_list = []
            for i in range(max_guesses):
                guess_list = [''] * int(word_length)
                guess_nested_list.append(guess_list)
            game_state['grid'] = guess_nested_list

            # Based on the maximum guesses , building the color grid of game state
            color_nested_list = []
            for i in range(max_guesses):
                color_list = ['w'] * int(word_length)
                color_nested_list.append(color_list)
            game_state['colour_grid'] = color_nested_list
            game_state['i'] = 0
            game_state['j'] = 0
            game_state['status'] = 'playing'
            game_state['wordle_words_file'] = 'wordle_words.txt'
            game_state['all_words_file'] = all_words_file
            game_state['popup_queue'] = []
            game_state['active_letters'] = {
                "A": True, "B": True, "C": True, "D": True, "E": True, "F": True,
                "G": True, "H": True, "I": True, "J": True, "K": True, "L": True,
                "M": True, "N": True, "O": True, "P": True, "Q": True, "R": True,
                "S": True, "T": True, "U": True, "V": True, "W": True, "X": True,
                "Y": True, "Z": True
            }
            game_state['green_letters_with_pos'] = []
            game_state['green_letters_list'] = []
            game_state['green_letters_indices'] = []
            game_state['yellow_letters'] = []
            __logger__.debug(f"Current Game state : \n {game_state}")
            # Update the guess limit if changed in the game history list
            update_guess_limit_in_hist()
    except KeyboardInterrupt as err:
        persist_game_stats(game_state)
        __logger__.exception(str(err))
    except SystemExit as sysexit:
        persist_game_stats(game_state)
        __logger__.exception(str(sysexit))
    except Exception as e:
        persist_game_stats(game_state)
        __logger__.exception(str(e))
        raise e

    # Returning the game_state variable
    return game_state


def reset_game(input_game_state: dict, secret_word=None) -> None:
    """ 
    This method resets the game and the items in the game_state dictionary so that a new game can be played.

    Arguments:
    ----------
    game_state : dict
    A dictionary containing the current state of the game with all the details

    secret_word: str
    A string containing the secret word for the wordle game

    Returns:
    --------
    None
    """

    try:

        __logger__.debug(f"Resetting the game..")

        # Initializing the game_state variable as GLOBAL
        global game_state

        # Getting the all words file name from game_state dict
        all_words_file = input_game_state['all_words_file']

        # Getting the wordle words file name from the game state dict
        wordle_words_file = input_game_state['wordle_words_file']

        secret = input_game_state['secret_word']
        message1 = f"You have chosen to restart! The word was {secret}"

        # Resetting the game_state variable with the arguments
        game_state = initialise_game(all_words_file, wordle_words_file, secret_word)

        # Adding a message to the popup queue
        show_popup(input_game_state, "Restarting game", "text")
        show_popup(game_state, message1, "text")


        return

    except Exception as e:
        __logger__.exception(str(e))


def clear_game_state() -> None:
    """ 
    This method removes the game_state.json file if the file is present in the current directory
    the game is interrupted due to unforeseen circumstances

    Arguments:
    ----------
    None

    Returns:
    --------
    None

    """
    try:
        __logger__.debug("Clearing the game state if persisted..")

        # getting the file name with the current directory
        file_name = os.path.join(current_dir, "game_stats.json")

        # Checking the file exists and it is valid
        if os.path.exists("game_stats.json") and os.path.isfile(file_name):
            # Remove the file
            os.remove("game_stats.json")

    except Exception as e:
        __logger__.exception(str(e))


def validate_guess(game_state: dict) -> bool:
    """ 
    This method validates the individual guess made by the user based on its length and 
    availability in all words file

    Arguments:
    ----------
    game_state: dict
    A dictionary containing the current state of the game with all the details

    Returns:
    --------
    valid_guess_ind :bool
    A boolean with either True or False value representing whether guess is valid or not
    """

    __logger__.debug("Validating the guess..")

    # Setting the indicator to False
    valid_guess_ind = False
    try:
        # Fetching the all words file
        all_words_file = game_state['all_words_file']

        # fetching the word length in the game state dict
        word_len = game_state['word_length']

        # Adding the path to the all words file name
        file_name = os.path.join(current_dir, all_words_file)

        # Checking the existence of file
        if os.path.isfile(file_name):

            # Opening the file in read mode
            with open(file_name, 'r') as file:

                # Filtering the words from all words file based on word length
                lines = [line.strip() for line in file.readlines() if len(line.strip()) == word_len]

                # check whether there are 0 words for given length
                if len(lines) == 0:

                    # if True, raise Exception
                    raise Exception("No valid words in all words file")
                else:
                    # if False , check the validity of guess
                    i = game_state['i']
                    current_guess = "".join(game_state['grid'][i])
                    __logger__.debug(f"Current guess : {current_guess}")

                    # Checking the current guess for length and availability
                    if len(current_guess) == word_len and current_guess in lines:

                        # Setting indicator to 
                        valid_guess_ind = True
                    else:
                        # Adding a popup message to be displayed to the frontend
                        show_popup(game_state, "Invalid word\nUse clear or delete to edit your guess")

    except Exception as e:
        __logger__.exception(str(e))
        raise e

    # Return the indicator
    return valid_guess_ind


def process_guess(guess: list, secret_word: str) -> list:
    """ 
    This method processes the guess made with the secret word to determine the correct/incorrect letters in the guess.

    Arguments:
    ----------
    guess:list
    A list of characters containing the guess word made by the gamer

    secret_word:str
    A string containing the secret word for the game which has been played

    Returns:
    color_list : list
    A list containing the results of guess where each character is color-coded
    """

    __logger__.debug(f"Processing the guess..")
    global game_state

    # Initializing the list to store the color results of the guess
    color_list = []

    # combine the characters in the guess word as single string
    guess_word = "".join(guess)

    # Create a list to store the character that are already matched
    matched_list = []

    try:
        # Check whether the guess and secret are not empty
        if guess_word and secret_word:

            # check the guess and secret are equal
            if guess_word == secret_word:

                # Assign the color list if there is a complete match
                color_list = ['g', 'g', 'g', 'g', 'g']
            else:
                word_length = len(secret_word)

                # Looping for the length of the secret word
                for i in range(word_length):

                    # Checking whether character in guess is in secret and not in matched_list
                    if guess[i] in secret_word and guess[i] not in matched_list:

                        # Check whether the character is equal
                        if guess[i] == secret_word[i]:

                            # Append the character in matched list
                            matched_list.append(secret_word[i])

                            # Assign the color 'g' since there is a match
                            color_list.append('g')

                        else:
                            # Assign the color 'y' since there is no match
                            color_list.append('y')
                    else:

                        # Assign hyphen since the character is not in secret word
                        color_list.append('-')

                        # Change the state of character in the active_letters in the game_state as False
                        game_state['active_letters'][str(guess[i]).upper()] = False
                        # print(f"{active_letters}")
        else:
            __logger__.error("Either guess or secret_word is Empty")

    except Exception as e:
        __logger__.exception(str(e))

    # Returning the color list
    return color_list


def get_hints(game_state: dict) -> list:
    """ 
    This method fetches the hints for the gamer based on the current details in the game_state dict

    Arguments:
    ----------
    game_state: dict
    A dictionary containing the current state of the game with all the details

    Returns:
    --------
    A list of hints to be displayed to the gamer
    """
    __logger__.debug("Fetching the hints..")

    try:
        # Fetching the game details for hints 
        game_grid = game_state['grid']
        color_grid = game_state['colour_grid']
        word_len = game_state['word_length']
        filter_words = []
        hint_list = []
        file_name = os.path.join(current_dir, game_state['all_words_file'])

        # Looping over the color grid to fetch the matched characters
        for i, color_list in enumerate(color_grid):
            for j, color in enumerate(color_list):
                if color == 'g':
                    if {'char': game_grid[i][j], 'pos': j} not in game_state['green_letters_with_pos']:
                        game_state['green_letters_with_pos'].append({'char': game_grid[i][j], 'pos': j})
                    if game_grid[i][j] not in game_state['green_letters_list']:
                        game_state['green_letters_list'].append(game_grid[i][j])
                    if j not in game_state['green_letters_indices']:
                        game_state['green_letters_indices'].append(j)
                elif color == 'y':
                    if game_grid[i][j] not in game_state['yellow_letters']:
                        game_state['yellow_letters'].append(game_grid[i][j])

        # Appending the secret word into filter words list to remove it frm hints
        filter_words.append(game_state['secret_word'])

        # Appending the guesses into filter words list to remove it frm hints
        for word in game_grid:
            guess_word = "".join(word)
            filter_words.append(guess_word)

        # Loading all words file and reading all the valid letters to develop hints
        with open(file_name, 'r') as file:
            all_words = [line.strip() for line in file.readlines() if len(line.strip()) == word_len]

        # Filtering the words from all words list so that it is not added to hints
        filtered_word_list = list(filter(lambda x: x not in filter_words, all_words))

        # Removing duplicates from the green letters list
        unique_green_list = [dict(t) for t in {frozenset(d.items()) for d in game_state['green_letters_with_pos']}]

        initial_hint_list = []
        if unique_green_list:
            for s in filtered_word_list:
                # indicator to track if all characters match
                all_match = True

                for correct in unique_green_list:
                    char = correct['char']
                    index = correct['pos']

                    # Ensure index is an integer (if it's a string, convert it to integer)
                    if isinstance(index, str):
                        index = int(index)

                    # Check if the char matches the string at the specified index
                    if len(s) <= index or s[index] != char:
                        all_match = False
                        # Exit loop early if any condition fails
                        break

                        # If all characters matched at the correct positions, add the word to the hint_list
                if all_match:
                    initial_hint_list.append(s)
        else:
            initial_hint_list = filtered_word_list

        for s in initial_hint_list:
            # Create a new string by omitting characters at the specified indices
            modified_string = ''.join([s[i] for i in range(len(s)) if i not in game_state['green_letters_indices']])

            # Check if the remaining characters match the condition (contains all chars in char_list)
            if all(char in modified_string for char in game_state['yellow_letters']):
                hint_list.append(s)

        # Returning hint list
        return hint_list

    except Exception as e:
        __logger__.exception(str(e))
        raise e


def process_command(game_state: dict, command: str) -> bool:
    """ 
    This method take a user command passed as a str and update the game_state accordingly .

    Arguments:
    ----------
    game_state: dict
    A dictionary containing the current state of the game with all the details

    command:str
    A string containing the user command

    Returns:
    --------
    process_ind : bool
    A boolean value that indicates whether the game has ended. 
        if True - game has not ended.
        if False - game has ended
    """
    __logger__.debug(f"Processing the command..")
    start_time = time.time()
    __logger__.debug(f"Started : {start_time}")

    # Initializing the process_ind as True
    process_ind = True
    i = game_state['i']
    __logger__.debug(f"i is {i}")
    j = game_state['j']
    __logger__.debug(f"j is {j}")

    # Fetching the word length that is set in current game state 
    word_len = game_state['word_length']

    # Checking whether there is special character in the command
    special_char_list = re.findall(r"[^a-zA-Z0-9]+", command)
    try:
        # Checking whether the length of command > 0 and special char list > 0
        if len(command) > 1 and len(special_char_list) > 0:

            # Finding the index of the special character in the command
            index = command.find(special_char_list[0])

            # Splitting the word string
            word_str = command[:index]

            # Checking whether the word matches with the word length
            if len(word_str) == word_len:

                # Splitting the string into list of characters
                # word_str_list = str(word_str.strip()).split(",")

                # Processing each character as command
                for command in word_str:
                    process_command(game_state=game_state, command=command)

                # Processing the special character 
                process_command(game_state=game_state, command=special_char_list[0])
            else:

                # Setting the popup message for the show pop up method
                message = "Invalid word\nUse clear or delete to edit your guess"
                show_popup(game_state, message, "text")

        # Checking whether the command is a character 
        elif (len(command) == 1
              and re.fullmatch('^[A-Z]+$|^[a-z]+$', command)
              and command not in ['+', '!', '@', '-', '_', '*']):
            # check the length of current guess
            __logger__.debug(f"Command is {command}")
            if j < word_len:
                game_state['grid'][i][j] = command
                # print(f"{game_state['grid'][i][j]}")
                game_state['j'] = j + 1
            else:
                message = "Can't add more letters\nUse clear or delete to edit your guess."
                show_popup(game_state, message)
            # else:
                # raise Exception("Invalid Letter")

        # Checking whether the command is DELETE
        elif (command == 'delete' and len(special_char_list) == 0) or command == '-':
            __logger__.debug(f"Command is {command}")
            game_state['grid'][i][j - 1] = ''
            j -= 1
            game_state['j'] = j

        # Checking whether the command is clear
        elif (command == 'clear' and len(special_char_list) == 0) or command == '_':
            __logger__.debug(f"Command is {command}")
            game_state['grid'][i] = ['', '', '', '', '']
            j = 0
            game_state['j'] = j

        # Checking whether the command is 'enter'
        elif (command == 'enter' and len(special_char_list) == 0) or command == '+':
            __logger__.debug(f"Command is {command}")

            # Validating the guess
            if validate_guess(game_state):
                __logger__.debug(f"Validation of Guess is Passed")
                # curr_guess = "".join(game_state['grid'][i])

                # Processing the guess
                color_list = process_guess(game_state['grid'][i], game_state['secret_word'])

                __logger__.debug(f"color_list is {color_list}")
                # global game_state
                game_state['colour_grid'][i] = color_list

                # Decreasing the maximum guesses by 1
                game_state['max_guesses'] -= 1
                # __logger__.debug(f"{len(set(game_state['colour_grid'][i]))}")
                # __logger__.debug(f"{set(game_state['colour_grid'][i])}")
                # Checking whether the guess is correct
                if len(set(game_state['colour_grid'][i])) == 1 and game_state['colour_grid'][i] == ['g', 'g', 'g', 'g',
                                                                                                    'g']:
                    __logger__.debug("Guess is correct..")
                    game_state['status'] = 'won'
                    show_popup(game_state, "You won!")
                    process_command(game_state=game_state, command='share')
                    update_game_history()
                    clear_game_state()
                    process_ind = False
                else:
                    __logger__.debug("Guess is wrong..")

                    # Checking whether the guesses ran out
                    if game_state['max_guesses'] == 0:
                        __logger__.debug("Game is lost..")
                        game_state['status'] = 'lost'
                        message = f"You lose! The word was {game_state['secret_word']}"
                        show_popup(game_state, message)
                        process_command(game_state=game_state, command='share')
                        update_game_history()
                        clear_game_state()
                        process_ind = False
                    else:
                        __logger__.debug("Moving to next guess..")
                        game_state['i'] += 1
                        game_state['j'] = 0

        # Checking whether the command is 'restart'
        elif (command == 'restart' and len(special_char_list) == 0) or command == '!':
            __logger__.debug("Restarting the game..")
            reset_game(game_state)

        # Checking whether the command is share
        elif (command == 'share' and len(special_char_list) == 0) or command == '@':
            __logger__.debug("Sharing the status of the game")
            game_status = game_state['status']
            game_result_str = ""
            if game_status == 'won' or game_status == 'lost':
                results_list = game_state['colour_grid']
                color_white_list = ['w'] * int(game_state['word_length'])
                for guess_color in results_list:
                    guess_result = ""
                    if guess_color != color_white_list:

                        for char_result in guess_color:
                            unicode_char = ''
                            if char_result == 'g':
                                unicode_char = "\U0001F7E9"
                            elif char_result == 'y':
                                unicode_char = "\U0001F7E8"
                            elif char_result == '-':
                                unicode_char = "\U00002B1C"
                            guess_result = str(guess_result) + str(unicode_char)
                        game_result_str = str(game_result_str) + str(guess_result + "\n")
                show_popup(game_state, game_result_str, "share")

        # Checking whether the command is 'hint'
        elif (command == 'hint' and len(special_char_list) == 0) or command == '*':
            __logger__.debug("Fetching the hints for the game..")
            hint_list = get_hints(game_state=game_state)
            if len(hint_list) == 0:
                show_popup(game_state=game_state,
                           content="No hints found. Take a random guess or restart the game!",
                           mode="text")
            else:
                hint_word = random.choice(hint_list)
                guess_num = int(game_state['i'])
                for j in range(len(hint_word)):
                    game_state['grid'][guess_num][j] = hint_word[j]
                __logger__.debug(f"Hint : {game_state['grid'][guess_num]}")

        # Checking whether the command is history
        elif command == 'history':
            __logger__.debug("Loading the history of game..")
            if os.path.exists("game_history.txt"):
                with open("game_history.txt", "r") as file:
                    data = file.read().strip().split(",")
                    history = [int(x) for x in data]
                    show_popup(game_state, content=history, mode="history")

        # Checking whether the command is quit
        elif command == 'quit':
            __logger__.debug("Quitting the game")
            game_state['status'] = 'lost'
            secret = game_state['secret_word']
            update_game_history()
            clear_game_state()
            process_ind = False
            message = f"You have chosen to quit! The word was {secret}!"
            show_popup(game_state, message, "text")
        else:
            show_popup(game_state, "Invalid command", "text")
        __logger__.debug(f" Current Game state : \n {game_state}")
    except KeyboardInterrupt as err:
        persist_game_stats(game_state)
        __logger__.exception(str(err))
    except SystemExit as sysexit:
        persist_game_stats(game_state)
        __logger__.exception(str(sysexit))
    except Exception as e:
        persist_game_stats(game_state)
        __logger__.exception(str(e))
    finally:
        clear_game_state()
    end_time = time.time()
    execution_time = end_time - start_time
    __logger__.debug(f"Ended at {end_time}")
    __logger__.debug(f"Execution time: {execution_time}")
    __logger__.debug("-----------------------------------------")

    # Returning the process ind
    return process_ind
