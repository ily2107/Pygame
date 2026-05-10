import pygame
from collections import deque

TILE = 30

class MiniBoss:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.px = x * TILE
        self.py = y * TILE

        self.path = []

        self.step_delay = 30
        self.step_cd = 0

    def bfs(self, start, goal, maze):
        queue = deque([start])

        visited = set([start])

        parent = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx = x + dx
                ny = y + dy

                if not maze.is_walkable(nx, ny):
                    continue

                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))

                parent[(nx, ny)] = (x, y)

                queue.append((nx, ny))

        if goal not in visited:
            return []

        path = []

        cur = goal

        while cur != start:
            path.append(cur)
            cur = parent[cur]

        path.reverse()

        return path

    def go_to(self, target, maze):
        start = (self.grid_x, self.grid_y)

        self.path = self.bfs(start, target, maze)

    def update(self):
        if self.step_cd > 0:
            self.step_cd -= 1
            return

        if len(self.path) == 0:
            return

        nx, ny = self.path.pop(0)

        self.grid_x = nx
        self.grid_y = ny

        self.px = nx * TILE
        self.py = ny * TILE

        self.step_cd = self.step_delay