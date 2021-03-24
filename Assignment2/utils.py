from typing import List, Tuple
from enum import Enum

import anytree

class Moves(Enum):
    RIGHT = 0
    LEFT = 1,
    UP = 2,
    DOWN = 3
             
def get_available_moves(y: int, x: int, max_y: int, max_x: int) -> List:
    moves = []

    if x > 0:
        moves.append(Moves.LEFT)

    if x < max_x - 1:
        moves.append(Moves.RIGHT)

    if y > 0:
        moves.append(Moves.UP)

    if y < max_y - 1:  
        moves.append(Moves.DOWN)
    
    return moves  

def find_number(input_puzzle: Tuple, number: int) -> Tuple[int, int]: 
    for y in range(0, len(input_puzzle)):
        for x in range(0, len(input_puzzle)):
            if number == input_puzzle[y][x]:
                return y, x
 
    return (-1, -1)

def final_puzzle(dim: int):
    new = []
    for y in range(0, dim):
        row = []
        for x in range(0, dim):
            row.append(y * dim + (x + 1))
        new.append(tuple(row))

    return tuple(new);

def is_number_correct(dim: int, number: int, pos: Tuple[int, int]):
    return final_puzzle(dim)[pos[0]][pos[1]] == number

def is_goal(input_puzzle) -> bool:
    for y in range(0, len(input_puzzle)):
        for x in range(0, len(input_puzzle[0])): 
            value = y * len(input_puzzle) + (x + 1)
            if input_puzzle[y][x] != value:
                return False
    return True

def generate_next_puzzle(original, pos: Tuple, move: Moves):  
    pos_y, pos_x = pos
    new = []
    if move == Moves.UP:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == pos_y - 1 and x == pos_x:
                    row.append(original[pos_y][pos_x])
                elif y == pos_y and x == pos_x:
                    row.append(original[y - 1][x])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))
    elif move == Moves.DOWN:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == pos_y + 1 and x == pos_x:
                    row.append(original[pos_y][pos_x])
                elif y == pos_y and x == pos_x:
                    row.append(original[y + 1][x])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))
    elif move == Moves.LEFT:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == pos_y and x == pos_x - 1:
                    row.append(original[pos_y][pos_x])
                elif y == pos_y and x == pos_x:
                    row.append(original[y][x - 1])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))
    else:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == pos_y and x == pos_x + 1:
                    row.append(original[pos_y][pos_x])
                elif y == pos_y and x == pos_x:
                    row.append(original[y][x + 1])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))

    return tuple(new)

def traceback(node: anytree.AnyNode):
    puzzles = [] 

    print("performing traceback");
   
    while node is not None:
        puzzles.append(node.value)         
        node = node.parent;

    return puzzles
