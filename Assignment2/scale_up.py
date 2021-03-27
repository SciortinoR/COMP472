import os
import argparse

from random import shuffle

from analysis import run_analysis
from a_star import h2, a_star
from puzzle_helper import write_analysis, extend_puzzles, \
                            make_puzzle_tuples, gen_linear_puzzles


# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--start_size', help='Start size of a puzzle. (eg. 3 (for 3x3), 4 (for 4x4) etc.)',
                    required=True)
parser.add_argument('--end_size', help='End size of a puzzle. Must be greater than start size! (eg. 4 (for 4x4), 5 (for 5x5) etc.)',
                    required=True)
parser.add_argument('--num_puzzles', help='Number of puzzles to generate for each size batch. (eg. 5, 10, 20 etc)',
                    required=True)

args = parser.parse_args()

if int(args.end_size) <= int(args.start_size):
    raise Exception("End size must be larger than start size!")

PUZZLE_START_SIZE = int(args.start_size)
PUZZLE_END_SIZE = int(args.end_size)
NUM_PUZZLES = int(args.num_puzzles)


def run_scale_up(a_type, f, linear_puzzles, algo_set):
    for size in range(PUZZLE_START_SIZE, PUZZLE_END_SIZE+1):
        linear_puzzles, puzzle_tuples = extend_puzzles(linear_puzzles, size)

        run_analysis(a_type, f, puzzle_tuples, algo_set, size, True)


if __name__ == "__main__":
    # Generate puzzles
    puzzles = gen_linear_puzzles(PUZZLE_START_SIZE, NUM_PUZZLES)

    # Algo to test
    algo_set = [('A_Star_H2', a_star, h2)]

    # Open output file
    f = 'outputs//scale_up_analysis.txt'
    os.makedirs(os.path.dirname(f), exist_ok=True)
    f = open(f, 'w')

    # Run scale up analysis
    run_scale_up('scale_up_analysis', f, puzzles, algo_set)
    print(f"Full scale-up analysis completed!")

    f.close()