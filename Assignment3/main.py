import sys
import time
from minmax import alpha_beta_search
from analysis import run_analysis

def print_results(move, value, stats):
    print(f"Move: {move}")
    print(f"Value: {value}")
    print(f'Number of Nodes Visited: {stats["visited_nodes"]}')
    print(f'Number of Nodes Evaluated: {stats["evaluated_nodes"]}')
    print(f'Max Depth Reached: {stats["depth_reached"]}')
    average_branching = float("{:.1f}".format(stats["branches"] / stats["parents"] if stats["parents"] != 0 else 0.0))
    print(f'Avg Effective Branching Factor: {average_branching}')

    print(f'Total time elapsed: {stats["time_elapsed"]}')

if __name__ == "__main__":
    args = sys.argv[1:]

    # If no args are provided, we run the analysis
    if not args:
        for test_stat in run_analysis("./testcases.txt"):
            case, score, move, stats = test_stat
            print(f"{case}\n")
            print_results(move, score, stats)
            print("-" * 50)
        exit()

    tokens, taken_tokens_cnt, depth = int(args[0]), int(args[1]), int(args[-1])
    taken_tokens = [int(args[i]) for i in range(2, taken_tokens_cnt + 2)]
    last_move = taken_tokens[-1] if taken_tokens_cnt > 0 else 0
    print(f"Token Count: {tokens}, Taken Tokens: {taken_tokens} (len = {taken_tokens_cnt}), depth: {depth}, last_move: {last_move}\n")

    start_time = time.time()
    score, move, stats = alpha_beta_search(tokens, taken_tokens, depth, last_move, taken_tokens_cnt % 2 == 0)
    stats["time_elapsed"] = f"{time.time() - start_time}s"
    print_results(move, score, stats)

