import time
import heapq
import collections
import puzzle_helper as pzh


# Heuristic 1: Returns number of positions out of place in puzzle
# NOT ADMISSIBLE:
# (2,1,3)
# (4,5,6)
# (7,8,9)
# h1(state) = 2, Real Cost = 1
def h1(puzzle):
    val = 1
    count = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != val:
                count += 1
            val += 1
    return count


# Heuristic 2: Returns the Manhattan distance of passed state divided by 2
# (sum of all the distances by which positions are out of place)
# ADMISSIBLE:
# (2,1,3)
# (4,5,6)
# (7,8,9)
# h2(state) = 1, Real Cost = 1
def h2(puzzle):
    s = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            val = puzzle[i][j]
            real_row = (val-1) // len(puzzle)
            real_col = (val-1) % len(puzzle)
            s += abs(i-real_row) + abs(j-real_col)
    return s / 2


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
    for i, h in enumerate([h1, h2], 1):
        print(f"Running A_Star_H{i} on test puzzle ((6,1,2),(7,8,3),(5,4,9))...")
        solution, search, ex_time, success = a_star(((6,1,2),(7,8,3),(5,4,9)), h1)
        pzh.output(f"A_Star_H{i}", success, solution, 'solution')
        pzh.output(f"A_Star_H{i}", success, search, 'search')
        print(f'Done! Execution Time: {ex_time} seconds')