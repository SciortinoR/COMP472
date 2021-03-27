import os

from dfs import dfs
from a_star import h1, h2, a_star
from id_dfs import iterative_deepening
from puzzle_helper import generate_puzzles, make_puzzle_tuples, write_analysis, output, write_optimality


PUZZLE_SIZE = 3
NUM_PUZZLES = 20


def analyze(a_type, puzzles, algo, heuristic, name, opt_results, skip_time):
    tot_no_sol = 0
    tot_ex_time = 0
    tot_sol_p_l = 0
    tot_search_p_l = 0

    n = len(puzzles)
    size = len(puzzles[0])
    for i, p in enumerate(puzzles):
        print(f"Running puzzle {i+1}...")

        solution_space, search_space, execution_time, success = algo(p, heuristic, skip_time)

        if a_type == 'analysis' and opt_results[i][1] > execution_time:
            opt_results[i] = (name, execution_time)
            
        tot_no_sol += not success
        tot_ex_time += execution_time
        tot_sol_p_l += len(solution_space)
        tot_search_p_l += len(search_space)
        
        output(f'{a_type}_paths//{name}_{size}x{size}_{i+1}', success, solution_space, 'solution')
        output(f'{a_type}_paths//{name}_{size}x{size}_{i+1}', success, search_space, 'search')

    return tot_sol_p_l, tot_search_p_l, tot_ex_time, tot_no_sol, tot_sol_p_l / n, \
            tot_search_p_l / n, tot_ex_time / n, tot_no_sol / n


# Run each algo and collect stats on set of puzzles
def run_analysis(a_type, f, puzzles, algo_set, puzzle_size, skip_time=False):
    n = len(puzzles)
    opt_results = [(None, float('inf'))]*n

    for name, algo, h in algo_set:
        print(f'Running {a_type} on {name} with {n} puzzles of size {puzzle_size}x{puzzle_size}...')
        out = analyze(a_type, puzzles, algo, h, name, opt_results, skip_time)
        write_analysis(f, out, name, n, puzzle_size)

    write_optimality(a_type, f, opt_results)


if __name__ == "__main__":
    puzzles = []

    # Generate or Load puzzles
    if os.path.isfile('puzzles.txt'):
        with open('puzzles.txt', 'r') as f:
            puzzles.extend(make_puzzle_tuples(PUZZLE_SIZE, l.strip().split()) for l in f)
    else:
        puzzles = generate_puzzles(PUZZLE_SIZE, NUM_PUZZLES)
    
    # Algo set to test
    algo_set = [('DFS', dfs, None), ('ID_DFS', iterative_deepening, None), \
                ('A_Star_H1', a_star, h1), ('A_Star_H2', a_star, h2)]

    # Open output file
    f = 'outputs//analysis.txt'
    os.makedirs(os.path.dirname(f), exist_ok=True)
    f = open(f, 'w')

    # Run Analysis
    run_analysis('analysis', f, puzzles, algo_set, PUZZLE_SIZE)
    print(f"Full analysis completed!")

    f.close()