import time
import collections
import math
import numpy as np


def main():
    #puzzles = create_puzzle_from_input("input.txt")
    input_len = 2
    puzzles = generate_puzzles(3, input_len)

    dfs_length_list = 0
    dfs_no_sol = 0
    dfs_av_ex_time = 0

    id_length_list = 0
    id_no_sol = 0
    id_av_ex_time = 0

    a_length_list = 0
    a_no_sol = 0
    a_av_ex_time = 0

    for puzzle in puzzles:
        print(puzzle)
        dfs_success, dfs_closed_list, dfs_solution_space, dfs_time = depth_first(puzzle)
        dfs_length_list += len(dfs_solution_space)
        if not dfs_success:
            dfs_no_sol += 1
        dfs_av_ex_time += dfs_time

        id_success, id_closed_list, id_solution_space, id_time = iter_deepeneing(puzzle)
        id_length_list += len(id_solution_space)
        if not id_success:
            id_no_sol += 1
        id_av_ex_time += id_time

        astar_success, astar_closed_list, astar_solution_space, astar_time = alg_a(puzzle, 1)
        a_length_list += len(dfs_solution_space)
        if not astar_success:
            a_no_sol += 1
        a_av_ex_time += astar_time

        write_output_file("dfs", dfs_solution_space, dfs_closed_list)
        write_output_file("id", id_solution_space, id_closed_list)
        write_output_file("astar", astar_solution_space, astar_closed_list)

    print("Analysis")
    print("DFS")
    print("Average Length", dfs_length_list/input_len)
    print("Average 'no solution'", dfs_no_sol/input_len)
    print("Average execution time", dfs_av_ex_time/input_len)

    print("ID")
    print("Average Length", id_length_list/input_len)
    print("Average 'no solution'", id_no_sol/input_len)
    print("Average execution time", id_av_ex_time/input_len)

    print("A*")
    print("Average Length", a_length_list/input_len)
    print("Average 'no solution'", a_no_sol/input_len)
    print("Average execution time", a_av_ex_time/input_len)


def create_puzzle_from_input(filename):
    file = open(filename, "r")
    lines = file.readlines()

    list_of_puzzles = []

    for line in lines:
        # Create 2d list for puzzle
        list_2d = []
        rows = line.split(");")

        for row_str in rows:
            # Remove unwanted characters
            row_str = row_str.replace('(', '')
            row_str = row_str.replace(' ', '')
            row_str = row_str.replace(')', '')

            # Convert string to array of int
            row = row_str.split(";")
            row = tuple(map(int, row))

            # Add row to list
            list_2d.append(row)

        tuple_2d = tuple(list_2d)
        print(tuple_2d)
        list_of_puzzles.append(tuple_2d)
    return list_of_puzzles


def depth_first(puzzle):
    begin = time.time()

    open_list = [(puzzle, None)]
    closed_list = set([puzzle])
    success = False
    parents = collections.defaultdict()

    while open_list:
        # Check execution time limit
        if time.time() - begin >= 60:
            break

        puzzle, parent = open_list.pop()

        # Check for goal state
        if check_goal_state(puzzle):
            success = True
            parents[puzzle] = parent
            break

        closed_list.add(puzzle)
        parents[puzzle] = parent

        possible_states = get_next_states(puzzle)
        for state in possible_states:
            if state in closed_list:
                continue
            closed_list.add(state)
            open_list.append((state, puzzle))

    solution_space = get_solution_path(puzzle, parents, success)

    return success, closed_list, solution_space, (time.time() - begin)


