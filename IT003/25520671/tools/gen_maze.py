import random
import os

ROWS = 22
COLS = 32

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

configs = {
    1: {
        "braid": 0.25,
        "rooms": 3,
        "room_size": 2
    },

    2: {
        "braid": 0.65,
        "rooms": 12,
        "room_size": 2
    },

    3: {
        "braid": 0.8,
        "rooms": 15,
        "room_size": 2
    }
}

def gen_maze(level):
    cfg = configs[level]

    maze = [[1] * ROWS for _ in range(COLS)]

    maze[0][0] = 0
    maze[0][1] = 0
    maze[1][0] = 0

    def dfs(x, y):
        maze[x][y] = 0

        dirs = [0, 1, 2, 3]
        random.shuffle(dirs)

        for idx in dirs:
            nx = x + dx[idx]
            ny = y + dy[idx]

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                continue

            if maze[nx][ny] == 0:
                continue

            cnt = 0

            for k in range(4):
                tx = nx + dx[k]
                ty = ny + dy[k]

                if 0 <= tx < COLS and 0 <= ty < ROWS:
                    if maze[tx][ty] == 0:
                        cnt += 1

            if cnt <= 1:
                dfs(nx, ny)

    dfs(0, 1)
    dfs(1, 0)

    def braid(chance):
        for x in range(COLS):
            for y in range(ROWS):

                if maze[x][y] == 1:
                    continue

                open_cnt = 0
                walls = []

                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]

                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        if maze[nx][ny] == 0:
                            open_cnt += 1
                        else:
                            walls.append((nx, ny))

                if open_cnt == 1 and len(walls) > 0:
                    if random.random() < chance:
                        wx, wy = random.choice(walls)
                        maze[wx][wy] = 0

    braid(cfg["braid"])

    for _ in range(cfg["rooms"]):
        size = cfg["room_size"]

        x = random.randint(1, COLS - size - 1)
        y = random.randint(1, ROWS - size - 1)

        for i in range(size):
            for j in range(size):
                maze[x + i][y + j] = 0

    return maze

def save_maze(maze, path):
    with open(path, "w") as f:
        for y in range(ROWS):
            line = ""

            for x in range(COLS):
                line += str(maze[x][y])

            f.write(line + "\n")

for level in [1, 2, 3]:
    folder = f"maps/level{level}"

    os.makedirs(folder, exist_ok=True)

    for idx in range(1, 4):
        maze = gen_maze(level)

        save_maze(
            maze,
            f"{folder}/map{idx}.txt"
        )