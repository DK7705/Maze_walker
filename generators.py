import random

class MazeGenerator:
    """Base class for all maze generators."""
    def generate(self, rows, cols):
        """Returns a new grid (list of strings) representing the maze."""
        pass

class DFSMazeGenerator(MazeGenerator):
    """Generates a maze using the Recursive Backtracker (DFS) algorithm."""
    def generate(self, rows, cols):
        # Initialize grid with all walls (#)
        grid_rows = rows * 2 + 1
        grid_cols = cols * 2 + 1
        grid = [['#' for _ in range(grid_cols)] for _ in range(grid_rows)]
        
        # Grid for tracking visited cells in the generation process
        visited = set()
        stack = []
        
        # Start in a random inner cell
        start_cell = (random.randrange(rows), random.randrange(cols))
        visited.add(start_cell)
        stack.append(start_cell)
        
        def to_grid_coords(r, c):
            return 2 * r + 1, 2 * c + 1
        
        def carve_path(r1, c1, r2, c2):
            """Carve a path between two adjacent cells (r1, c1) and (r2, c2)."""
            gr1, gc1 = to_grid_coords(r1, c1)
            gr2, gc2 = to_grid_coords(r2, c2)
            
            # Carve path at cell centers
            grid[gr1][gc1] = ' '
            grid[gr2][gc2] = ' '
            
            # Carve wall between them
            mid_r = (gr1 + gr2) // 2
            mid_c = (gc1 + gc2) // 2
            grid[mid_r][mid_c] = ' '

        while stack:
            r, c = stack[-1]
            
            # Find unvisited neighbors
            neighbors = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    neighbors.append((nr, nc, dr, dc))
            
            if neighbors:
                # Choose a random neighbor
                nr, nc, dr, dc = random.choice(neighbors)
                
                # Carve path to new cell
                carve_path(r, c, nr, nc)
                
                # Move to new cell
                visited.add((nr, nc))
                stack.append((nr, nc))
            else:
                # Backtrack
                stack.pop()

        # Set Start and End points in the top-left and bottom-right corners
        grid[1][1] = 'S'
        grid[grid_rows - 2][grid_cols - 2] = 'E'
        
        # Convert to list of strings, required for Flask jsonify
        return ["".join(row) for row in grid]

class PrimMazeGenerator(MazeGenerator):
    """Generates a maze using Prim's algorithm."""
    def generate(self, rows, cols):
        
        grid_rows = rows * 2 + 1
        grid_cols = cols * 2 + 1
        grid = [['#' for _ in range(grid_cols)] for _ in range(grid_rows)]
        
        # Cell status: 0=unvisited, 1=frontier, 2=in maze
        cell_status = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # List of frontier walls (r, c, dr, dc)
        frontier = [] 
        
        def to_grid_coords(r, c):
            return 2 * r + 1, 2 * c + 1
        
        # 1. Start with a random cell
        start_r, start_c = random.randrange(rows), random.randrange(cols)
        cell_status[start_r][start_c] = 2 # In maze
        grid[2 * start_r + 1][2 * start_c + 1] = ' '
        
        # Add its walls to the frontier list
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = start_r + dr, start_c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                frontier.append((start_r, start_c, dr, dc))
                cell_status[nr][nc] = 1 # Frontier

        # 2. Loop until frontier is empty
        while frontier:
            # Pick a random wall from the frontier (randomized Prim's)
            r1, c1, dr, dc = frontier.pop(random.randrange(len(frontier)))
            r2, c2 = r1 + dr, c1 + dc
            
            if cell_status[r2][c2] == 1: # If the new cell is a frontier cell
                
                # Carve a path
                grid[2 * r2 + 1][2 * c2 + 1] = ' '
                grid[2 * r1 + 1 + dr][2 * c1 + 1 + dc] = ' ' # Mid-wall
                
                cell_status[r2][c2] = 2 # Add new cell to maze

                # Add the new cell's walls to the frontier list
                for dr_new, dc_new in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r2 + dr_new, c2 + dc_new
                    if 0 <= nr < rows and 0 <= nc < cols and cell_status[nr][nc] == 0:
                        frontier.append((r2, c2, dr_new, dc_new))
                        cell_status[nr][nc] = 1 # Mark as frontier

        # Set Start and End points
        grid[1][1] = 'S'
        grid[grid_rows - 2][grid_cols - 2] = 'E'

        # Convert to list of strings
        return ["".join(row) for row in grid]