def iter_deepeneing(puzzle):
    begin = time.time()
    success = False
    max_depth = 1
    current_depth = 0
    limit = 100000
    parents = collections.defaultdict()

    while max_depth < limit:
        open_list = [(puzzle, None)]
        closed_list = set([puzzle])

        while open_list:
            # Check execution time limit
            if time.time() - begin >= 60:
                max_depth = 200000
                break

            puzzle, parent = open_list.pop()

            # Check for goal state
            if check_goal_state(puzzle):
                success = True
                max_depth = 200000
                parents[puzzle] = parent
                break

            closed_list.add(puzzle)
            parents[puzzle] = parent

            if current_depth < max_depth:
                current_depth += 1
                possible_states = get_next_states(puzzle)
                for state in possible_states:
                    if state in closed_list:
                        continue
                    closed_list.add(state)
                    open_list.append((state, puzzle))

        current_depth = 0
        max_depth += 1

    solution_space = get_solution_path(puzzle, parents, success)

    return success, closed_list, solution_space, (time.time() - begin)


def alg_a(puzzle, heuristic):
    begin = time.time()

    open_list = [(1, puzzle, None)]
    closed_list = set([puzzle])
    success = False
    parents = collections.defaultdict()

    while open_list:
        # Check execution time limit
        if time.time() - begin >= 60:
            break

        priority, puzzle, parent = open_list.pop()

        # Check for goal state
        if check_goal_state(puzzle):
            parents[puzzle] = parent
            success = True
            break

        closed_list.add(puzzle)
        parents[puzzle] = parent

        possible_states = get_next_states(puzzle)
        for state in possible_states:
            if state in closed_list:
                continue
            closed_list.add(state)
            priority = get_puzzle_priority(puzzle, heuristic)

            # adding puzzle with priority
            open_list.append((priority, state, puzzle))
            open_list.sort(reverse=True)

    solution_space = get_solution_path(puzzle, parents, success)

    return success, closed_list, solution_space, (time.time() - begin)


def get_puzzle_priority(puzzle, heuristic):
    result = 0

    # hamming distance
    if heuristic == 0:
        prev = 0
        result = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if puzzle[i][j] != prev + 1:
                    result += 1
                prev += 1

        return result

    # manhattan distance
    else:
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                current_val = puzzle[i][j]
                correct_i = math.ceil(current_val/len(puzzle))
                correct_j = current_val % len(puzzle)
                if correct_j == 0:
                    correct_j = 3

                manhattan_distance = abs(correct_i - i) + abs(correct_j - j)
                result += manhattan_distance
        return result


def check_goal_state(puzzle):
    prev = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != prev + 1:
                return False
            prev += 1
    return True


def get_next_states(puzzle):
    next_states = []

    # All horizontal swaps
    for i in range(len(puzzle)):
        row = puzzle[i]
        for j in range(len(puzzle) - 1):
            new_row = row[:j] + (row[j + 1],) + (row[j],) + row[j + 2:]
            state = puzzle[:i] + (new_row,) + puzzle[i + 1:]
            next_states.append(state)

    # All vertical swaps
    for i in range(len(puzzle) - 1):
        row1 = puzzle[i]
        row2 = puzzle[i + 1]
        for j in range(len(puzzle)):
            new_row1 = row1[:j] + (row2[j],) + row1[j + 1:]
            new_row2 = row2[:j] + (row1[j],) + row2[j + 1:]
            state = puzzle[:i] + (new_row1,) + (new_row2,) + puzzle[i + 2:]
            next_states.append(state)

    return next_states


def get_solution_path(puzzle, parents, success):
    if not success:
        return "No solution"

    sol_path = []
    while puzzle is not None:
        sol_path.append(puzzle)
        puzzle = parents[puzzle]

    return sol_path


def generate_puzzles(dimension, size):
    puzzle_list = []

    for i in range(size):
        array = np.arange(1, pow(dimension, 2) + 1)
        np.random.shuffle(array)
        array = array.reshape(3, 3)

        tuple_puzzle = tuple(map(tuple, array))
        puzzle_list.append(tuple_puzzle)

    return puzzle_list


def write_output_file(alg_name, solution_path, search_path):
    sol_filename = alg_name + "-solution_space.txt"
    sol_file = open(sol_filename, "a")
    sol_file.write(str(solution_path))

    search_filename = alg_name + "-search_space.txt"
    search_file = open(search_filename, "a")
    search_file.write(str(search_path))


if __name__ == "__main__":
    main()
