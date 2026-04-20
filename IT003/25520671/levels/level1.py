import random
from core.maze import Maze

type = random.randint(1,3)
maze = Maze.load_from_txt(f"maps/level1/map{type}.txt")

player_spawn = (0, 0)
goal_x, goal_y = maze.cols - 1, maze.rows - 1

walkable = []

for i in range(maze.rows):
    for j in range(maze.cols):
        if maze.is_walkable(i, j) and (i, j) != player_spawn and (j, i) != (goal_x, goal_y):
            walkable.append((j, i))

def far(cell):
    return abs(cell[0] - player_spawn[0]) + abs(cell[1] - player_spawn[1])

walkable.sort(key = far, reverse = True)

enemy = walkable[:len(walkable)//4]
enemy_spawn = enemy[0]