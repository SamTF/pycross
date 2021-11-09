from typing import Dict, List                               # for type hinting/documentation
import nonoblock as nb                                      # my script that generates all possible permutations of blocks within a line according to the rules of nonograms


SIZE = 5
BLOCKS = {
    "rows" : [ [5], [1], [5], [1], [5] ],
    "cols" : [ [3,1], [1,1,1], [1,1,1], [1,1,1], [1,3] ] 
}

# BLOCKS = {
#     "rows" : [ [5], [1], [1], [1], [5] ],
#     "cols" : [ [1,1], [1,2], [1,1,1], [2,1], [1,1] ] 
# }

# BLOCKS = {
#     "rows" : [ [1,1], [5], [1,1], [5], [1,1] ],
#     "cols" : [ [1,1], [5], [1,1], [5], [1,1] ] 
# }

# BLOCKS = {
#     "rows" : [ [3], [2,2], [1,1], [2,2], [3] ],
#     "cols" : [ [3], [2,2], [1,1], [2,2], [3] ] 
# }

# BLOCKS = {
#     "rows" : [ [5], [1,1,1], [5], [1], [1] ],
#     "cols" : [ [5], [1,1], [3], [1,1], [3] ] 
# }

# BLOCKS = {
#     "rows" : [ [2,1], [2,1], [1], [2,1], [2,1] ],
#     "cols" : [ [2,2], [2,2], [0], [1,1], [3] ] 
# }


# SIZE = 10
# BLOCKS = {
#     "rows" : [ [2], [4], [6], [8], [10],      [4,4], [4,4], [10], [10], [10] ],
#     "cols" : [ [6], [7], [8], [9], [5,3],      [5,3], [9], [8], [7], [6]  ] 
# }
# BLOCKS = {
#     "rows" : [ [3,2], [2,1,1], [2,1,1], [2,1], [3,2],   [4,3], [5,4], [4,3], [4,3], [10] ],
#     "cols" : [ [10], [10], [1,6], [5], [1,1],           [1], [1,1], [2,5], [1,6], [10]  ] 
# }

# SIZE = 10
# BLOCKS = {
#     "rows" : [ [], [], [], [], [],      [], [], [], [], [] ],
#     "cols" : [ [], [], [], [], [],      [], [], [], [], []  ] 
# }

# SIZE = 10
# BLOCKS = {
#     "rows" : [ [1,1], [1,1], [10], [1,2,2], [3,1],      [1,1,1], [3,1], [4,2], [10], [1,1] ],
#     "cols" : [ [7], [1,1,4], [1,7], [3,2], [1,1],      [1,1], [2,1], [1,1,1], [2,3], [7]  ] 
# }

# SIZE = 10
# BLOCKS = {
#     "rows" : [ [2,2], [2,4,2], [1,3,2,1], [4,3], [4,3],     [3,4], [2,5], [6], [4], [2,2] ],
#     "cols" : [ [2], [2,4], [1,6,1], [5,3], [4,3],           [1,4], [9], [1,6,1], [2,4], [2]  ] 
# }



def gen_all_combinations(l:List[int]) -> List[List[str]]:
    '''
    Generating every permutation possible for every row. Returns a 2D list of permutations as strings.
    Ex: [ [X.X.X], [XX.XX], [XXXX], [XXX.., .XXX., ..XXX], [XX.X., XX..X, .XX.X] ]
    '''
    combinations = []
    size = len(l)

    for block in l:
        block_combinations = nb.create_combinations(block, size)
        block_combinations = [nb.block2string(c) for c in block_combinations]        
        combinations.append(block_combinations)
    
    return combinations

   

def invert(board:List[list], join=False) -> List[list]:
    '''
    Turns the rows into columns.
    '''
    columns = []
    for i in range(SIZE):
        col = [x[i] for x in board] if not join else ''.join([x[i] for x in board])
        columns.append(col)

    return columns


def output_puzzle_info(Blocks: Dict[str, List[int]]) -> None:
    '''
    Prints all the puzzle info known to the player.
    '''
    size = (len(Blocks['rows']), len(Blocks['cols']))
    print(f'Grid: {size[0]}x{size[1]}')
    print(f'Row blocks:', end='')
    print(*Blocks['rows'], sep=" ")
    print(f'Col blocks:', end='')
    print(*Blocks['cols'], sep=" ")


# The starting point of the Deduction - finding the guaranteed moves
def guaranteed_moves(axis_combinations:List[List[str]], guaranteed:List[str] = None) -> List[str]:
    '''
    Finds all the positions for each line that all permutations have in common. These moves are guaranteed and are used to deduce the solution.
    Unknown positions are left as ?.
    Ex: [2 1] => '?X???'
    '''
    if not guaranteed:  guaranteed = [ ['?'] * SIZE ] * SIZE        # initialising a list of X unknown elements for the entire axis, if no previous Guaranteed list has been specified

    for i, axis in enumerate(axis_combinations):                    # looping over the permutations of every line in this axis
        deduction = guaranteed[i].copy()                            # initialising a list of X unknown elements for this specific line

        for position in range(0, SIZE):                             # looking at every position in the line
            x   = all(comb[position] == 'X' for comb in axis)       # checking if ALL elements in all permutation are FILLED (X) at this position
            dot = all(comb[position] == '.' for comb in axis)       # checking if ALL elements in all permutation are EMPTY  (.) at this position

            if x:   deduction[position] = 'X'                       # if all permutations have an X at this position, the X is gauranteed
            if dot: deduction[position] = '.'                       # if all permutations have a dot at this position, the . is gauranteed
        
        guaranteed[i] = deduction                                   # adding this line's guaranateed moves to the main list
    
    return guaranteed


