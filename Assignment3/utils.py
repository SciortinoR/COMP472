import math

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
