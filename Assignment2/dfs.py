from collections import deque
from typing import List

import anytree
import utils

def depth_first_search(input_puzzle: List): 
    stack = deque()
    stack.append(anytree.AnyNode(id="root", value=input_puzzle))

    while stack:
        current_node = stack.pop()

        print(current_node.value)

        if utils.is_goal(current_node.value):
            return current_node.value

        if anytree.search.find(current_node, lambda node: node.value == current_node.value) is not None:
            continue

        dim = (len(input_puzzle), len(input_puzzle[0]))
        pos = find_nine(input_puzzle=input_puzzle) 

        for move in reversed(get_available_moves(y=pos[0], x=pos[1], max_y=dim[0], max_x=dim[1])): 
            new_puzzle = generate_move_puzzle(input_puzzle, pos, move)
           
            print('new puzzle {}', new_puzzle)

            if anytree.search.find(current_node, lambda node: node.value == new_puzzle) is None:
                stack.append(anytree.AnyNode(value=new_puzzle, parent=current_node))
