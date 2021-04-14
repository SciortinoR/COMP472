import sys
import math 
import utils

def minimax(token_count, used_token_values, depth, alpha, beta, is_max_turn, metrics):
    metrics["visited"] += 1

    last_used_token = None
    if len(used_token_values) > 0:
        last_used_token = used_token_values[-1]

    available_moves = utils.legal_moves(token_count, used_token_values, last_used_token)

    if depth == 0 or len(available_moves) == 0:
        if metrics["current_depth"] > metrics["max_depth"]:
            metrics["max_depth"] = metrics["current_depth"]

        metrics["current_depth"] = 0
        metrics["evaluated"] += 1

        return utils.static_board_eval(token_count, used_token_values), None

    metrics["branch_count"] += 1

    if is_max_turn:
        max_eval = -math.inf
        best_move = 0

        for move in available_moves:
            metrics["current_depth"] += 1
            metrics["branches"] += 1

            used_token_values.append(move)
            
            eval, _ = minimax(token_count, used_token_values, depth - 1, alpha, beta, False, metrics)
            max_eval = max(alpha, eval)
                
            used_token_values.remove(move)

            if eval > max_eval:
                best_move = move

            if beta <= max(alpha, eval):
                break

        if metrics["current_depth"] > metrics["max_depth"]:
            metrics["max_depth"] = metrics["current_depth"]

        metrics["current_depth"] = 0

        return max_eval, best_move
    else:
        metrics["current_depth"] += 1
        metrics["branches"] += 1

        min_eval = math.inf
        best_move = 0

        for move in available_moves:
            used_token_values.append(move)
            
            eval, _ = minimax(token_count, used_token_values, depth - 1, alpha, beta, True, metrics)
            min_eval = min(beta, eval)
                
            used_token_values.remove(move)

            if eval < min_eval:
                best_move = move

            if min(beta, eval) <= alpha:
                break

        if metrics["current_depth"] > metrics["max_depth"]:
            metrics["max_depth"] = metrics["current_depth"]

        metrics["current_depth"] = 0

        return min_eval, best_move


if __name__ == "__main__":
    token_count = int(sys.argv[1])
    used_token_count = int(sys.argv[2])
    used_token_values = [int(arg) for arg in sys.argv[3:-1]]
    depth = int(sys.argv[-1])

    if depth == 0:
        depth = -1

    is_max_turn = used_token_count % 2 == 0

    metrics = {
        "visited": 0, 
        "evaluated": 0, 
        "max_depth": 0, 
        "current_depth": 0, 
        "branches": 0, 
        "branch_count": 0}

    eval, move = minimax(token_count, used_token_values, depth, -math.inf, math.inf, is_max_turn, metrics);

    if move is None:
        if eval == 1:
            print("Max win")
        else:
            print("Min win")

    visited = metrics["visited"]
    evaluated = metrics["evaluated"]
    max_depth = metrics["max_depth"]

    print(f"Move: {move}")
    print(f"Eval: {eval}")
    print(f"Number of Nodes Visited: {visited}")
    print(f"Number of Nodes Evaluated:  {evaluated}")
    print(f"Max depth reached: {max_depth}")
    print("Average Effective Branching Factor: ", format(metrics["branches"]/metrics["branch_count"], '.1f') if metrics["branch_count"] != 0 else 0)
