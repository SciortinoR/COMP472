import time
from minmax import alpha_beta_search

def run_analysis(testfile):
    test_cases = parse_test_file(testfile)

    test_case_stats = []
    for case in test_cases:
        tokens, taken_tokens, depth, last_move = case
        start_time = time.time()
        score, move, stats = alpha_beta_search(tokens, taken_tokens, depth, last_move, len(taken_tokens) % 2 == 0)
        stats["time_elapsed"] = f"{time.time() - start_time}s"
        
        test_case_stats.append((case, score, move, stats))
    return test_case_stats

def parse_test_file(testfile):
    test_cases = []
    with open(testfile, 'r') as f:
        for line in f:
            line = line.split()
            tokens, taken_tokens_cnt, depth = int(line[0]), int(line[1]), int(line[-1])
            taken_tokens = [int(line[i]) for i in range(2, taken_tokens_cnt + 2)]
            last_move = taken_tokens[-1] if taken_tokens_cnt > 0 else 0

            test_cases.append((tokens, taken_tokens, depth, last_move))
    return test_cases