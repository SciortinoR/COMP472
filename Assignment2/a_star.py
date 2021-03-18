import time
import heapq
import collections
import puzzle_helper as pzh


# Heuristic 1: Returns number of positions out of place in puzzle
def h1(puzzle):
    val = 1
    count = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != val:
                count += 1
            val += 1
    return count


# Heuristic 2: Returns the Manhattan distance of passed state 
# (sum of all the distances by which positions are out of place)
def h2(puzzle):
    s = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            val = puzzle[i][j]
            real_row = (val-1) // len(puzzle)
            real_col = (val-1) % len(puzzle)
            m_dist = abs(i-real_row) + abs(j-real_col)
            s += m_dist
    return s


def a_star(puzzle, heuristic, skip_time=False):
    start_time = time.time()

    # Min-Heap storing (f_cost, g_cost, parent, state)
    heap = []
    heapq.heappush(heap, (0, 0, None, puzzle))
    
    # Holds state to parent_state mapping (for retracing solution path)
    parents = collections.defaultdict()
    
    search_space = []
    success = False
    vis = set()

    while heap:
        if not skip_time and time.time() - start_time >= pzh.EXECUTION_TIME_LIMIT:
            break
        
        _, g_cost, parent, puzzle = heapq.heappop(heap)
        
        # Skip puzzles already visited with lower costs
        if puzzle in vis:
            continue
        
        search_space.append(puzzle)
        parents[puzzle] = parent
        vis.add(puzzle)
        
        # Check goal state reached
        if pzh.is_goal_puzzle(puzzle):
            success = True
            break
        
        new_g_cost = g_cost + 1
        next_states = pzh.get_next_states(puzzle)
        for state in next_states:
            if state in vis:
                continue
            
            heapq.heappush(heap, (new_g_cost + heuristic(state), new_g_cost, puzzle, state))
    
    solution_space = pzh.retrace_solution_path(puzzle, parents, success)

    return solution_space, search_space, time.time() - start_time, success


if __name__ == "__main__":
    print(f"Running A_Star_H1 on test puzzle ((6,1,2),(7,8,3),(5,4,9))...")
    solution, search, _, success = a_star(((6,1,2),(7,8,3),(5,4,9)), h1)
    pzh.output("a_star_h1", success, solution, 'solution')
    pzh.output("a_star_h1", success, search, 'search')
    print("Done!")

    print(f"Running A_Star_H2 on test puzzle ((6,1,2),(7,8,3),(5,4,9))...")
    solution, search, _, success = a_star(((6,1,2),(7,8,3),(5,4,9)), h2)
    pzh.output("a_star_h2", success, solution, 'solution')
    pzh.output("a_star_h2", success, search, 'search')
    print("Done!")