def deduce(combinations:Dict[str, List[str]], guaranteed:List[str], rows=True, r:int=0) -> List[str]:
    '''
    Uses logic to deduce the correct moves and solve the puzzle! Returns the solved puzzle as a list of strings with Xs and Dots.
    combinations: Dict of every possible combination for every line in every axis
    guaranteed: List containing all the 100% guaranteed moves. Used to deduce the rest of the movies.
    rows: Whether we're currently iterating over rows or columns. Columns need to be inverted.
    r: The current loop in the recursion. Used to stop before a fatal StackOverflow error is reached.
    '''
    if not rows: guaranteed = invert(guaranteed)                                        # transposes data if checking columns instead of rows
    print(guaranteed, rows)

    axis_combinations = combinations['rows'] if rows else combinations['cols']
    possible_combinations = []                                                          # all the combinations that match the guaranteed known values

    for i, axis in enumerate(axis_combinations):                                        # looping over every row
        axis_possible = []                                                              # all the combinations possible for this axis given the guaranteed values
        g = guaranteed[i]                                                               # getting the guaranteed values for this column/row
        indicies = [pos for pos, char in enumerate(g) if char == 'X' or char == '.']    # Getting all the positions where the value is known for sure (X or dot, no question mark)
        
        if not indicies:                                                                # failsafe in case every position is marked with '?
            print('no values are guanateed for this axis')
            possible_combinations.append(axis)                                          # every value is still possible because none have been eliminated
            continue

        for pos in axis:                                                                # looping over every combination in this line
            match = all(pos[i] == g[i] for i in indicies)                               # checking if this combination's values ALL match up with the guaranteed values
            if (match):
                axis_possible.append(pos)
        
        possible_combinations.append(axis_possible)                                     # appending this row/col's possible combinations to the overall list
    

    # Adding the finished rows/columns to the guaranteed list
    for i, axis in enumerate(possible_combinations):
        if len(axis) == 1: guaranteed[i] = axis[0]                                      # if there is only 1 possibility, it's guaranteed to be the correct solution

    # Puzzle if finished when no more question marks are left in the guaranteed list
    puzzle_solved = not any('?' in row for row in guaranteed)

    ### END if puzzle is solved or CONTINUE WITH RECURSION if not yet solved
    if puzzle_solved:
        solution = guaranteed if rows else invert(guaranteed)                           # rotates the solution the right way up in case it was using columns instead of rows
        print('\n\n🎈🎈🎈 HORAYYY WE SOLVED IT!!! 🎈🎈🎈')
        print('-' * (SIZE+4))
        for block in solution:  print(f'| {nb.block2string(block)} |')
        print('-' * (SIZE+4))

        return solution
    
    # Raises an error if solving is taking too many recursions: meaning the algo can't solve it.
    if r >= 50:
        print('=====> PUZZLE IS NOT SOLVEABLE!!' * 5)
        raise RecursionError('Puzzle is not solveable by this algo!') 
    
    else:
        print('********************')
        print('NEEDS MORE DEDUCING')
        print('********************')
        return deduce(combinations, guaranteed, not rows, r+1) # !! don't forget the RETURN keyword when calling functions recursively!



##################################################
def solve(Blocks: Dict[str, List[int]]):
    global SIZE
    SIZE = len(Blocks['rows'])

    combinations = {
        'rows' : gen_all_combinations(Blocks['rows']),
        'cols' : gen_all_combinations(Blocks['cols'])
    }
    # print(combinations)

    guaranteed = guaranteed_moves(combinations['cols'])
    guaranteed = guaranteed_moves(combinations['rows'], invert(guaranteed))

    solution = deduce(combinations, guaranteed)

    return solution



### Testing the solver algo
if __name__ == "__main__":
    BLOCKS = {
        "rows" : [ [5], [1], [5], [1], [5] ],
        "cols" : [ [3,1], [1,1,1], [1,1,1], [1,1,1], [1,3] ] 
    }
    BLOCKS = {
        "rows" : [ [5], [1,1,1], [5], [1], [1] ],
        "cols" : [ [5], [1,1], [3], [1,1], [3] ] 
    }
    BLOCKS = {
        "rows" : [ [2], [4], [6], [8], [10],      [4,4], [4,4], [10], [10], [10] ],
        "cols" : [ [6], [7], [8], [9], [5,3],      [5,3], [9], [8], [7], [6]  ] 
    }
    BLOCKS = {
    "rows" : [ [2,2], [2,4,2], [1,3,2,1], [4,3], [4,3],     [3,4], [2,5], [6], [4], [2,2] ],
    "cols" : [ [2], [2,4], [1,6,1], [5,3], [4,3],           [1,4], [9], [1,6,1], [2,4], [2]  ] 
}

    solve(BLOCKS)