from typing import List, Tuple
from enum import Enum

class Moves(Enum):
    RIGHT = 0
    LEFT = 1,
    UP = 2,
    DOWN = 3
             
def get_available_moves(y: int, x: int, max_y: int, max_x: int) -> List:
    moves = []
    if x < max_x - 1:
        moves.append(Moves.RIGHT)

    if x > 0:
        moves.append(Moves.LEFT)

    if y > 0:
        moves.append(Moves.UP)

    if y < max_y - 1:  
        moves.append(Moves.DOWN)
    
    return moves  

def find_nine(input_puzzle) -> Tuple[int, int]:
    for y in range(0, len(input_puzzle)):
        for x in range(0, len(input_puzzle[0])):
            if input_puzzle[y][x] == 9:
                return y, x

    return (-1, -1)

def is_goal(input_puzzle) -> bool:
    for y in range(0, len(input_puzzle)):
        for x in range(0, len(input_puzzle[0])): 
            value = y * len(input_puzzle) + (x + 1)
            if input_puzzle[y][x] != value:
                return False
    return True

def generate_move_puzzle(original, pos: Tuple, move: Moves):  
    nine_y, nine_x = pos
    new = []
    if move == Moves.UP:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == nine_y - 1 and x == nine_x:
                    row.append(9)
                elif y == nine_y and x == nine_x:
                    row.append(original[y - 1][x])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))
    elif move == Moves.DOWN:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == nine_y + 1 and x == nine_x:
                    row.append(9)
                elif y == nine_y and x == nine_x:
                    row.append(original[y + 1][x])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))
    elif move == Moves.LEFT:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == nine_y and x == nine_x - 1:
                    row.append(9)
                elif y == nine_y and x == nine_x:
                    row.append(original[y][x - 1])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))
    else:
        for y in range(0, len(original)):
            row = [];
            for x in range(0, len(original[0])):
                if y == nine_y and x == nine_x + 1:
                    row.append(9)
                elif y == nine_y and x == nine_x:
                    row.append(original[y][x + 1])
                else:
                    row.append(original[y][x])
            new.append(tuple(row))

    return tuple(new)
