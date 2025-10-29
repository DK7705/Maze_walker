from flask import Flask, render_template, request, jsonify
from maze_solver.algorithms import BFSSolver, DFSSolver, AStarSolver
from maze_solver.maze import Maze
import os

app = Flask(__name__)

# Initialize solvers
SOLVERS = {
    'bfs': BFSSolver(),
    'dfs': DFSSolver(),
    'astar': AStarSolver()
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve_maze():
    try:
        # Get the maze file and algorithm choice
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        algorithm = request.form.get('algorithm', 'bfs')
        
        if algorithm not in SOLVERS:
            return jsonify({'error': f'Unknown algorithm: {algorithm}'}), 400
            
        # Parse the maze
        content = file.read().decode('utf-8').splitlines()
        rows, cols = map(int, content[0].split())
        grid = [list(line) for line in content[1:rows+1]]
        
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)