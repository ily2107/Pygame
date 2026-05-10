import pygame
import random
import math
from collections import deque

TILE = 30

class Support_enemy:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.px = x * TILE
        self.py = y * TILE

        self.directions = [(1,0), (0,1), (-1,0), (0,-1)]

        self.move_dir = random.choice(self.directions)
        self.move_steps = random.randint(3, 8)

        self.step_cd = 0
        self.step_delay = 18

        self.bias_strength = 0.65
        self.mode = "patrol"

        self.daze = 0

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
    
    def get_chase(self, player, maze):
        root_x, root_y = self.grid_x, self.grid_y
        for dx, dy in self.directions:
            tmp_x, tmp_y = root_x + dx, root_y + dy
            while maze.is_walkable(tmp_x, tmp_y):
                if ((tmp_x, tmp_y) == (player.grid_x, player.grid_y)):
                    return True
                tmp_x += dx
                tmp_y += dy

        return False

    def update(self, player, maze):
        if self.mode == "patrol":

            dx = player.grid_x - self.grid_x
            dy = player.grid_y - self.grid_y

            dist = abs(dx) + abs(dy)

            if dist < 10:
                self.bias_strength = 0.85
            else:
                self.bias_strength = 0.55

            if self.step_cd > 0:
                self.step_cd -= 1
                return

            nx = self.grid_x + self.move_dir[0]
            ny = self.grid_y + self.move_dir[1]

            if maze.is_walkable(nx, ny):
                self.grid_x = nx
                self.grid_y = ny

                self.px = nx * TILE
                self.py = ny * TILE

            self.step_cd = self.step_delay

            self.move_steps -= 1

            if self.move_steps <= 0:
                self.move_steps = random.randint(3, 8)
                self.move_dir = self.get_biased_direction(player, maze)
            
            if self.get_chase(player, maze):
                self.mode = "chase"
        else:
            start = (self.grid_x, self.grid_y)
            goal = (player.grid_x, player.grid_y)

            path = self.bfs(start, goal, maze)

            if len(path) > 0:
                next_x, next_y = path[0]

                self.grid_x = next_x
                self.grid_y = next_y

                self.px = self.grid_x * 30
                self.py = self.grid_y * 30
            
            if not self.get_chase(player, maze):
                self.mode = "patrol"

    def get_biased_direction(self, player, maze):
        x, y = self.grid_x, self.grid_y
        tx, ty = player.grid_x, player.grid_y

        best_dir = None
        best_score = -10**9

        for dx, dy in self.directions:
            nx = x + dx
            ny = y + dy

            if not maze.is_walkable(nx, ny):
                continue

            dist = abs(nx - tx) + abs(ny - ty)

            attraction = -dist * self.bias_strength

            noise = random.uniform(-1, 1)

            score = attraction + noise

            if score > best_score:
                best_score = score
                best_dir = (dx, dy)

        if best_dir is None:
            return random.choice(self.directions)

        return best_dir