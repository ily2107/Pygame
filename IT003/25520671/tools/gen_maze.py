import random

ROWS, COLS = 32, 22

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

def gen_lv1():
    maze = [[1]*ROWS for _ in range(COLS)]
    maze[0][0] = maze[0][1] = maze[1][0] = 0

    def dfs(x, y):
        maze[x][y] = 0

        dirs = [0, 1, 2, 3]
        random.shuffle(dirs)

        for idx in dirs:
            nx, ny = x + dx[idx], y + dy[idx]

            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if maze[nx][ny] == 1:

                    cnt = 0
                    for nidx in range(4):
                        tx, ty = nx + dx[nidx], ny + dy[nidx]

                        if 0 <= tx < COLS and 0 <= ty < ROWS:
                            if maze[tx][ty] == 0:
                                cnt += 1

                    if cnt <= 1:
                        dfs(nx, ny)

    dfs(0, 1)
    dfs(1, 0)

    def braid(chance=0.35):
        for x in range(COLS):
            for y in range(ROWS):

                if maze[x][y] == 1:
                    continue

                dirs = [(1,0),(-1,0),(0,1),(0,-1)]

                open_cnt = 0
                walls = []

                for dx_, dy_ in dirs:
                    nx, ny = x + dx_, y + dy_

                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        if maze[nx][ny] == 0:
                            open_cnt += 1
                        else:
                            walls.append((nx, ny))

                if open_cnt == 1 and len(walls) > 1 and random.random() < chance:
                    wx, wy = random.choice(walls)
                    maze[wx][wy] = 0

    braid()

    return maze


maze = gen_lv1()

for row in maze:
    print("".join(map(str, row)))