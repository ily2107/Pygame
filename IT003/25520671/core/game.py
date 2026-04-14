import time
import pygame
import random
import importlib
from setting import *
from ui.menu import Menu
from core.maze import Maze
from entities.player import Player
from entities.enemy import Enemy
from systems.renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.menu = Menu(self)
        self.level_cnt = 1
        self.last_move = 0

        self.level = importlib.import_module(f"levels.level{self.level_cnt}")
        self.player = Player(*self.level.player_spawn)
        self.enemy = Enemy(self.level.x, self.level.y)

        self.game_over = False
        self.game_victory = False

        self.renderer = Renderer(self.screen)
        self.renderer.draw_maze(self.level.maze, self.level.type)
    
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

            if self.game_over:
                self.show_game_over()
                continue

            if self.game_victory:
                self.show_game_victory()
                continue

            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, self.level.maze)
            self.player.update()

            if time.time() - self.last_move > 0.3:
                self.enemy.update(self.player, self.level.maze)
                self.last_move = time.time()

            if self.enemy.grid_x == self.player.grid_x and self.enemy.grid_y == self.player.grid_y:
                self.game_over = True

            if self.player.grid_x == self.level.goal_x and self.player.grid_y == self.level.goal_y:
                self.game_victory = True

            self.screen.blit(self.renderer.maze_surface, (0, 0))
            self.renderer.draw_player(self.screen, self.player)
            self.renderer.draw_enemy(self.screen, self.enemy)

            pygame.display.flip()
            self.clock.tick(FPS)
    
    def show_game_over(self):
        self.screen.fill((0, 0, 0))

        font = pygame.font.SysFont("Arial", 80)
        text = font.render("GAME OVER", True, (255, 0, 0))

        self.screen.blit(text, (WIDTH//2 - text.get_width()//2,
                                HEIGHT//2 - text.get_height()//2))

        pygame.display.flip()
    
    def show_game_victory(self):
        self.screen.fill((0, 0, 0))

        font = pygame.font.SysFont("Arial", 80)
        text = font.render("VICTORY!", True, (0, 255, 0))

        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2,
                                HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()