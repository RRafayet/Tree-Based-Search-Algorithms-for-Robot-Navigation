import unittest
from algorithm import bfs, dfs, a_star, gbfs, ids, best_first_search
from grid import Grid

class TestPathfindingAlgorithms(unittest.TestCase):
    def test_simple_open_grid(self):
        grid = Grid((10, 10), (1, 1), [(8, 8)], [])
        path, visited = bfs(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (8, 8))

    def test_no_solution(self):
        walls = [(0, 7, 10, 1)]  # x, y, width, height
        grid = Grid((10, 10), (1, 1), [(8, 8)], walls)
        path, visited = bfs(grid)
        self.assertIsNone(path)

    def test_path_require_backtracking(self):
        walls = [(0, 8, 9, 1), (8, 6, 1, 2)]
        grid = Grid((10, 10), (0, 0), [(9, 9)], walls)
        path, visited = dfs(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (9, 9))

    def test_complex_maze_grid(self):
        walls = [(0, 1, 1, 2), (1, 3, 1, 2), (2, 5, 1, 2), (3, 7, 1, 2),
                 (4, 2, 1, 3), (5, 4, 1, 3), (6, 6, 1, 3), (7, 1, 1, 4), (8, 3, 1, 4)]
        grid = Grid((10, 10), (0, 0), [(9, 9)], walls)
        path, visited = a_star(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (9, 9))

    def test_large_sparse_grid(self):
        walls = [(10, 5, 1, 5), (5, 10, 5, 1)]
        grid = Grid((20, 20), (1, 1), [(18, 18)], walls)
        path, visited = bfs(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (18, 18))

    def test_performance_test(self):
        walls = [(3, 3, 1, 15), (5, 0, 1, 18), (10, 2, 10, 1)]
        grid = Grid((20, 20), (0, 0), [(19, 19)], walls)
        path, visited = bfs(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (19, 19))

    def test_single_wall_barrier_grid(self):
        walls = [(5, 0, 1, 4), (5, 5, 1, 5)]
        grid = Grid((10, 10), (0, 0), [(9, 9)], walls)
        path, visited = a_star(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (9, 9))

    def test_multiple_goals_grid(self):
        grid = Grid((10, 10), (0, 0), [(9, 0), (0, 9), (9, 9)], [])
        path, visited = bfs(grid)
        self.assertIsNotNone(path)
        self.assertTrue(any(path[-1] == goal for goal in [(9, 0), (0, 9), (9, 9)]))

    def test_sparse_obstacles_grid(self):
        walls = [(1, 2, 1, 1), (3, 5, 1, 1), (7, 8, 1, 1), (4, 3, 1, 1), (6, 6, 1, 1)]
        grid = Grid((10, 10), (0, 0), [(9, 9)], walls)
        path, visited = gbfs(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (9, 9))

    def test_tight_corridors_grid(self):
        walls = [(1, 1, 8, 1), (1, 3, 8, 1), (1, 5, 8, 1), (1, 7, 8, 1)]
        grid = Grid((10, 10), (0, 0), [(9, 9)], walls)
        path, visited = bfs(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], (9, 9))


if __name__ == '__main__':
    unittest.main()
