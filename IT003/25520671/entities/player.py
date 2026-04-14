import pygame
from core.maze import Maze
class Player: 
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.px = x * 40
        self.py = y * 40

        self.target_x = self.px 
        self.target_y = self.py
        
        self.speed = 4
        self.moving = False
    
    def handle_input(self, keys, maze):
        if self.moving: 
            return
        nx, ny = self.grid_x, self.grid_y
        if keys[pygame.K_LEFT]:
            nx -= 1
        elif keys[pygame.K_RIGHT]:
            nx += 1
        elif keys[pygame.K_UP]:
            ny -= 1
        elif keys[pygame.K_DOWN]:
            ny += 1

        if not maze.is_walkable(nx, ny):
            return
        
        self.grid_x, self.grid_y = nx, ny
        self.target_x, self.target_y = nx * 40, ny * 40

        self.moving = True
    
    def update(self):
        if not self.moving:
            return
        
        if self.px < self.target_x:
            self.px += self.speed
        elif self.px > self.target_x:
            self.px -= self.speed

        if self.py < self.target_y:
            self.py += self.speed
        elif self.py > self.target_y:
            self.py -= self.speed

        if self.px == self.target_x and self.py == self.target_y:
            self.moving = False
        