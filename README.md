# Maze Solver

A clean, offline-capable maze solving application with multiple algorithms and real-time visualization.

## Features

- Multiple maze solving algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search
- Real-time visualization of the solving process
- Supports both text file and visual maze creation
- Offline-capable (no internet required)
- Clean, modern UI

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open a browser and navigate to:
```
http://localhost:5000
```

## Maze File Format

Text files should use the following format:
```
15 20
####################
#S       #        #
# ###### # ###### #
#      # # #    # #
###### # # # ## # #
#    # #   #  # # #
# ## ##### #### # #
#  #     #      # #
## ##### ######## #
#  #   #          #
# ## # ########## #
#  # #          # #
## # ########## # #
#    #          #E#
####################
```

Where:
- First line: height width
- '#' = Wall
- 'S' = Start
- 'E' = End
- ' ' = Path

## Algorithms

### Breadth-First Search (BFS)
- Guarantees shortest path
- Explores uniformly in all directions
- Memory usage: O(w*h)

### Depth-First Search (DFS)
- May not find shortest path
- Memory efficient
- Memory usage: O(w+h)

### A* Search
- Guarantees shortest path
- Uses heuristics to optimize search
- Memory usage: O(w*h)


## 📂 File Structure
Here is the project's file structure:

```
MAZE_WALKER-MAIN/
├── maze_solver/
│   ├── __init__.py
│   ├── algorithms.py   # Contains BFS, DFS, and A* solving algorithms
│   ├── generators.py   # Contains DFS and Prim's maze generators
│   └── maze.py         # Maze class to handle grid logic
│
├── templates/
│   └── index.html      # Main frontend page for the UI
│
├── .gitignore
├── app.py              # Main Flask application file
├── maze1.txt           # Example maze file
├── maze2.txt           # Example maze file
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
└── setup.py            # Project setup script
```