import time
import collections
import puzzle_helper as pzh


def dfs(puzzle):
    start_time = time.time()
    
    states = [(puzzle, None)]
    vis = set([puzzle])
    
    # Holds state to parent_state mapping (for retracing solution path)
    parents = collections.defaultdict()
    
    search_space = []
    success = False
    
    while states:
        # Check execution time limit
        if time.time() - start_time >= pzh.EXECUTION_TIME_LIMIT:
            break
        
        puzzle, parent = states.pop()
        
        search_space.append(puzzle)
        parents[puzzle] = parent
        
        # Check goal state reached
        if pzh.is_goal_puzzle(puzzle):
            success = True
            break
        
        next_states = pzh.get_next_states(puzzle)
        for state in next_states:
            if state in vis:
                continue
            vis.add(state)
            states.append((state, puzzle))
    
    solution_space = pzh.retrace_solution_path(puzzle, parents, success)

    return success, solution_space, search_space, (time.time() - start_time)


if __name__ == "__main__":
    success, solution, search, _ = dfs(((6,1,2),(7,8,3),(5,4,9)))
    pzh.output("dfs", success, solution, 'solution')
    pzh.output("dfs", success, search, 'search')
