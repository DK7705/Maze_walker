from flask import Flask, render_template, request, jsonify
from maze_solver.algorithms import BFSSolver, DFSSolver, AStarSolver
from maze_solver.maze import Maze
from maze_solver.generators import DFSMazeGenerator, PrimMazeGenerator
import os
import json # Added to handle JSON body from frontend

app = Flask(__name__)

# Initialize solvers
SOLVERS = {
    'bfs': BFSSolver(),
    'dfs': DFSSolver(),
    'astar': AStarSolver()
}

# Initialize generators
GENERATORS = {
    'dfs': DFSMazeGenerator(),
    'prim': PrimMazeGenerator()
}

@app.route('/')
def index():
    return render_template('index.html')

# NEW ROUTE FOR MAZE GENERATION
@app.route('/api/generate', methods=['POST'])
def generate_maze():
    try:
        # Get data from JSON body
        data = request.get_json()
        algorithm = data.get('algorithm', 'dfs')
        # Use integer division // 2 because the generator works on cell count, 
        # but the UI inputs are for grid dimensions (odd numbers like 31, 51).
        rows = int(data.get('rows', 31)) // 2
        cols = int(data.get('cols', 31)) // 2

        if algorithm not in GENERATORS:
            return jsonify({'error': f'Unknown generator algorithm: {algorithm}'}), 400

        # Run the generation
        generator = GENERATORS[algorithm]
        grid = generator.generate(rows, cols) 
        
        # Return grid as list of strings
        return jsonify({'grid': grid})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/solve', methods=['POST'])
def solve_maze():
    try:
        algorithm = request.form.get('algorithm', 'bfs')
        grid = None
        
        if 'file' in request.files and request.files['file'].filename != '':
            # 1. Solving an uploaded file
            file = request.files['file']
            
            # Parse the maze
            content = file.read().decode('utf-8').splitlines()
            rows, cols = map(int, content[0].split())
            
            # --- START OF FIX ---
            # Pad any blank or short lines with spaces to match the declared width
            # This prevents "list index out of range" errors in maze.py
            grid = [list(line.ljust(cols, ' ')) for line in content[1:rows+1]]
            # --- END OF FIX ---
            
        elif 'data' in request.form:
            # 2. Solving a generated/loaded maze (passed via JSON in 'data' field)
            data = json.loads(request.form.get('data'))
            grid = data['grid']
            
            # If the grid is provided as a list of strings, convert it to list of lists of chars
            if isinstance(grid[0], str):
                grid = [list(line) for line in grid]
                
        else:
            return jsonify({'error': 'No maze file uploaded or maze data provided'}), 400

        if algorithm not in SOLVERS:
            return jsonify({'error': f'Unknown algorithm: {algorithm}'}), 400
            
        # Create maze object
        maze = Maze(grid)
        
        # Solve the maze
        solver = SOLVERS[algorithm]
        path = solver.solve(maze)
        
        if path is None:
            return jsonify({'error': 'No solution found'}), 404
            
        # Return the solution
        return jsonify({
            'grid': grid,
            'path': path,
            'stats': solver.get_stats()
        })
        
    except Exception as e:
        # Provide a more specific error message to the frontend
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)