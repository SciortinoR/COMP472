import sys

if __name__ == "__main__":
    args = sys.argv[1:]

    tokens, taken_tokens_cnt, depth = int(args[0]), int(args[1]), int(args[-1])
    taken_tokens = [int(args[i]) for i in range(2, taken_tokens_cnt + 2)]
    last_move = taken_tokens[-1] if taken_tokens_cnt > 0 else 0

    print(f"Tokens: {tokens}, Taken Tokens: {taken_tokens} (len = {taken_tokens_cnt}), depth: {depth}, last_move: {last_move}\n")
