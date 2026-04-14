from setting import *
import random
from entities.cell import Cell

class Maze:
    def __init__(self, grid):
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.grid = [
            [Cell(i, j) for j in range(self.cols)]
            for i in range (self.rows)
        ]
        
        for i in range (self.rows):
            for j in range (self.cols):
                if grid[i][j] == 0:
                    self.grid[i][j].type = "Path"
                else: self.grid[i][j].type = "Wall"

    def is_walkable(self, x, y):
        if x < 0 or y < 0 or x >= self.cols or y >= self.rows:
            return False
        return self.grid[y][x].type == "Path"
    
    @classmethod
    def load_from_txt(cls, path):
        grid = []
        with open(path, "r") as f:
            for line in f:
                row = list(map(int, line.strip()))
                grid.append(row)

        return cls(grid)