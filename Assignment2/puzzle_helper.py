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
    prev = 0
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if puzzle[row][col] != prev + 1:
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


# Displays puzzle nicely in output file
def write_puzzle(file, state):
    for i in range(len(state)):
        file.write(str(state[i])+'\n')
    file.write('\n')


# Write output to file
def output(filename, success, out, out_name):
    with open(filename+f'_{out_name}_path', 'w') as f:
        if not success:
            f.write("No solution found")
        else:
            f.write(f'{out_name} path ({len(out) - 1} iterations): \n\n')
            for item in out:
                if type(item) == str:
                    f.write(item)
                write_puzzle(f, item)
    f.close()


# Generates puzzles
def generate_puzzles(size, num_puzzles):
    puzzles = []
    p = [str(i+1) for i in range(size**2)]

    for _ in range(num_puzzles):
        shuffle(p)
        puzzles.append(' '.join(p))
    
    return puzzles


if __name__ == "__main__":
    puzzles = generate_puzzles(3, 20)
    with open("puzzles", 'w') as f:
        for p in puzzles:
            f.write(p+'\n')
    
    f.close()