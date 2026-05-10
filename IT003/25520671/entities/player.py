import pygame
from core.maze import Maze
class Player: 
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.px = x * 30
        self.py = y * 30

        self.target_x = self.px 
        self.target_y = self.py
        
        self.speed = 5
        self.moving = False
        self.cooldown = 0

        self.inventory = []
    
    def handle_input(self, keys, maze):
        if self.moving or self.cooldown > 0: 
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
        self.target_x, self.target_y = nx * 30, ny * 30

        self.moving = True
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        
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
            self.cooldown = 3
        