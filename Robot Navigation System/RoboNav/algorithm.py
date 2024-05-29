from collections import deque
from queue import PriorityQueue
import sys
from math import sqrt

# Helper functions
def heuristic(current, goal):
    # Manhattan distance as heuristic
    return abs(goal[0] - current[0]) + abs(goal[1] - current[1])

def get_directions(path):
    directions = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]  # Change in x-coordinate (row)
        dy = path[i][1] - path[i - 1][1]  # Change in y-coordinate (column)
        if dy == 1:
            directions.append("down")
        elif dy == -1:
            directions.append("up")
        elif dx == 1:
            directions.append("right")
        elif dx == -1:
            directions.append("left")
    return directions


def print_path_info(goal, path, visited):
    print(f"The goal {goal} is reachable.")
    print(f"Path: {', '.join(map(str, path))}")
    print(f"Directions: {', '.join(get_directions(path))}")
    print(f"Number of nodes traversed: {len(visited)}")
    print(f"Traversal Path: {', '.join(map(str, visited))}")

# Breadth-First Search
def bfs(grid, start=None):
    if start is None:
        start = grid.start
    queue = deque([(start, [start])])
    visited = set()
    visited_order = []

    while queue:
        current, path = queue.popleft()
        visited.add(current)
        visited_order.append(current)

        if current in grid.goals:
            print_path_info(current, path, visited_order)
            return path, visited_order

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    print("No goal is reachable.")
    return None, visited_order

# Depth-First Search
def dfs(grid, start=None):
    if start is None:
        start = grid.start
    stack = [(start, [start])]
    visited = set()
    visited_order = []

    while stack:
        current, path = stack.pop()
        if current not in visited:
            visited.add(current)
            visited_order.append(current)

            if current in grid.goals:
                print_path_info(current, path, visited_order)
                return path, visited_order

            for neighbor in reversed(grid.get_neighbors(current)):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    print("No goal is reachable.")
    return None, visited_order

# A* Search
def heuristic(current, goal):
    # Manhattan distance as heuristic
    return abs(goal[0] - current[0]) + abs(goal[1] - current[1])

def get_directions(path):
    directions = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]  # Change in x-coordinate (row)
        dy = path[i][1] - path[i - 1][1]  # Change in y-coordinate (column)
        if dy == 1:
            directions.append("down")
        elif dy == -1:
            directions.append("up")
        elif dx == 1:
            directions.append("right")
        elif dx == -1:
            directions.append("left")
    return directions

def a_star(grid, start=None, goals=None):
    if start is None:
        start = grid.start
    if goals is None:
        goals = grid.goals

    frontier = PriorityQueue()
    frontier.put((0, start, [start]))
    visited = set()
    cost_so_far = {start: 0}
    goal = list(goals)[0]  # Assuming a single goal for simplicity in heuristic calculation

    while not frontier.empty():
        _, current, path = frontier.get()

        if current in goals:
            # Formatting and printing the output when the goal is reached
            print(f"The goal {goal} is reachable.")
            print(f"Path: {', '.join(map(str, path))}")
            print(f"Directions: {', '.join(get_directions(path))}")
            print(f"Number of nodes traversed: {len(visited)}")
            print(f"Traversal Path: {', '.join(map(str, visited))}")
            return path, visited

        if current not in visited:
            visited.add(current)
            for neighbor in grid.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Assuming uniform cost
                if neighbor not in visited or new_cost < cost_so_far.get(neighbor, float('inf')):
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    frontier.put((priority, neighbor, path + [neighbor]))

    print("No goal is reachable.")
    return None, visited

# Greedy Best-First Search
def gbfs(grid, start=None):
    if start is None:
        start = grid.start
    frontier = PriorityQueue()
    frontier.put((0, start, [start]))
    visited = set()
    visited_order = []

    while not frontier.empty():
        _, current, path = frontier.get()
        visited.add(current)
        visited_order.append(current)

        if current in grid.goals:
            print_path_info(current, path, visited_order)
            return path, visited_order

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                priority = heuristic(neighbor, list(grid.goals)[0])
                frontier.put((priority, neighbor, path + [neighbor]))
    
    print("No goal is reachable.")
    return None, visited_order

# Depth-Limited Search
def dls(grid, start, goal, limit, visited=None):
    if visited is None:
        visited = set()

    stack = [(start, [start], visited.copy())]  # Use a local copy of visited for each path

    while stack:
        current, path, local_visited = stack.pop()
        local_visited.add(current)

        if current in goal:
            # Only return path and visited, don't print here
            return path, local_visited
        if len(path) - 1 < limit:
            for neighbor in grid.get_neighbors(current):
                if neighbor not in local_visited:
                    stack.append((neighbor, path + [neighbor], local_visited.copy()))

    return None, visited

# Iterative Deepening Search
def ids(grid, start=None, goal=None):
    if start is None:
        start = grid.start
    if goal is None:
        goal = grid.goals

    visited_overall = set()
    for limit in range(sys.maxsize):
        path, visited = dls(grid, start, goal, limit)
        visited_overall.update(visited)
        if path:
            # Only print information when a successful path is found
            print_path_info(goal, path, visited)
            return path, visited_overall
    # Handle the case when no path is found
    if not path:
        print("No goal is reachable.")
        print(f"Total nodes visited: {len(visited_overall)}")
    return None, visited_overall

#Best First Search
def best_first_search(grid, start=None):
    if start is None:
        start = grid.start
    frontier = PriorityQueue()
    frontier.put((0, start, [start]))  # (priority, current_node, path)
    visited = set()
    visited_order = []

    while not frontier.empty():
        _, current, path = frontier.get()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current in grid.goals:
            print_path_info(current, path, visited_order)
            return path, visited_order

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                priority = heuristic(neighbor, list(grid.goals)[0])  # Change heuristic as appropriate
                frontier.put((priority, neighbor, path + [neighbor]))

    print("No goal is reachable.")
    return None, visited_order
