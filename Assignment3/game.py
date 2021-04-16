import math

def get_possible_moves(N, tokens, last_move, isFirstMove):
    if isFirstMove:
        ceil = int(N / 2) + 1 if N & 1 else int(N / 2)
        return [i for i in range(1, ceil, 2) if i in tokens]

    if last_move == 1:
        return [i for i in range(2, N + 1) if i in tokens]

    factors = get_factors(last_move, tokens)
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
        max_prime = max_prime_factor(N)
        count = len([i for i in range(max_prime, N + 1, max_prime) if i in tokens])
        score = 0.6 if count & 1 else -0.6
    return score if isMaximizingTurn else -score

# Finds all factors of last move
def get_factors(last_move, tokens):
    factors = []
    for n in range(1, int(last_move**(0.5))+1):
        if last_move % n == 0:
            first = n
            second = last_move // n

            if first in tokens:
                factors.append(first)

            if first != second and second in tokens:
                factors.append(second)

    return factors


# Finds largest prime factor of number
def max_prime_factor(n):
    max_prime = n + 1
      
    while n % 2 == 0:
        n >>= 1
          
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            max_prime = i
            n /= i

    if n > 2:
        max_prime = n

    return int(max_prime)


# Detrmines if number is prime
def is_prime(n):
    if (n <= 1) :
        return False
    if (n <= 3) :
        return True

    if (n % 2 == 0 or n % 3 == 0):
        return False
 
    i = 5
    while(i * i <= n) :
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6
 
    return True
