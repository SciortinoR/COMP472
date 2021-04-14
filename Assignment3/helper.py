import math


# Gets next token removals
def get_next_removals(n_tokens, n_taken_tokens, taken_tokens, last_move):
    if n_taken_tokens == 0:
        return [i for i in range(1, (n_tokens+1)//2, 2)]

    return get_factors(last_move, taken_tokens) + get_multiples(last_move, n_tokens, taken_tokens)


# Gets all multiples of last move
def get_multiples(last_move, n_tokens, taken_tokens):
    multiples = []
    for i in range(last_move*2, n_tokens+1, last_move):
        if not taken_tokens[i]:
            multiples.append(i)

    return multiples


# Finds all factors of last move
def get_factors(last_move, taken_tokens):
    factors = []
    for n in range(1, int(last_move**(0.5))+1):
        if last_move % n == 0:
            first = n
            second = last_move // n

            if not taken_tokens[first]:
                factors.append(first)

            if first != second and not taken_tokens[second]:
                factors.append(second)

    return factors


# Finds largest prime factor of number
def max_prime_factor(n):
    max_prime = -1
      
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

    if (n % 2 == 0 or n % 3 == 0) :
        return False
 
    i = 5
    while(i * i <= n) :
        if (n % i == 0 or n % (i + 2) == 0) :
            return False
        i = i + 6
 
    return True


# Static Board Evaluation
def board_eval(last_move, taken_tokens, next_removals, is_max_turn):
    res = 0.0
    
    if len(next_removals) == 0:
        res = -1.0
    elif not taken_tokens[1]:
        res = 0.0
    elif last_move == 1:
        res = 0.5 if len(next_removals)%2 != 0 else -0.5
    elif is_prime(last_move):
        # 1 is already taken, and last move is prime, therefore next removals are only multiples
        res = 0.7 if len(next_removals) % 2 != 0 else -0.7
    else:
        num_multiples = 0
        max_prime = max_prime_factor(last_move)

        for num in next_removals:
            if num % max_prime == 0:
                num_multiples += 1

        res = 0.6 if num_multiples % 2 != 0 else -0.6

    return res if is_max_turn else -res

# Prints all stats
def print_stats(best_move, value, stats):
    print(f'Move: {best_move}')
    print(f'Value: {value}')
    print(f"Number of Nodes Visited: {stats['nodes_vis']}")
    print(f"Number of Nodes Evaluated: {stats['nodes_eval']}")
    print(f"Max Depth Reached: {stats['max_depth']}")
    print(f"Avg Effective Branching Factor: {0 if len(stats['branching_factors']) == 0 else sum(stats['branching_factors']) / len(stats['branching_factors']):.1f}\n")
    print(f"Execution time: {stats['end_time'] - stats['start_time']} seconds")