import random

ROWS, COLS = 24, 16

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

                    if cnt <= 1 or random.random() < 0.05:
                        dfs(nx, ny)

    dfs(0, 1)
    dfs(1, 0)

    return maze

maze = gen_lv1()

for row in maze:
    print("".join(map(str, row)))