import os
from random import shuffle


EXECUTION_TIME_LIMIT = 60

# Get next puzzle states
def get_next_states(puzzle):
    next_states = []
    
    # All horizontal swaps
    for i in range(len(puzzle)):
        row = puzzle[i]
        for j in range(len(puzzle)-1):
            new_row = row[:j] + (row[j+1],) + (row[j],) + row[j+2:]
            state = puzzle[:i] + (new_row,) + puzzle[i+1:]
            next_states.append(state)
    
    # All vertical swaps
    for i in range(len(puzzle)-1):
        row1 = puzzle[i]
        row2 = puzzle[i+1]
        for j in range(len(puzzle)):
            new_row1 = row1[:j] + (row2[j],) + row1[j+1:]
            new_row2 = row2[:j] + (row1[j],) + row2[j+1:]
            state = puzzle[:i] + (new_row1,) + (new_row2,) + puzzle[i+2:]
            next_states.append(state)
    
    return next_states


# Check goal puzzle
def is_goal_puzzle(puzzle):
    prev = 1
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != prev:
                return False
            prev += 1
    return True


# Outlines solution space from beginning to end
def retrace_solution_path(puzzle, parents, success):
    if not success:
        return []

    solution_space = []
    while puzzle is not None:
        solution_space.append(puzzle)
        puzzle = parents[puzzle]
    
    solution_space.reverse()
    return solution_space


# Write optimality results to file
def write_optimality(a_type, f, opt_results):
    if a_type == 'analysis':
        f.write("Optimality results (Fastest algo on each puzzle):\n")
        for i, (name, time) in enumerate(opt_results, 1):
            f.write(f"{i}. {name}: {time} seconds\n")
        f.write('\n')


# Write full analyis to file
def write_analysis(f, out, name, num_puzzles, size):
    tot_sol_p_l, tot_search_p_l, tot_ex_time, tot_no_sol, \
        av_sol_p_l, av_search_p_l, av_ex_time, av_no_sol = out

    f.write(f"Performance of {name} on random set of {num_puzzles} puzzle(s) of size {size}x{size}:\n")
    f.write(f"Total solution path length: {tot_sol_p_l} states\n")
    f.write(f"Total search path length: {tot_search_p_l} states\n")
    f.write(f"Total cost: {tot_sol_p_l-1} iterations\n")
    f.write(f"Total execution time: {tot_ex_time} seconds\n")
    f.write(f"Total no solution: {tot_no_sol}\n")
    f.write(f"Average solution path length: {av_sol_p_l} states\n")
    f.write(f"Average search path length: {av_search_p_l} states\n")
    f.write(f"Average cost: {av_sol_p_l-1} iterations\n")
    f.write(f"Average execution time: {av_ex_time} seconds\n")
    f.write(f"Average no solution: {av_no_sol}\n")
    f.write('\n')


# Displays puzzle nicely in output file
def write_puzzle(file, state):
    for i in range(len(state)):
        file.write(str(state[i])+'\n')
    file.write('\n')


# Write output to file
def output(filename, success, out, out_name):
    filename = f'outputs//{filename}_{out_name}_path.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        if not success:
            f.write("No solution found")
        else:
            f.write(f'{out_name} path ({len(out) - 1} iterations): \n\n')
            for item in out:
                if type(item) == str:
                    f.write(item)
                else:
                    write_puzzle(f, item)
    f.close()


# Extends puzzles for scale-up
def extend_puzzles(puzzles, size):
    n = len(puzzles)
    puzzle_tuples = []
    for i in range(n):
        puzzles[i] += [j+1 for j in range(len(puzzles[i]), size**2)]
        shuffle(puzzles[i])
        puzzle_tuples.append(make_puzzle_tuples(size, puzzles[i]))
    
    return puzzles, puzzle_tuples


# Generates puzzles
def generate_puzzles(size, num_puzzles):
    puzzles = []

    p = [str(i+1) for i in range(size**2)]
    with open("puzzles.txt", 'w') as f:
        for _ in range(num_puzzles):
            shuffle(p)
            f.write(' '.join(p)+'\n')
            puzzles.append(make_puzzle_tuples(size, p))
    f.close()

    return puzzles


# Generate linear puzzles for scale up
def gen_linear_puzzles(size, num_puzzles):
    puzzles = []
    p = [str(i+1) for i in range(size**2)]
    
    for _ in range(num_puzzles):
        shuffle(p)
        puzzles.append(list(map(int, p)))

    return puzzles


# Makes tuples of string puzzle
def make_puzzle_tuples(size, puzzle):
    i = 0
    res = []
    for _ in range(size):
        res.append(tuple(map(int, [puzzle[j] for j in range(i, i+size)])))
        i += size

    return tuple(res)