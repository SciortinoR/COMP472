# Assignment 2: S-Puzzle Search Algorithms

## Running Instructions:

All scripts must be run using minimum version python 3.7.8.

1. To run each algorithm individually on the example puzzle provided in the assignment:


```sh
python <algo_name>.py
eg. python dfs.py
```
This will generate files containing the entire soltuion and search space. (eg. `<algo_name>_solution_path` & `<algo_name>_search_path`)


2. To run analysis on all algos using 20 random 3x3 puzzles:

```sh
python analysis.py
```

This will automatically generate 20 random puzzles and save them to a file named `puzzles`. This will also generate a file named `analysis` compiling all the data and results from the analysis run.

3. To run analysis on the most performant algo on a scaled up version of the S-Puzzle (eg. 4x4, 5x5 etc.):

```sh
python scale_up.py
```

In our case, the most performant algorithm was the A* H2 variant. Running scale up will automatically generate 20 random 3x3 puzzles and will extend incrementally up to 6x6. This will also generate a file named `scale_up_analysis` compiling all the data and results from the scale up analysis run.