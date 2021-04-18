# Assignment 3: Pick Numbered-Tokens Game (PNT-Game)

## Running Instructions:

All scripts must be run using minimum python version 3.7.8.

1. To run a single custom, test case:


```sh
python main.py <number_of_tokens> <number_taken_tokens> <list_taken_tokens> <max_depth>

eg. python main.py 7 2 3 6 0
```
`number_of_tokens`: The total number of tokens in the game  
`number_taken_tokens`: The number of tokens that have already been taken in previous moves.  
`list_taken_tokens`: A sequence of integers indicating the indexes of the already taken tokens, ordered from first to last token taken. 
`max_depth`: The maximum search depth allowed. If max_depth is 0, search to end game states.


2. To run analysis on multiple test cases at once:

Store your testcases line by line in a file named `testcases.txt` and run the following:

```sh
python run_testcases.py
```

Running both a custom test case or multiple test cases from a text file will generate the respective output within the terminal.

eg.
```
Move: 1
Value: -1.0
Number of Nodes Visited: 16
Number of Nodes Evaluated: 8
Max Depth Reached: 4
Avg Effective Branching Factor: 1.9

Execution time: 0.0 seconds
```