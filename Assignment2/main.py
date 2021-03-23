import dfs

if __name__ == "__main__":  
    input = [
        [1, 2, 3],
        [4, 5, 6], 
        [7, 9, 8]]

    print(dfs.depth_first_search(input_puzzle=input))
