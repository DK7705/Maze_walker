class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        self.start = self._find_point('S')
        self.end = self._find_point('E')
        
    def _find_point(self, char):
        """Find a specific character (S or E) in the maze"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == char:
                    return (x, y)
        return None
        
    def is_valid_move(self, x, y):
        """Check if a position is within bounds and not a wall"""
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.grid[y][x] != '#')
                
    def get_neighbors(self, x, y):
        """Get valid neighboring positions"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_x, new_y = x + dx, y + dy
            if self.is_valid_move(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors