import dfs
import a_star
import generator 

if __name__ == "__main__":  
    
    for puzzle in generator.generate_puzzles():
        for traceback in reversed(dfs.depth_first_search(input_puzzle=puzzle)):
            print(traceback)

        a_star.a_star(input_puzzle=puzzle)
