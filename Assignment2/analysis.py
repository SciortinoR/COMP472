import os.path

from dfs import dfs
from a_star import h1, h2, a_star
from id_dfs import iterative_deepening
from puzzle_helper import generate_puzzles, make_puzzle_tuples, write_analysis


PUZZLE_SIZE = 3
NUM_PUZZLES = 20


def analyze(puzzles, algo, heuristic, skip_time):
    tot_no_sol = 0
    tot_ex_time = 0
    tot_sol_p_l = 0
    tot_search_p_l = 0

    n = len(puzzles)
    for i, p in enumerate(puzzles, 1):
        print(f"Running puzzle {i}...")
        solution_space, search_space, execution_time, success = algo(p, heuristic, skip_time)

        tot_no_sol += not success
        tot_ex_time += execution_time
        tot_sol_p_l += len(solution_space) - 1
        tot_search_p_l += len(search_space) - 1

    return tot_sol_p_l, tot_search_p_l, tot_ex_time, tot_no_sol, tot_sol_p_l / n, \
            tot_search_p_l / n, tot_ex_time / n, tot_no_sol / n


# Run each algo and collect stats on set of puzzles
def run_analysis(a_type, f, puzzles, algo_set, puzzle_size, skip_time=False):
    n = len(puzzles)

    for name, algo, h in algo_set:
        print(f'Running {a_type} on {name} with {n} puzzles of size {puzzle_size}x{puzzle_size}...')
        write_analysis(f, analyze(puzzles, algo, h, skip_time), name, n, puzzle_size)


if __name__ == "__main__":
    puzzles = []

    # Generate puzzles
    puzzles, _ = generate_puzzles(PUZZLE_SIZE, NUM_PUZZLES)
    
    # Algo set to test
    algo_set = [('DFS', dfs, None), ('ID DFS', iterative_deepening, None), \
                ('A_Star_H1', a_star, h1), ('A_Star_H2', a_star, h2)]

    f = open('analysis', 'w')
    run_analysis('analysis', f, puzzles, algo_set, PUZZLE_SIZE)
    print(f"Full analysis completed!")
    f.close()




