import pygame
import random
import math

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

    def update(self, player, maze, game):

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