import sys
import math


def main():
    # Get info from user input
    sys.argv.remove(sys.argv[0])
    args = list(map(int, sys.argv))
    token_number = args[0]
    num_taken_tokens = args[1]
    taken_token_list = []

    for i in range(2, len(args)-1):
        taken_token_list.append(args[i])

    depth = sys.argv[len(sys.argv)-1]

    # Check whose turn it is
    if num_taken_tokens % 2 == 0:
        is_max_turn = True
    else:
        is_max_turn = False

    if int(depth) == 0:
        depth = -1

    # Play the game
    play_game(token_number, taken_token_list, int(depth), is_max_turn)


def play_game(token_number, taken_token_list, depth, is_max_turn):
    metric_dict = {"visited": 0, "evaluated": 0, "max_depth": 0, "current_depth": 0, "branches": 0, "branch_count": 0}
    value, move = alpha_beta_prune(token_number, taken_token_list, depth, -math.inf, math.inf, is_max_turn, metric_dict)

    if move is None:
        if value == 1:
            print("Max wins")
        else:
            print("Min wins")

    print("Move: ", move)
    print("Value: ", value)
    print("Number of Nodes Visited: ", metric_dict["visited"])
    print("Number of Nodes Evaluated: ", metric_dict["evaluated"])
    print("Max depth reached: ", metric_dict["max_depth"])
    print("Average Effective Branching Factor: ", format(metric_dict["branches"]/metric_dict["branch_count"], '.1f') if metric_dict["branch_count"] != 0 else 0)


def alpha_beta_prune(token_number, taken_tokens, depth, alpha, beta, is_max_turn, metrics):
    metrics["visited"] += 1

    # Get last node and possible moves from there
    last_token = taken_tokens[-1] if len(taken_tokens) > 0 else None
    possible_moves = legal_moves(token_number, taken_tokens, last_token)

    if depth == 0 or len(possible_moves) == 0:
        if metrics["current_depth"] > metrics["max_depth"]:
            metrics["max_depth"] = metrics["current_depth"]

        metrics["current_depth"] = 0
        metrics["evaluated"] += 1

        return static_board_eval(token_number, taken_tokens), None

    # In non terminal node
    metrics["branch_count"] += 1

    if is_max_turn:
        value = -math.inf
        best_move = 0
        best_value = -math.inf

        for move in possible_moves:
            # Update metrics
            metrics["current_depth"] += 1
            metrics["branches"] += 1

            taken_tokens.append(move)
            val, _ = alpha_beta_prune(token_number, taken_tokens, depth - 1, alpha, beta, False, metrics)
            value = max(value, val)
            alpha = max(alpha, value)
            taken_tokens.remove(move)

            if value > best_value:
                best_value = value
                best_move = move

            if alpha >= beta:
                break

        if metrics["current_depth"] > metrics["max_depth"]:
            metrics["max_depth"] = metrics["current_depth"]

        metrics["current_depth"] = 0

        return value, best_move

    else:
        value = math.inf
        best_move = 0
        best_value = math.inf

        for move in possible_moves:
            # Update metrics
            metrics["current_depth"] += 1
            metrics["branches"] += 1

            taken_tokens.append(move)
            val, _ = alpha_beta_prune(token_number, taken_tokens, depth - 1, alpha, beta, True, metrics)
            value = min(value, val)
            beta = min(beta, value)
            taken_tokens.remove(move)

            if value < best_value:
                best_value = value
                best_move = move

            if beta <= alpha:
                break

        if metrics["current_depth"] > metrics["max_depth"]:
            metrics["max_depth"] = metrics["current_depth"]

        metrics["current_depth"] = 0

        return value, best_move


def static_board_eval(token_number, taken_token_list):
    if not taken_token_list:
        moves = legal_moves(token_number, taken_token_list, None)
    else:
        moves = legal_moves(token_number, taken_token_list, taken_token_list[-1])

    # Max turn
    if len(taken_token_list) % 2 == 0:
        if not moves:
            return -1.0
        if 1 not in taken_token_list:
            return 0
        if taken_token_list[-1] == 1:
            move_list = legal_moves(token_number, taken_token_list, 1)
            if len(move_list) % 2 == 0:
                return -0.5
            else:
                return 0.5
        if is_prime(taken_token_list[-1]):
            move_count = count_prime_multiple_moves(token_number, taken_token_list, taken_token_list[-1])
            if move_count % 2 == 0:
                return -0.7
            else:
                return 0.7
        else:
            largest_prime = max_prime_factor(taken_token_list[-1])
            move_count = count_prime_multiple_moves(token_number, taken_token_list, largest_prime)
            if move_count % 2 == 0:
                return -0.6
            else:
                return 0.6
    # Min turn
    else:
        if not moves:
            return 1.0
        if 1 not in taken_token_list:
            return 0
        if taken_token_list[-1] == 1:
            move_list = legal_moves(token_number, taken_token_list, 1)
            if len(move_list) % 2 == 0:
                return 0.5
            else:
                return -0.5
        if is_prime(taken_token_list[-1]):
            move_count = count_prime_multiple_moves(token_number, taken_token_list, taken_token_list[-1])
            if move_count % 2 == 0:
                return 0.7
            else:
                return -0.7
        else:
            largest_prime = max_prime_factor(taken_token_list[-1])
            move_count = count_prime_multiple_moves(token_number, taken_token_list, largest_prime)
            if move_count % 2 == 0:
                return 0.6
            else:
                return -0.6


def is_prime(num):
    if num > 1:
        for i in range(2, int(num / 2) + 1):
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False


def max_prime_factor(n):
    max_prime = -1

    while n % 2 == 0:
        max_prime = 2
        n >>= 1

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            max_prime = i
            n = n / i

    if n > 2:
        max_prime = n

    return int(max_prime)


def count_prime_multiple_moves(token_number, taken_token_list, prime_number):
    legal_move_list = []
    prime_multiple = 1
    current_token = prime_multiple * prime_number

    while current_token <= token_number:
        if current_token not in taken_token_list:
            legal_move_list.append(current_token)

        prime_multiple += 1
        current_token = prime_multiple * prime_number
    return len(legal_move_list)


def legal_moves(token_number, taken_token_list, last_token):
    legal_move_list = []

    if taken_token_list:
        token_multiple = 1
        current_token = last_token * token_multiple

        for i in range(1, last_token):
            if i not in taken_token_list and last_token % i == 0:
                legal_move_list.append(i)

        while current_token <= token_number:
            if current_token not in taken_token_list:
                legal_move_list.append(current_token)

            token_multiple += 1
            current_token = last_token * token_multiple

    else:
        first_move_max = token_number/2
        first_move_max = math.ceil(first_move_max)
        for i in range(1, int(first_move_max)):
            if i % 2 != 0:
                legal_move_list.append(i)

    return legal_move_list


if __name__ == "__main__":
    main()
