import time
import collections
import puzzle_helper as pzh


def iterative_deepening(puzzle, heuristic=None, skip_time=False):
    start_time = time.time()
    
    full_search_space = []
    solution_space = []
    success = False
    
    limit = 0
    while True:
        # Check execution time limit
        if not skip_time and time.time() - start_time >= pzh.EXECUTION_TIME_LIMIT:
            break
        
        success, solution_space, search_space, max_depth_seen = id_dfs(puzzle, limit, start_time, skip_time)
        
        full_search_space.append(f"DFS Limit {limit}: \n\n")
        full_search_space += search_space
        
        # Goal found or entire search space explored
        if success or max_depth_seen < limit:
            break

        limit += 1
    
    return solution_space, full_search_space, time.time() - start_time, success
    
    
def id_dfs(puzzle, limit, start_time, skip_time):
    states = [(puzzle, None, 0)]
    
    # Holds state to parent_state mapping (for retracing solution path)
    parents = collections.defaultdict()
    
    # Holds visited to depth mapping
    vis_depth = collections.defaultdict(None)
    
    search_space = []
    success = False
    
    max_depth_vis = 0
    vis_depth[puzzle] = 0

    while states:
        # Check execution time limit
        if not skip_time and time.time() - start_time >= pzh.EXECUTION_TIME_LIMIT:
            break
        
        puzzle, parent, depth = states.pop()
        
        max_depth_vis = max(max_depth_vis, depth)
        
        search_space.append(puzzle)
        parents[puzzle] = parent
        
        # Check goal state reached
        if pzh.is_goal_puzzle(puzzle):
            success = True
            break
        
        next_depth = depth + 1
        if next_depth <= limit:
            next_states = pzh.get_next_states(puzzle)
            for state in next_states:
                state_depth = vis_depth[state] if state in vis_depth else None
                if state_depth is not None and state_depth <= next_depth:
                    continue
                
                vis_depth[state] = next_depth
                states.append((state, puzzle, next_depth))
    
    solution_space = pzh.retrace_solution_path(puzzle, parents, success)
        
    return success, solution_space, search_space, max_depth_vis


if __name__ == "__main__":
    print(f"Running Iterative Deepening DFS on test puzzle ((6,1,2),(7,8,3),(5,4,9))...")
    solution, search, _, success = iterative_deepening(((6,1,2),(7,8,3),(5,4,9)))
    pzh.output("id_dfs", success, solution, 'solution')
    pzh.output("id_dfs", success, search, 'search')
    print('Done!')