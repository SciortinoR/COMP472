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

def find_nine(input_puzzle: List) -> Tuple[int, int]:
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
    new = []
    if move == Moves.LEFT:
        new[pos[0]][pos[1]] = new[pos[0]][pos[1] - 1]
        new[pos[0]][pos[1] - 1] = 9;
        
        return new
    elif move == Moves.RIGHT:
        new[pos[0]][pos[1]] = new[pos[0]][pos[1] + 1]
        new[pos[0]][pos[1] + 1] = 9;
        
        return new
    elif move == Moves.UP:
        new[pos[0]][pos[1]] = new[pos[0] - 1][pos[1]]
        new[pos[0] - 1][pos[1]] = 9;
        
        return new

    elif move == Moves.DOWN:
        new[pos[0]][pos[1]] = new[pos[0] + 1][pos[1]]
        new[pos[0] + 1][pos[1]] = 9;
        
        return new
    else:
        return new


