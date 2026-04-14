import random
from core.maze import Maze

type = random.randint(1,3)
maze = Maze.load_from_txt(f"maps/level1/map{type}.txt")

player_spawn = (0, 0)
x, y = 0, 0

for i in range (maze.rows):
    for j in range (maze.cols):
        if maze.is_walkable(i, j):
            if i + j >= x + y:
                x, y = i, j

enemy_spawn = (x, y)

goal_x, goal_y = maze.cols - 1, maze.rows - 1