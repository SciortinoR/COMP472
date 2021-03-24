from collections import deque
from typing import Set, Tuple

import anytree
import utils

def place_number(discovered: Set, puzzle: Tuple, parent: anytree.AnyNode, number: int):
    stack = deque()
    stack.append((puzzle, parent))

    while stack:
        curr_puzzle, parent = stack.pop()
        curr_node = anytree.AnyNode(value=curr_puzzle, parent=parent)

        y, x = utils.find_number(curr_puzzle, number)
        if utils.is_number_correct(len(puzzle), number, [y, x]):
            return curr_node

        dim = len(puzzle)
        for move in reversed(utils.get_available_moves(y=y, x=x, max_y=dim, max_x=dim)):
            new_puzzle = utils.generate_next_puzzle(curr_puzzle, [y, x], move)
            
            if new_puzzle not in discovered:
                discovered.add(new_puzzle)
                stack.append((new_puzzle, curr_node))  

def depth_first_search(input_puzzle): 
    print("Starting Depth first Search on {}".format(input_puzzle))

    discovered = set([input_puzzle])

    stack = deque()
    stack.append(anytree.AnyNode(value=input_puzzle, parent=None))
 
    curr_number = 1
    while stack:
        curr_node = stack.pop()
        curr_puzzle = curr_node.value
        curr_parent = curr_node.parent
        
        if utils.is_goal(curr_puzzle):
            print("Goal reached")
            return utils.traceback(curr_node)

        stack.append(place_number(
            discovered=discovered, puzzle=curr_puzzle, 
            parent=curr_parent, number=curr_number))

        curr_number = curr_number + 1
        if curr_number == 10:
            curr_number = 1
