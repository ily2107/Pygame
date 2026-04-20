import pygame
import random
from setting import *

class Renderer:
    def __init__(self,screen):
        self.screen=screen
        self.maze_surface = None

        self.exit_close_image = pygame.image.load("assets/ChatGPT Image Apr 16, 2026, 03_53_08 PM.png").convert_alpha()
        self.exit_close_image.set_colorkey((0, 0, 0))
        self.exit_close_image = pygame.transform.scale(self.exit_close_image, (40, 50))

        self.exit_open_image = pygame.image.load("assets/ChatGPT Image Apr 16, 2026, 03_06_34 PM.png").convert_alpha()
        self.exit_open_image.set_colorkey((0, 0, 0))
        self.exit_open_image = pygame.transform.scale(self.exit_open_image, (40, 50))

        self.doraemon_image = pygame.image.load("assets/Doraemon_character.png").convert_alpha()
        self.doraemon_image.set_colorkey((0, 0, 0))
        self.doraemon_image = pygame.transform.scale(self.doraemon_image, (40, 40))

        self.doraemon_eating_image = pygame.image.load("assets/1293-con-so-may-man-cua-doraemon-583174.png").convert_alpha()
        self.doraemon_eating_image.set_colorkey((0, 0, 0))
        self.doraemon_eating_image = pygame.transform.scale(self.doraemon_eating_image, (40, 40))

        self.dorayaki_image = pygame.image.load("assets/ChatGPT Image Apr 16, 2026, 04_23_13 PM.png").convert_alpha()
        self.dorayaki_image.set_colorkey((0, 0, 0))
        self.dorayaki_image = pygame.transform.scale(self.dorayaki_image, (40, 40))

        wall_image2_1 = pygame.image.load("assets/Screenshot 2026-04-14 163254.png").convert_alpha()
        wall_image2_2 = pygame.image.load("assets/Screenshot 2026-04-14 163322.png").convert_alpha()
        wall_image2_3 = pygame.image.load("assets/Screenshot 2026-04-14 163555.png").convert_alpha()
        wall_image2_4 = pygame.image.load("assets/Screenshot 2026-04-14 160239.png").convert_alpha()
        
        wall_image2_1 = pygame.transform.scale(wall_image2_1, (40, 40))
        wall_image2_2 = pygame.transform.scale(wall_image2_2, (40, 40))
        wall_image2_3 = pygame.transform.scale(wall_image2_3, (40, 40))
        wall_image2_4 = pygame.transform.scale(wall_image2_4, (40, 40))

        self.wall_images2 = [wall_image2_1, wall_image2_2, wall_image2_3, wall_image2_4]

        self.path_image2 = pygame.image.load("assets/Screenshot 2026-04-14 162414.png").convert_alpha()
        self.path_image2 = pygame.transform.scale(self.path_image2, (40, 40))

        self.path_image3 = pygame.image.load("assets/0e5aa738-90d6-4d47-909c-75c6a6e88d50.png").convert_alpha()
        self.path_image3.set_colorkey((0, 0, 0))
        self.path_image3 = pygame.transform.scale(self.path_image3, (42, 42))

        self.player_image = pygame.image.load("assets/nobita4 (1)-Picsart-AiImageEnhancer.png").convert_alpha()
        self.player_image.set_colorkey((0, 0, 0))
        self.player_image = pygame.transform.scale(self.player_image, (40, 40))

        self.enemy_image = pygame.image.load("assets/anh-chaien-dang-tuc-gian-1747363266910-17473632669.png").convert()
        self.enemy_image.set_colorkey((0, 0, 0))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (40, 40))

    def draw_wall_block1(self, surface, x, y):
        colors = {
            "1": (10, 45, 18), 
            "2": (18, 78, 30),    
            "3": (28, 120, 45),  
            "4": (55, 170, 70),  
        }

        pattern = [
            "12222322232222322321",
            "22333433343334333432",
            "23344344434443444332",
            "33432233322333223433",
            "24333344433344433342",
            "33444333344333344433",
            "22333222333222333322",
            "23344433444334444332",
            "33433322333223333433",
            "24334443344433443342",
            "33422333223332223343",
            "22333444334443433322",
            "23344333322333344432",
            "33433344433444333343",
            "24332233322333223342",
            "33444433444334444433",
            "22333322333223333322",
            "23344443344433444332",
            "22333433343334333432",
            "12222322232222322321",
        ]

        for row in range(20):
            for col in range(20):
                c = pattern[row][col]
                pygame.draw.rect(surface, colors[c], (x + 2 * col, y + 2 * row, 2, 2))

    def draw_wall_block2(self, surface, x, y, type):
        surface.blit(self.wall_images2[type], (x, y))

    def draw_wall_block3(self, surface, x, y):
        colors = {
            "1": (32, 110, 140),
            "2": (64, 158, 180),
            "3": (46, 134, 160),
            "4": (56, 146, 170),
            "5": (76, 172, 192),
            "6": (88, 184, 202),
        }

        pattern = [
            "12222322222232222221",
            "22333433322334333432",
            "23344344433443444332",
            "33432233344333223433",
            "24333344433344433342",
            "33444333344333344433",
            "22333222333222333322",
            "23344433444334444332",
            "33433322333223333433",
            "24334443344433443342",
            "33422333223332223343",
            "22333444334443433322",
            "23344333322333344432",
            "33433344433444333343",
            "24332233322333223342",
            "33444433444334444433",
            "22333322333223333322",
            "23344443344433444332",
            "22333433343334333432",
            "12222322232222322321",
        ]

        pixel_size = 2

        for row in range(20):
            for col in range(20):
                c = pattern[row][col]
                pygame.draw.rect(
                    surface,
                    colors[c],
                    (x + col * pixel_size, y + row * pixel_size, pixel_size, pixel_size)
                )

    def draw_path_block1(self, surface, x, y):
        colors = {
            "1": (55, 55, 55),   
            "2": (75, 75, 75),   
            "3": (95, 95, 95),   
            "4": (120, 120, 120),
        }

        pattern = [
            "11111111111111111111",
            "12222222222222222221",
            "12322222232222222221",
            "12222222222222242221",
            "12222322222222222221",
            "12222222222232222221",
            "12222242222222222221",
            "12222222222322222221",
            "12222222222222222221",
            "12223222222222222221",
            "12222222222224222221",
            "12222222222222232221",
            "12222222322222222221",
            "12222222222222222221",
            "12242222222223222221",
            "12222222222222222221",
            "12222232222222222221",
            "12222222222222242221",
            "12222222222222222221",
            "11111111111111111111",
        ]

        for row in range(20):
            for col in range(20):
                c = pattern[row][col]
                pygame.draw.rect(surface, colors[c], (x + 2 * col, y + 2 * row, 2, 2))

    def draw_path_block2(self, surface, x, y):
        pygame.draw.rect(surface, (148, 218, 0), (x, y, 40, 40))
        surface.blit(self.path_image2, (x, y))
    
    def draw_path_block3(self, surface, x, y):
        pygame.draw.rect(surface, (64, 158, 180), (x, y, 40, 40))
        surface.blit(self.path_image3, (x, y))

    def draw_maze(self, game, type):
        self.maze_surface = pygame.Surface((game.level.maze.cols * 40, game.level.maze.rows * 40))
        arr = [[0 for _ in range(game.level.maze.cols)] for _ in range(game.level.maze.rows)]
        for x in range(game.level.maze.rows):
            for y in range(game.level.maze.cols):
                arr[x][y] = random.randint(0,3)

        for x in range(game.level.maze.rows):
            for y in range(game.level.maze.cols):
                cell=game.level.maze.grid[x][y]
                if type == 1:
                    if cell.type=="Wall": 
                        self.draw_wall_block1(self.maze_surface, y * 40, x * 40)
                    else: 
                        self.draw_path_block1(self.maze_surface, y * 40, x * 40)
                elif type == 2:
                    if cell.type=="Wall": 
                        self.draw_wall_block2(self.maze_surface, y * 40, x * 40, arr[x][y])
                    else: 
                        self.draw_path_block2(self.maze_surface, y * 40, x * 40)
                else:
                    if cell.type=="Wall": 
                        self.draw_wall_block3(self.maze_surface, y * 40, x * 40)
                    else: 
                        self.draw_path_block3(self.maze_surface, y * 40, x * 40)
        
        self.maze_surface.blit(self.exit_close_image, (game.level.goal_x * 40, game.level.goal_y * 40))
        self.maze_surface.blit(self.doraemon_image, (game.doraemon[1] * 40, game.doraemon[0] * 40))
                
    def draw_player(self, surface, player):
        surface.blit(self.player_image, (player.px, player.py))

    def draw_enemy(self, surface, enemy):
        surface.blit(self.enemy_image, (enemy.px, enemy.py))
