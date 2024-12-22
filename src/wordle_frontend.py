# wordle_front_end.py

# updated 18th Nov to correct calls to show_popup
# (prev incorrectly been named popup_message)

# updated 6th Dec removed You Won/Lost!!! messages
# (should be triggered in your backend)


from wordle_backend import *
from IPython.display import HTML, clear_output
import time

template_html = """
<style>
.container div.white { background-color: white; border: 1px solid black;} 
.container div.grey { background-color: grey; color: white; } 
.container div.green { background-color: green; color: white;} 
.container div.yellow { background-color: goldenrod; color: white;} 

.container {
  padding-top: 1em;
  grid-template-columns: repeat(5, 50px);
  grid-template-rows: repeat(6, 50px);
  display: grid;
}

.container div {
  text-transform: uppercase;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  width: 2em;
  height: 2em;
  line-height: 2em;
  text-align: center;
  font-size: 1.5em;
  margin: 0 0 0 0;
}

.game_state {
    position: relative;
}

.popup {
  position:absolute; top:0; left:0;
  text-align: center;
}

.popup div {
  margin-top: 5px;
  width: 200px;
  background: black;
  padding-top: 0.2em;
  padding-bottom: 0.2em;
  visibility: visible;
  color: white;
  opacity: 0;
  animation: fade 2.5s linear;
}

@keyframes fade {  0%, 100% { opacity: 0 } 20%, 80% { opacity: 1 } }

.container div.r0{  grid-row: 1; }
.container div.r1{  grid-row: 2; }
.container div.r2{  grid-row: 3; }
.container div.r3{  grid-row: 4; }
.container div.r4{  grid-row: 5; }
.container div.r5{  grid-row: 6; }

.container div.c0{  grid-column: 1; }
.container div.c1{  grid-column: 2; }
.container div.c2{  grid-column: 3; }
.container div.c3{  grid-column: 4; }
.container div.c4{  grid-column: 5; }

</style>
<div class="game_space">
<div class="popup">  </div>
  <div class="container">
    <div class="r0 c0"></div>
    <div class="r0 c1"></div>
    <div class="r0 c2"></div>
    <div class="r0 c3"></div>
    <div class="r0 c4"></div>

    <div class="r1 c0"></div>
    <div class="r1 c1"></div>
    <div class="r1 c2"></div>
    <div class="r1 c3"></div>
    <div class="r1 c4"></div>

    <div class="r2 c0"></div>
    <div class="r2 c1"></div>
    <div class="r2 c2"></div>
    <div class="r2 c3"></div>
    <div class="r2 c4"></div>

    <div class="r3 c0"></div>
    <div class="r3 c1"></div>
    <div class="r3 c2"></div>
    <div class="r3 c3"></div>
    <div class="r3 c4"></div>

    <div class="r4 c0"></div>
    <div class="r4 c1"></div>
    <div class="r4 c2"></div>
    <div class="r4 c3"></div>
    <div class="r4 c4"></div>

    <div class="r5 c0"></div>
    <div class="r5 c1"></div>
    <div class="r5 c2"></div>
    <div class="r5 c3"></div>
    <div class="r5 c4"></div>
  </div>
  </div>
"""

def print_game_state(game_state):
    temp = game_state['allowed_words']
    game_state['allowed_words'] = "..."
    print(game_state)
    game_state['allowed_words'] = temp
    return
    
def fill_template(game_state, template_html):
    col_dict = { 'g':'green','y':'yellow','-':'grey','w':'white' }
    grid = game_state['grid']
    colour_grid = game_state['colour_grid']
    max_guesses = len(grid)
    word_length = len(grid[0])
    n_row = max_guesses
    n_col = word_length
    for i in range(n_row):
        for j in range(n_col): 
            letter = grid[i][j]
            col_code = colour_grid[i][j]
            colour = col_dict[col_code]
            template_html = template_html.replace(f'r{i} c{j}">',f'{colour} r{i} c{j}">{letter}')

    popup_queue = game_state['popup_queue']
    while len(popup_queue) > 0:
        content, mode = popup_queue.pop(-1)
        target = '<div class="popup">'
        div = f'<div>{content}</div>'
        template_html = template_html.replace(target, target+div)
    return template_html

def get_guess_str(game_state,i=None):
    if i is None:
        i = game_state['i']
    guess = "".join(game_state['grid'][i])
    return guess
    
def display_game_terminal(game_state):
    popup_queue = game_state['popup_queue']
    while len(popup_queue) > 0:
        content, mode = popup_queue.pop()
        print(content)    
    col_dict = {}
    col_dict['y'] = "🟨"
    col_dict['g'] = "🟩"
    col_dict['-'] = "⬜"
    col_dict['w'] = "?"
    grid = game_state['grid']
    colour_grid = game_state['colour_grid']
    i = game_state['i']
    max_guesses = len(grid)
    word_length = len(grid[0])
    n_row = max_guesses
    n_col = word_length
    if game_state['i'] < max_guesses:
        n_print = game_state['i'] + 1
    else: n_print=max_guesses
    for i in range(n_print):
        print("\t".join(grid[i]))
        col_blocks = "\t".join([ col_dict[x] for x in game_state['colour_grid'][i]])
        print(col_blocks)
        print("-\t"*5)


def display_game_notebook(game_state):
    clear_output(wait=True)
    time.sleep(0.05)
    display(HTML(fill_template(game_state, template_html)))
    return

def take_input_notebook():
    command = input("enter command: ")
    return command

def run_game_notebook(game_state):
    finished = False
    while game_state['status'] == 'playing':
        display_game_notebook(game_state)
        command = take_input_notebook()
        process_command(game_state, command )
    display_game_notebook(game_state)
        
def run_game_terminal(game_state):
    finished = False
    while game_state['status'] == 'playing':
        display_game_terminal(game_state)
        command = input("enter command: ")
        process_command(game_state, command )
    display_game_terminal(game_state) 
