from collections import deque
from typing import List

import anytree
import utils

def depth_first_search(input_puzzle): 
    print("DEPTH FIRST SEARCH")

    stack = deque()
    stack.append((input_puzzle, None))

    discovered = set([input_puzzle])
 
    while stack:
        current_puzzle, parent = stack.pop()
        current_node = anytree.AnyNode(value=current_puzzle, parent=parent)

        if utils.is_goal(current_puzzle):
            print("GOAL REACHED")
            return current_puzzle

        dim = (len(input_puzzle), len(input_puzzle[0]))
        pos = utils.find_nine(input_puzzle=current_puzzle) 

        for move in reversed(utils.get_available_moves(y=pos[0], x=pos[1], max_y=dim[0], max_x=dim[1])): 
            new_puzzle = utils.generate_move_puzzle(current_puzzle, pos, move)
            
            if new_puzzle not in discovered:
                discovered.add(new_puzzle)
                stack.append((new_puzzle, current_node))  
