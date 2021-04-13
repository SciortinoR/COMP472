import math
from game import evaluate_board, get_possible_moves

def alpha_beta_search(N, taken_tokens, depth, last_move, isMaximizingTurn): 
    # Generate available tokens 
    tokens = set([i for i in range(1, N + 1) if i not in taken_tokens])

    # Create stats dict
    stats = {
        "depth_reached": 0,
        "visited_nodes": 0,
        "evaluated_nodes": 0,
        "parents": 0,
        "branches": 0,
    }

    # Compute next best move
    if isMaximizingTurn:
        score, move = max_value(N, tokens, last_move, 0, depth, -math.inf, math.inf, stats) 
    else:
        score, move = min_value(N, tokens, last_move, 0, depth, -math.inf, math.inf, stats)
    return score, move, stats

def max_value(N, tokens, last_move, depth, max_depth, alpha, beta, stats):
    stats["visited_nodes"] += 1
    stats["depth_reached"] = max(stats["depth_reached"], depth)

    possible_moves = get_possible_moves(N, tokens, last_move, last_move == 0)

    # Terminal State
    if not possible_moves or 1 < depth == max_depth:
        stats["evaluated_nodes"] += 1
        score = evaluate_board(N, possible_moves, last_move, True)
        return score, None

    # Count the nodes which have successors
    stats["parents"] += 1

    # Explore successors
    v, best_move = -math.inf, None
    for move in possible_moves:
        # Count explored branches
        stats["branches"] += 1

        tokens.remove(move)  # Do move
        score, _ = min_value(N, tokens, move, depth + 1, max_depth, alpha, beta, stats)
        tokens.add(move)  # Undo move

        if score > v:
            v, best_move = score, move
            alpha = max(alpha, v)
        if v >= beta:
            return v, best_move

    return v, best_move

def min_value(N, tokens, last_move, depth, max_depth, alpha, beta, stats):
    stats["visited_nodes"] += 1
    stats["depth_reached"] = max(stats["depth_reached"], depth)

    possible_moves = get_possible_moves(N, tokens, last_move, last_move == 0)

    # Terminal State
    if not possible_moves or 1 < depth == max_depth:
        stats["evaluated_nodes"] += 1
        score = evaluate_board(N, possible_moves, last_move, False)
        return score, None

    # Count the nodes which have successors
    stats["parents"] += 1

    # Explore successors
    v, best_move = math.inf, None
    for move in possible_moves:
        # Count explored branches
        stats["branches"] += 1
        
        tokens.remove(move)  # Do move
        score, _ = max_value(N, tokens, move, depth + 1, max_depth, alpha, beta, stats)
        tokens.add(move)  # Undo move

        if score < v:
            v, best_move = score, move
            beta = min(beta, v)
        if v <= alpha:
            return v, best_move
            
    return v, best_move