class Grid:
    def __init__(self, size, start, goals, walls, filename=None):
        self.size = size  # (rows, cols) tuple representing grid size
        self.start = start  # (x, y) tuple for starting position
        self.goals = set(goals)  # Set of (x, y) tuples for goal positions
        self.walls = self._parse_walls(walls)  # Set of (x, y) tuples for wall positions
        self.filename = filename  # Store the filename

    def _parse_walls(self, walls_input):
        walls = set()
        for x, y, w, h in walls_input:
            for i in range(w):
                for j in range(h):
                    walls.add((x + i, y + j))
        return walls

    def get_neighbors(self, pos):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        neighbors = []
        for dx, dy in directions:
            next_pos = (pos[0] + dx, pos[1] + dy)
            if (0 <= next_pos[0] < self.size[0] and 0 <= next_pos[1] < self.size[1] and
                    next_pos not in self.walls):
                neighbors.append(next_pos)
        return neighbors



def parse_map(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Parse grid size
        grid_size = [int(x) for x in lines[0].strip()[1:-1].split(',')]
        grid_size = (grid_size[1], grid_size[0])  # Swap rows and columns for consistency

        # Parse initial state
        initial_state = tuple(map(int, lines[1].strip()[1:-1].split(',')))

        # Parse goal states
        goal_states = [tuple(map(int, goal.strip()[1:-1].split(','))) for goal in lines[2].strip().split('|')]

        # Parse wall locations, safely ignoring non-numeric parts or comments
        walls = []
        for wall in lines[3:]:
            try:
                # Strip out inline comments if they exist (assuming comments start with '#')
                wall = wall.split('#')[0].strip()
                if wall:
                    walls.append(tuple(map(int, wall[1:-1].split(','))))
            except ValueError as e:
                print(f"Skipping invalid wall entry: {wall}. Error: {str(e)}")

    return Grid(grid_size, initial_state, goal_states, walls, filename)

