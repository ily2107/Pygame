from collections import deque

class Enemy:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.px = x * 40
        self.py = y * 40

    def bfs(self, start, goal, maze):
        queue = deque([start])
        visited = set()
        parent = {}

        visited.add(start)

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            moves = [(1,0), (-1,0), (0,1), (0,-1)]

            for dx, dy in moves:
                nx = x + dx
                ny = y + dy

                if not maze.is_walkable(nx, ny):
                    continue

                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

        path = []
        cur = goal

        while cur != start:
            path.append(cur)
            cur = parent.get(cur)
            if cur is None:
                return []

        path.reverse()
        return path

    def update(self, player, maze):
        start = (self.grid_x, self.grid_y)
        goal = (player.grid_x, player.grid_y)

        path = self.bfs(start, goal, maze)

        if len(path) > 0:
            next_x, next_y = path[0]

            self.grid_x = next_x
            self.grid_y = next_y

            self.px = self.grid_x * 40
            self.py = self.grid_y * 40