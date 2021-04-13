import math

def get_possible_moves(N, tokens, last_move, isFirstMove):
    if isFirstMove:
        ceil = int(N / 2) + 1 if N & 1 else int(N / 2)
        return [i for i in range(1, ceil) if i & 1 and i in tokens]

    if last_move == 1:
        return [i for i in range(2, N + 1) if i in tokens]

    factors = [i for i in range(1, last_move + 1) if i in tokens and not last_move % i]
    multiples = [i for i in range(last_move * 2, N + 1, last_move) if i in tokens]

    return factors + multiples


def evaluate_board(N, tokens, last_move, isMaximizingTurn):
    if not tokens:
        return -1.0 if isMaximizingTurn else 1.0
    if 1 in tokens:
        return 0.0

    if last_move == 1:
        score = 0.5 if len(tokens) & 1 else -0.5
    elif is_prime(last_move):
        count = len([i for i in range(last_move * 2, N + 1, last_move) if i in tokens])
        score = 0.7 if count & 1 else -0.7
    else:
        max_prime = N + 1
        for i in range(last_move - 1, 0, -1):
            if not last_move % i and is_prime(i):
                max_prime = i
                break
        count = len([i for i in range(max_prime, N + 1, max_prime) if i in tokens])
        score = 0.6 if count & 1 else -0.6
    return score if isMaximizingTurn else -score


def is_prime(n):
    if n < 2:
        return False
        
    i = 2
    while i * i <= n:
        if not n % i:
            return False
        i += 1
    return True
