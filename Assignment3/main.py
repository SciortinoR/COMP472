import sys
import time

from helper import get_next_removals, board_eval, print_stats


# Start PNT Game
def alpha_beta_search(n_tokens, n_taken_tokens, taken_tokens, last_move, max_depth, stats):
    value, best_move = None, None

    if n_taken_tokens % 2 == 0:
        value, best_move = max_value(n_tokens, n_taken_tokens, taken_tokens, last_move, 0, max_depth, float('-inf'), float('inf'), stats)
    else:
        value, best_move = min_value(n_tokens, n_taken_tokens, taken_tokens, last_move, 0, max_depth, float('-inf'), float('inf'), stats)

    return best_move, value


# Plays Max Player turn
def max_value(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, max_depth, alpha, beta, stats):
    stats['max_depth'] = max(stats['max_depth'], depth)
    stats['nodes_vis'] += 1

    next_removals = get_next_removals(n_tokens, n_taken_tokens, taken_tokens, last_move)
    if len(next_removals) == 0 or (max_depth != 0 and depth == max_depth):
        stats['nodes_eval'] += 1
        return board_eval(last_move, taken_tokens, next_removals, True), None
    
    v = float('-inf')
    best_move = None

    branches_visited = 0

    for move in next_removals:
        taken_tokens[move] = True

        v2, _ = min_value(n_tokens, n_taken_tokens + 1, taken_tokens, move, depth + 1, max_depth, alpha, beta, stats)

        branches_visited += 1

        if (v2 > v) or (v2 == v and (best_move is None or move < best_move)):
            v, best_move = v2, move
            alpha = max(alpha, v)

        # Backtrack next removal tokens
        taken_tokens[move] = False

        if v >= beta:
            break

    stats['branching_factors'].append(branches_visited)
    return v, best_move


# Plays Min Player turn
def min_value(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, max_depth, alpha, beta, stats):
    stats['max_depth'] = max(stats['max_depth'], depth)
    stats['nodes_vis'] += 1

    next_removals = get_next_removals(n_tokens, n_taken_tokens, taken_tokens, last_move)
    if len(next_removals) == 0 or (max_depth != 0 and depth == max_depth):
        stats['nodes_eval'] += 1
        return board_eval(last_move, taken_tokens, next_removals, False), None
    
    v = float('inf')
    best_move = None

    branches_visited = 0

    for move in next_removals:
        taken_tokens[move] = True

        v2, _ = max_value(n_tokens, n_taken_tokens + 1, taken_tokens, move, depth + 1, max_depth, alpha, beta, stats)

        branches_visited += 1

        if (v2 < v) or (v2 == v and (best_move is None or move < best_move)):
            v, best_move = v2, move
            beta = min(beta, v)

        # Backtrack next removal tokens
        taken_tokens[move] = False

        if v <= alpha:
            break
    
    stats['branching_factors'].append(branches_visited)
    return v, best_move


if __name__ == '__main__':
    n_tokens = int(sys.argv[1])
    n_taken_tokens = int(sys.argv[2])

    # Use boolean list to denote taken tokens
    taken_tokens = [False]*(n_tokens+1)
    for i in range(n_taken_tokens):
        taken_tokens[int(sys.argv[3+i])] = True
    
    depth = int(sys.argv[-1])
    last_move = None if n_taken_tokens == 0 else int(sys.argv[-2])

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
    print_stats(best_move, value, stats)