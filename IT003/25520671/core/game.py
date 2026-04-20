import time
import math
import pygame
import random
import importlib
from setting import *
from ui.menu import Menu
from core.maze import Maze
from ui.TutorialOverlay import TutorialOverlay
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
        self.enemy = Enemy(*self.level.enemy_spawn)
        self.randomize_dorayaki()

        self.game_over = False
        self.game_victory = False

        self.renderer = Renderer(self.screen)
        self.renderer.draw_maze(self, self.level.type)

        self.tutorial = TutorialOverlay(self.screen)
        
        self.carry = False
        self.first_pick = False
        self.points = 0
        self.satisfy = False
        self.change = False

        self.alpha = 255
        self.alpha_dir = -5
        self.sun_angle = 0
    
    def run(self):
        self.menu.run()
        while True:
            self.tutorial.show(self.level_cnt,self.renderer)
            self.run_game()

    def randomize_dorayaki(self):
        walkable = []

        for i in range(self.level.maze.rows):
            for j in range(self.level.maze.cols):
                if self.level.maze.is_walkable(i, j) and (i, j) != self.level.player_spawn and (j, i) != (self.level.goal_x, self.level.goal_y):
                    walkable.append((j, i))

        def far(cell):
            return abs(cell[0] - self.level.maze.player_spawn[0]) + abs(cell[1] - self.level.maze.player_spawn[1])
        far_cells = walkable[:len(walkable)]
        positions = random.sample(far_cells, 4)
        self.dorayaki = positions[:3]
        self.doraemon = positions[3]

    def run_game(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            if self.game_over:
                self.show_game_over()
                self.__init__()
                return

            if self.game_victory:
                self.show_game_victory()
                self.load_level()
                return

            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, self.level.maze)
            self.player.update()

            if self.carry or self.points:
                if time.time() - self.last_move > 0.3:
                    self.enemy.update(self.player, self.level.maze)
                    self.last_move = time.time()

            if self.enemy.grid_x == self.player.grid_x and self.enemy.grid_y == self.player.grid_y:
                self.game_over = True

            if self.satisfy and self.player.grid_x == self.level.goal_x and self.player.grid_y == self.level.goal_y:
                self.game_victory = True

            px, py = self.player.grid_x, self.player.grid_y
            for item in self.dorayaki[:]: 
                if self.carry:
                    break
                if item == (py, px):
                    self.dorayaki.remove(item)
                    self.carry = True

            if self.satisfy and self.change == False:
                gx, gy = self.level.goal_x, self.level.goal_y
                self.renderer.maze_surface.blit(self.renderer.exit_open_image, (gx * 40, gy * 40))
                self.change = True

            if self.carry and self.player.grid_x == self.doraemon[1] and self.player.grid_y == self.doraemon[0]:
                self.points +=1
                self.carry = False

            if self.points:
                (gx, gy) = self.doraemon
                if self.level.type == 1:
                    self.renderer.draw_path_block1(self.renderer.maze_surface, gy * 40, gx * 40)
                elif self.level.type == 2:
                    self.renderer.draw_path_block2(self.renderer.maze_surface, gy * 40, gx * 40)
                else:
                    self.renderer.draw_path_block3(self.renderer.maze_surface, gy * 40, gx * 40)
                self.renderer.maze_surface.blit(self.renderer.doraemon_eating_image, (gy * 40, gx * 40))

            if self.points == 3:
                self.satisfy = True

            self.screen.blit(self.renderer.maze_surface, (0, 0))
            self.renderer.draw_player(self.screen, self.player)
            self.renderer.draw_enemy(self.screen, self.enemy)

            self.alpha += self.alpha_dir
            if self.alpha <= 120 or self.alpha >= 255:
                self.alpha_dir *= -1

            self.sun_angle += 2

            img = self.renderer.dorayaki_image.copy()
            img.set_alpha(self.alpha)

            for x, y in self.dorayaki:
                cx = y * 40 + 20
                cy = x * 40 + 20

                for i in range(12):
                    angle = math.radians(i * 30 + self.sun_angle)

                    length1 = 15
                    length2 = 28

                    x1 = cx + math.cos(angle) * length1
                    y1 = cy + math.sin(angle) * length1

                    x2 = cx + math.cos(angle) * length2
                    y2 = cy + math.sin(angle) * length2

                    pygame.draw.line(self.screen, (255, 200, 0), (x1, y1), (x2, y2), 3)

                self.screen.blit(img, (y * 40, x * 40))

            pygame.display.flip()
            self.clock.tick(FPS)
    
    def show_game_over(self):
        self.screen_end = pygame.image.load("assets/anh-chaien-bat-nat-nobita-1747363265477-17473632660221521854822.webp").convert()
        self.screen_end = pygame.transform.scale(self.screen_end, (WIDTH, HEIGHT))
        overlay = pygame.Surface((WIDTH, HEIGHT))

        overlay.set_alpha(100)
        overlay.fill((0, 0, 0)) 

        font_mid = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 80)
        font_mid.set_bold(True)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 40)

        text2 = font_mid.render("JAIAN CAUGHT YOU!", True, (255, 255, 255))
        text3 = font_small.render("PRESS SPACE TO CONTINUE", True, (180, 180, 180))

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over=False
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            self.screen.blit(self.screen_end,(0,0))
            self.screen.blit(overlay,(0,0))

            self.screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 50))
            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            img = text3.copy()
            img.set_alpha(alpha)
            self.screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT - 100))

            pygame.display.update()
        pygame.quit()
    
    def show_game_victory(self):
        self.screen_end = pygame.image.load("assets/8b7728e975e621bb4c5bd3e3729ecc42-17370298636981998921406-1737085019652-1737085019794761591577.webp").convert()
        self.screen_end = pygame.transform.scale(self.screen_end, (WIDTH, HEIGHT))
        overlay = pygame.Surface((WIDTH, HEIGHT))

        overlay.set_alpha(100)
        overlay.fill((0, 0, 0)) 

        font_mid = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 80)
        font_mid.set_bold(True)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 40)

        text2 = font_mid.render("YOU ESCAPED JAIAN!", True, (255, 255, 255))
        text3 = font_small.render("PRESS SPACE TO TRY NEXT LEVEL", True, (180, 180, 180))

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over=False
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            self.screen.blit(self.screen_end,(0,0))
            self.screen.blit(overlay,(0,0))

            self.screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 50))
            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            img = text3.copy()
            img.set_alpha(alpha)
            self.screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT - 100))

            pygame.display.update()
        pygame.quit()
    
    def load_level(self):
        self.level_cnt += 1
        self.last_move = 0

        self.level = importlib.import_module(f"levels.level{self.level_cnt}")
        self.player = Player(*self.level.player_spawn)
        self.enemy = Enemy(*self.level.enemy_spawn)

        self.game_over = False
        self.game_victory = False

        self.renderer = Renderer(self.screen)
        self.renderer.draw_maze(self.level, self.level.type)

        self.tutorial = TutorialOverlay(self.screen)
        
        self.carry = False
        self.first_pick = False
        self.points = 0
        self.satisfy = False
        self.change = False

        self.alpha = 255
        self.alpha_dir = -5
        self.sun_angle = 0
