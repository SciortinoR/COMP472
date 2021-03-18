from random import shuffle

from analysis import run_analysis
from a_star import h2, a_star
from puzzle_helper import write_analysis, extend_puzzles, \
                            make_puzzle_tuples, generate_puzzles


PUZZLE_START_SIZE = 3
PUZZLE_END_SIZE = 6
NUM_PUZZLES = 20


def run_scale_up(a_type, f, linear_puzzles, algo_set):
    for size in range(PUZZLE_START_SIZE, PUZZLE_END_SIZE+1):
        linear_puzzles, puzzle_tuples = extend_puzzles(linear_puzzles, size)

        run_analysis(a_type, f, puzzle_tuples, algo_set, size, True)


if __name__ == "__main__":
    # Generate puzzles
    _, linear_puzzles = generate_puzzles(PUZZLE_START_SIZE, NUM_PUZZLES)

    algo_set = [('A_Star_H2', a_star, h2)]

    f = open('scale_up_analysis', 'w')
    run_scale_up('scale-up analysis', f, linear_puzzles, algo_set)
    print(f"Full scale-up analysis completed!")
    f.close()