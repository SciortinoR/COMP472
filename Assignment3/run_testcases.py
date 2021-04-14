import os
import time

from helper import print_stats
from main import alpha_beta_search


if __name__ == '__main__':
    f = open('testcases.txt', 'r')
    for line in f:
        line = line.split()
        n_tokens = int(line[0])
        n_taken_tokens = int(line[1])

        # Use boolean list to denote taken tokens
        taken_tokens = [False]*(n_tokens+1)
        for i in range(n_taken_tokens):
            taken_tokens[int(line[2+i])] = True
        
        depth = int(line[-1])
        last_move = None if n_taken_tokens == 0 else int(line[-2])

        stats = {
            'nodes_vis': 0,
            'nodes_eval': 0,
            'max_depth': 0,
            'branching_factors': [],
            'start_time': time.time(),
            'end_time': None
        }

        # Run alpha beta pruning
        best_move, value = alpha_beta_search(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, stats)
        
        stats['end_time'] = time.time()

        print(f"Input: {' '.join(line[0:])}\n")
        print_stats(best_move, value, stats)
        print('\n')