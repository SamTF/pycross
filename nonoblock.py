### NONOBLOCK
### Generates all the possible permutations for each line in the puzzle according to the grid size, blocks, and rules of Picross. Wihout duplicates!

from sympy.utilities.iterables import multiset_permutations
import re


def create_elements(blocks:list, size:int) -> list:
    '''
    Creates all the required elements (Squares and empty spaces) for this Nonogram row.
    Returns those elements as an array of arrays.

    blocks: Array of spaces required. Ex: 2 1 would be [2,1]
    size: The amount of cells in the row
    '''
    min_spaces = sum(blocks) + len(blocks) - 1          # the minimum amount of spaces needed for the block sequence
    free_spaces = size - min_spaces                     # free blocks remaining after that

    elements = []                                       # list to house all the required elements
    for i, b in enumerate(blocks):                      # loops thru each block in the sequence
        value = ['X'] * b                               # creates squares (Xs) equal to the block value
        if i != len(blocks) - 1: value += '.'           # adds a mandatory space after the squares if this is not the last block
        elements.append(value)                          # adds this value to the elements array
    
    elements.extend([['.'] for i in range(free_spaces)])    # creates an empty space for each remaining free space

    return elements


def check_order(combination:list, blocks:list) -> bool:
    '''
    Checks if the element sequence matches the required block instructions. Returns bool.

    combination: Array representing the way in which the row's elements were arranged.
    blocks: Array of spaces required in order.
    '''
    order =[]
    for c in combination:                               # loops thru every element in the combination
        block = c.count('X')                            # counts how many filled squares there are
        if block:   order.append(block)                 # appens it to the order if there were any
    
    return order == blocks                              # checks if this combination's block order matches the required block instructions

def check_valid(row:list):
    '''
    Checks if the permutation is valid within the rules of Nonograms: blocks must be sperated by a space.
    '''
    # checking if the last item of the previous element was a square, followed by a consecutive square with no gaps
    prev = None
    for x in row:
        if prev == 'X' and x[0] == 'X':
            return False
        prev = x[-1]
    
    return True

def create_combinations(blocks:list, size:int) -> list:
    '''
    Main function to create all *possible* combinations, given a set of block instructions and a cell size.

    blocks: Array of spaces required. Ex: 2 1 would be [2,1]
    size: The amount of cells in the row
    '''
    if blocks == [0]: return [f"{'.' * size}"]

    elements = create_elements(blocks, size)
    all_combinations = list(multiset_permutations(elements))

    possible_combinations = [c for c in all_combinations if check_order(c, blocks) and check_valid(c)]
    possible_combinations = [block2string(c) for c in possible_combinations]
    possible_combinations = list(set(possible_combinations))

    return possible_combinations


#####################################################################################

def block2string(l:list) -> str:
    '''
    Converts the 2D Array blocks into readable strings USING REGEX instead of loops. This is the fastest way of found to achieve this result.
    Example: (['X', '.'], ['X'], ['.'], ['.']) -> 'X.X..'
    '''
    string = re.sub('[^A-Za-z0-9.]+', '', str(l))
    return string



#####################################################################################