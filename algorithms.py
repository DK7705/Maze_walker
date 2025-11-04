from abc import ABC, abstractmethod
import time
from collections import deque
import heapq
import math

class MazeSolver(ABC):
    def __init__(self):
        self.nodes_explored = 0
        self.time_taken = 0
        
    @abstractmethod
    def solve(self, maze):
        pass
        
    def get_stats(self):
        return {
            'nodes_explored': self.nodes_explored,
            'time_ms': self.time_taken * 1000  # Convert to milliseconds
        }
        
class BFSSolver(MazeSolver):
    def solve(self, maze):
        start_time = time.time()
        self.nodes_explored = 0
        
        # Initialize BFS
        queue = deque([(maze.start)])
        visited = {maze.start: None}  # Maps position to its parent
        
        while queue:
            current = queue.popleft()
            self.nodes_explored += 1
            
            if current == maze.end:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = visited[current]
                path.reverse()
                
                self.time_taken = time.time() - start_time
                return path
                
            # Explore neighbors
            x, y = current
            for next_pos in maze.get_neighbors(x, y):
                if next_pos not in visited:
                    visited[next_pos] = current
                    queue.append(next_pos)
                    
        self.time_taken = time.time() - start_time
        return None  # No path found

class DFSSolver(MazeSolver):
    def solve(self, maze):
        start_time = time.time()
        self.nodes_explored = 0
        
        # Initialize DFS
        stack = [(maze.start)]
        visited = {maze.start: None}
        
        while stack:
            current = stack.pop()
            self.nodes_explored += 1
            
            if current == maze.end:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = visited[current]
                path.reverse()
                
                self.time_taken = time.time() - start_time
                return path
                
            # Explore neighbors
            x, y = current
            for next_pos in maze.get_neighbors(x, y):
                if next_pos not in visited:
                    visited[next_pos] = current
                    stack.append(next_pos)
                    
        self.time_taken = time.time() - start_time
        return None  # No path found

class AStarSolver(MazeSolver):
    def heuristic(self, pos, goal):
        """Manhattan distance heuristic"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    def solve(self, maze):
        start_time = time.time()
        self.nodes_explored = 0
        
        # Initialize A*
        start = maze.start
        goal = maze.end
        
        frontier = [(0, start)]  # Priority queue of (f_score, position)
        came_from = {start: None}
        g_score = {start: 0}  # Cost from start to current position
        f_score = {start: self.heuristic(start, goal)}  # Estimated total cost
        
        while frontier:
            current = heapq.heappop(frontier)[1]
            self.nodes_explored += 1
            
            if current == goal:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                
                self.time_taken = time.time() - start_time
                return path
            
            # Explore neighbors
            x, y = current
            for next_pos in maze.get_neighbors(x, y):
                # g_score is just distance from start (each step costs 1)
                tentative_g = g_score[current] + 1
                
                if next_pos not in g_score or tentative_g < g_score[next_pos]:
                    came_from[next_pos] = current
                    g_score[next_pos] = tentative_g
                    f = tentative_g + self.heuristic(next_pos, goal)
                    f_score[next_pos] = f
                    heapq.heappush(frontier, (f, next_pos))
        
        self.time_taken = time.time() - start_time
        return None  # No path found