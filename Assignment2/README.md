# Assignment 2: S-Puzzle Search Algorithms

## Running Instructions:

All scripts must be run using minimum version python 3.7.8.

1. To run each algorithm individually on the example puzzle provided in the assignment:


```sh
python <algo_name>.py
eg. python dfs.py
```
This will generate files containing the entire solution and search space and place them in an `outputs` folder. (eg. `<algo_name>_solution_path.txt` & `<algo_name>_search_path.txt`)


2. To run analysis on all algos using 20 random 3x3 puzzles:

```sh
python analysis.py
```

This will automatically generate 20 random puzzles and save them to a file named `puzzles.txt`. If the puzzles text file already exists, it will use the puzzles within that file instead of generating new ones. 

Running the analysis will generate a file `outputs/analysis.txt`, compiling all the data and results from the analysis run. Solution and search paths will also be generated for each algo and each puzzle and will be stored within the `outputs/analysis_paths/` folder.

3. To run analysis on the most performant algo on scaled up versions of the S-Puzzle (eg. 4x4, 5x5 etc.):

```sh
python scale_up.py --start_size=<integer> --end_size==<integer> --num_puzzles=<integer>
```

In our case, the most performant algorithm was the A* H2 variant. Running scale up will automatically and randomly generate the amount of puzzles specified by the `num_puzzles` parameter. The puzzles will start off with `start_size` length specified and will scale up to the `end_size` length specified (End size must be greater than start size). 

Running scale up will generate a file `outputs/scale_up_analysis.txt`, compiling all the data and results from the scale up analysis run. Solution and search paths will also be generated for each puzzle and will be stored within the `outputs/scale_up_analysis_paths/` folder.