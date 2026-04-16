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

far_cells = walkable[:len(walkable)]

positions = random.sample(far_cells, 4)

dorayaki = positions[:3]
doraemon = positions[3]

while True:
    enemy = walkable[:len(walkable)//4]
    check = (enemy[0] == goal_x and enemy[1] == goal_y)
    for i in range (4):
        if enemy[0] == positions[i]:
            check = True
            break
    enemy_spawn = enemy[0]
    if check == False:
        break
