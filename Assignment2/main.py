import dfs
import generator 

if __name__ == "__main__":  
    
    for puzzle in generator.generate_puzzles():
        dfs.depth_first_search(input_puzzle=puzzle)
