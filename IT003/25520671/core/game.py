import pygame
import random
from setting import *
from ui.menu import Menu
from core.maze import Maze
from systems.renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.menu = Menu(self)

        self.map_type = random.randint(1,3)
        if self.map_type == 1:
            self.maze = Maze.load_from_txt("maps/level1/map1.txt")
        elif self.map_type == 2:
            self.maze = Maze.load_from_txt("maps/level1/map2.txt")
        else: 
            self.maze = Maze.load_from_txt("maps/level1/map3.txt")
            
        self.renderer = Renderer(self.screen)
        self.renderer.draw_maze(self.maze, self.map_type)
    
    def run(self):
        while True:
            self.menu.run()
            self.run_game()

    def run_game(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.screen.blit(self.renderer.maze_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)
        