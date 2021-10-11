import numpy as np
from enum import Enum

np.random.seed(0)  # seed for reproducibility

# Clean way to represent space states: either filled in or blank
class Space(Enum):
    filled = 1
    blank = 0
    empty = 2

# Graphics icons for the console
ICONS = ['x', '█', '.']

def generate_board(rows: int, cols: int = 0, blank: bool = False):
    '''
    Generates a 2D array of 1s and 0s of specified size.
    
    rows: How many rows the board will have
    cols: Equal to rows if no value is specified
    blank: If True, every cell will have a blank value.
    '''
    if not cols:    cols = rows
    
    print(f'\nGenerated board with size: {rows}x{cols}')

    board = np.random.randint(2, size=(rows, cols)) if not blank else np.full((rows, rows), Space.empty.value)

    return board


def check_pos_filled(board: np.ndarray, x:int, y:int) -> bool:
    '''
    Checks if a position on the board can be filled in. Returns a boolean.
    x: row index
    y: column index
    '''
    pos = board[y, x]

    return(pos == Space.filled.value)


def create_guides(board):
    '''
    Generates the number guides for each axis on the board.
    '''
    guides = {}
    guides['rows'] = create_axis_guides(board)
    guides['cols'] = create_axis_guides(board.T)

    return guides

def create_axis_guides(board):
    '''
    Generates a number guide for each row/column in a single axis
    '''
    axis_guides = []

    # loops through every row/column
    for row in board:
        zeroes = (np.where(row == Space.blank.value))[0]                    # gets the indices of all values equal to the Blank Space value (0) as an array
        split_arrays = np.split(row, zeroes)                                # splits the array at each blank value into sub arrays
        g = np.array([i.sum() for i in split_arrays])                       # sums each the split array and combines the result into a single array (counts how many consecutive filled spaces there are)
        guide = g[g != 0]                                                   # filters out the zeroes
        
        guide = guide.tolist()                                              # converts the np array to a normal python list (for readability in the console)

        axis_guides.append(guide)                                           # appends the current axis guide to the overall axis guides array
    
    return axis_guides
        

# this is so simple with numpy that there's no need to even have a function do this
def invert_board(board: np.ndarray) -> np.ndarray:
    return board.T


# a nicer way to visualise the guides in the console
def print_guides():
    print('\n--- ROW GUIDES ---------')
    print((GUIDES['rows']))
    print('\n--- COL GUIDES ---------')
    print((GUIDES['cols']))


# Prints the board to the console using ICONS instead of 1s and 0s
def get_icon(i):
    # if i == Space.empty.value: return i
    return ICONS[i]

def draw_icons(board):
    print('\n#################################\n')
    print(np.vectorize(get_icon)(board))
    print_guides()


# playing the actual game
def fill_in(x:int, y:int, fill=True) -> None:
    '''
    Allows players to fill in and cross out specific positions, currently only if they are correct moves. (maybe l'll change this in the future)
    Returns the new board if the move is possible.

    solution_board: The randomly generated board with the picture
    player_board: The board that players are controlling
    x: Row index of the space
    y: Column index of the space
    fill: True to fill in space, False to cross it out
    '''
    global player_board
    
    # if the position already has a value (filled in or cross out)
    if player_board[y, x] != Space.empty.value:
        print(f'>>> Position ({x}, {y}) is already filled in.')
        return


    # if the player wants to fill in a correct position, fill it
    if check_pos_filled(BOARD, x, y) and fill:
        player_board[y, x] = Space.filled.value

        draw_icons(player_board) # only relevant for the CLI version
        win_check()
        
        return
    
    # if the player wants to cross out a correct blank position, cross it
    elif not check_pos_filled(BOARD, x, y) and not fill:
        player_board[y, x] = Space.blank.value
        draw_icons(player_board)
        return
    
    else:
        print('>>> WRONG MOVE!')
    

def win_check():
    '''
    Checks if the player has one by seeing if the player's filled in ALL the same positions filled in on the solution BOARD. Ignores crossed out and blank positions.
    Prints a cool victory message if true.
    '''
    attempt     = np.where(player_board == Space.filled.value)[0]               # all positions equal to the filled in value on the player's board
    solution    = np.where(BOARD        == Space.filled.value)[0]               # all positions equal to the filled in value on the main BOARD
    
    if attempt.shape != solution.shape: return                                  # ends the check right here if these arrays don't have the same amount of values

    win = (attempt == solution).all()                                           # compares if these indicies are the same

    if win:
        print('\n>>> CONGRATULATIONS! YOU WIN!! 🥳\n' * 3)


################################
SIZE = 5
BOARD = generate_board(SIZE)
GUIDES = create_guides(BOARD)

player_board = generate_board(SIZE, blank=True)
draw_icons(player_board)