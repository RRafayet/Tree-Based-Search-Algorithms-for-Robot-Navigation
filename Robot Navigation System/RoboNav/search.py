import sys
from time import sleep
from grid import parse_map
from algorithm import bfs, dfs, gbfs, a_star, ids, best_first_search

# Attempt to import pygame
pygame_installed = False
try:
    import pygame
    from pygame.locals import *
    pygame_installed = True
except ImportError:
    print("Pygame is not installed, running in command-line mode only.")

# Define constants for visualization
if pygame_installed:
    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    AGENT_COLOR = (0, 255, 0)  # Color for the agent
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)  # Color for the path
    CELL_SIZE = 40
    PADDING = 2

def draw_initial_grid(screen, grid, visited=None):
    """Draws the initial state of the grid, rotated 90 degrees counterclockwise."""
    for i in range(grid.size[0]):
        for j in range(grid.size[1]):
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)  # Fill cell with white
            if (i, j) in grid.walls:
                pygame.draw.rect(screen, BLACK, rect)  # Draw walls in black
            elif visited and (i, j) in visited:
                pygame.draw.rect(screen, BLUE, rect)  # Mark visited nodes
            pygame.draw.rect(screen, BLACK, rect, 1)  # Grid lines in black

def draw_agent_and_goals(screen, grid, path, current_pos):
    """Draws the agent and goals on the grid, rotated 90 degrees counterclockwise."""
    # Draw goals
    for goal in grid.goals:
        goal_rect = pygame.Rect(goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, goal_rect)  # Goals in red
    
    # Draw agent at current position
    if current_pos:
        agent_rect = pygame.Rect(current_pos[0] * CELL_SIZE, current_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, AGENT_COLOR, agent_rect)  # Agent in green

def animate_agent(screen, grid, path):
    """Animates the agent moving along the path, rotated 90 degrees counterclockwise."""
    for node in path:
        draw_initial_grid(screen, grid)  # Redraw grid for each step
        draw_agent_and_goals(screen, grid, path, node)  # Draw the agent and goals
        pygame.display.flip()
        sleep(0.25)

def main(filename, method_name):
    grid = parse_map(filename)

    search_methods = {
        'dfs': dfs,
        'bfs': bfs,
        'gbfs': gbfs,
        'a_star': a_star,
        'cus_1': ids,
        'cus_2': best_first_search
    }

    if method_name not in search_methods:
        print(f"Search method '{method_name}' not recognized.")
        sys.exit(1)

    try:
        search_method = search_methods[method_name]
        path, visited = search_method(grid)
    except Exception as e:
        print(f"An error occurred during the search: {str(e)}")
        sys.exit(1)

    if pygame_installed and path:
        pygame.init()
        screen_size = (grid.size[0] * CELL_SIZE, grid.size[1] * CELL_SIZE)
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Pathfinding Visualization - Rotated')

        draw_initial_grid(screen, grid, visited)
        pygame.display.flip()

        sleep(1)
        animate_agent(screen, grid, path)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

        pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <map_filename> <search_method>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2].lower())
