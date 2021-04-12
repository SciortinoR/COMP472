import os
from Assignment3 import main
import random

number_of_test_cases = 10

for i in range(int(number_of_test_cases)):
    number_of_tokens = random.randint(1, 20)
    number_of_played_moves = random.randint(0, number_of_tokens-1)
    moves = []

    for j in range(number_of_played_moves):
        last_move = moves[-1] if moves else None
        possible_moves = main.legal_moves(number_of_tokens, moves, last_move)
        if possible_moves:
            moves.append(possible_moves[random.randint(0, len(possible_moves)-1)])
        else:
            number_of_played_moves = len(possible_moves)

    max_depth = random.randint(1, 20)
    print("="*50)
    moves_str = [str(i) for i in moves]
    space = " "

    if number_of_played_moves == 0:
        print(f"Running test case: {number_of_tokens} {number_of_played_moves} {max_depth}")
        os.system(f"main.py {number_of_tokens} {number_of_played_moves} {max_depth}")
    else:
        print(f"Running test case: {number_of_tokens} {number_of_played_moves} {space.join(moves_str)} {max_depth}")
        os.system(f"main.py {number_of_tokens} {number_of_played_moves} {space.join(moves_str)} {max_depth}")
