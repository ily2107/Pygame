import pygame
import random
from setting import *

class Renderer:
    def __init__(self,screen):
        self.screen=screen
        self.maze_surface = None

        wall_image2_1 = pygame.image.load("assets/Screenshot 2026-04-14 163254.png").convert_alpha()
        wall_image2_2 = pygame.image.load("assets/Screenshot 2026-04-14 163322.png").convert_alpha()
        wall_image2_3 = pygame.image.load("assets/Screenshot 2026-04-14 163555.png").convert_alpha()
        wall_image2_4 = pygame.image.load("assets/Screenshot 2026-04-14 160239.png").convert_alpha()
        
        wall_image2_1 = pygame.transform.scale(wall_image2_1, (25, 25))
        wall_image2_2 = pygame.transform.scale(wall_image2_2, (25, 25))
        wall_image2_3 = pygame.transform.scale(wall_image2_3, (25, 25))
        wall_image2_4 = pygame.transform.scale(wall_image2_4, (25, 25))

        self.wall_images2 = [wall_image2_1, wall_image2_2, wall_image2_3, wall_image2_4]
        
        for i in range(4):
            img = pygame.transform.scale(self.wall_images2[i], (25, 25))

            mask = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255,255,255), (0,0,25,25), border_radius=6)

            img.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            self.wall_images2[i] = img

        self.path_image2 = pygame.image.load("assets/Screenshot 2026-04-14 162414.png").convert_alpha()
        self.path_image2 = pygame.transform.scale(self.path_image2, (30, 30))

        self.path_image3 = pygame.image.load("assets/0e5aa738-90d6-4d47-909c-75c6a6e88d50.png").convert_alpha()
        self.path_image3.set_colorkey((0, 0, 0))
        self.path_image3 = pygame.transform.scale(self.path_image3, (31, 31))

        self.exit_close_image = pygame.image.load("assets/ChatGPT Image Apr 16, 2026, 03_53_08 PM.png").convert_alpha()
        self.exit_close_image.set_colorkey((0, 0, 0))
        self.exit_close_image = pygame.transform.scale(self.exit_close_image, (30, 37))

        self.exit_open_image = pygame.image.load("assets/ChatGPT Image Apr 16, 2026, 03_06_34 PM.png").convert_alpha()
        self.exit_open_image.set_colorkey((0, 0, 0))
        self.exit_open_image = pygame.transform.scale(self.exit_open_image, (30, 37))

        self.doraemon_image = pygame.image.load("assets/Doraemon_character.png").convert_alpha()
        self.doraemon_image.set_colorkey((0, 0, 0))
        self.doraemon_image = pygame.transform.scale(self.doraemon_image, (30, 30))

        self.doraemon_eating_image = pygame.image.load("assets/1293-con-so-may-man-cua-doraemon-583174.png").convert_alpha()
        self.doraemon_eating_image.set_colorkey((0, 0, 0))
        self.doraemon_eating_image = pygame.transform.scale(self.doraemon_eating_image, (30, 30))

        self.dorayaki_image = pygame.image.load("assets/ChatGPT Image Apr 16, 2026, 04_23_13 PM.png").convert_alpha()
        self.dorayaki_image.set_colorkey((0, 0, 0))
        self.dorayaki_image = pygame.transform.scale(self.dorayaki_image, (30, 30))

        self.paper_image = [
            pygame.transform.scale(pygame.image.load(path).convert_alpha(), (30, 30))
            for path in [
                "assets/d3ed1459-e77e-43eb-89e8-7d87eae58ee0.png",
                "assets/ChatGPT Image May 8, 2026, 08_53_44 PM.png",
                "assets/ChatGPT Image May 10, 2026, 12_49_43 AM.png"
            ]
        ]

        for img in self.paper_image:
            img.set_colorkey((0, 0, 0))

        self.miniboss_image = pygame.image.load("assets/1746526097210886618017-1746586971234-1746586971322469050790.png").convert_alpha()
        self.miniboss_image.set_colorkey((0, 0, 0))
        self.miniboss_image = pygame.transform.scale(self.miniboss_image, (30, 30))

        self.player_image = pygame.image.load("assets/nobita4 (1)-Picsart-AiImageEnhancer.png").convert_alpha()
        self.player_image.set_colorkey((0, 0, 0))
        self.player_image = pygame.transform.scale(self.player_image, (30, 30))

        self.enemy_image = pygame.image.load("assets/anh-chaien-dang-tuc-gian-1747363266910-17473632669.png").convert()
        self.enemy_image.set_colorkey((0, 0, 0))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (30, 30))

        self.support_enemy_image = pygame.image.load("assets/anh-suneo-02_preview_rev_1.png").convert_alpha()
        self.support_enemy_image.set_colorkey((0, 0, 0))
        self.support_enemy_image = pygame.transform.scale(self.support_enemy_image, (30, 30))

        self.background = pygame.image.load("assets/image001-16529546221552020285475.webp").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.home_image = pygame.image.load("assets/nobitahouseon2015movie-1467131929535.png").convert()
        self.home_image.set_colorkey((0, 0, 0))
        self.home_image = pygame.transform.scale(self.home_image, (30, 30))

        self.item_image1 = pygame.image.load("assets/Ma_Ma_Boo.PNG.jpg").convert()
        self.item_image2 = pygame.image.load("assets/Gi3Fi_z3F_z3F_t%3Fk.webp").convert()
        self.item_image3 = pygame.image.load("assets/Vongxuyenthau.webp").convert()

    def draw_wall_block1(self, surface, x, y):
        colors = {
            "1": (10, 45, 18), 
            "2": (18, 78, 30),    
            "3": (28, 120, 45),  
            "4": (55, 170, 70),  
        }

        pattern = [
            "112222222332222332222322322211",
            "112222222332222332222322322211",
            "222333333443333443333433433322",
            "222333333443333443333433433322",
            "233344444344444344444344433322",
            "333344442233333223333222344333",
            "333344442233333223333222344333",
            "224333333444433344444333333422",
            "333344444333333444333333444333",
            "333344444333333444333333444333",
            "222333333222333332222333333222",
            "223334444443334444433444443322",
            "223334444443334444433444443322",
            "333344333322333332233333344333",
            "224333444443344444333444433422",
            "224333444443344444333444433422",
            "333344222333322333322222333433",
            "222333334444433444443433333222",
            "222333334444433444443433333222",
            "233344444333333222333344444322",
            "333344333344444333444433333433",
            "333344333344444333444433333433",
            "224333322333333223333222333422",
            "333344444443334444433444444333",
            "333344444443334444433444444333",
            "222333333332233333223333333222",
            "223334444443344444333444433322",
            "223334444443344444333444433322",
            "222333333443333443333433433322",
            "112222222332222332222322322211",
        ]

        for row in range(30):
            for col in range(30):
                c = pattern[row][col]
                pygame.draw.rect(surface, colors[c], (x + col, y + row, 1, 1))

    def draw_wall_block2(self, surface, x, y, type):
        pygame.draw.rect(surface, (128, 196, 28), (x, y, 30, 30))
        shadow = pygame.Surface((30, 30), pygame.SRCALPHA)

        pygame.draw.rect(shadow, (0, 0, 0, 10), (0, 0, 30, 15))
        pygame.draw.rect(shadow, (0, 0, 0, 30), (0, 15, 30, 15))
        
        rect = self.wall_images2[type].get_rect(center=(x + 15, y + 15))
        surface.blit(self.wall_images2[type], rect)
        surface.blit(shadow, (x, y))

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
            "112222223222222222332222222221",
            "112222223222222222332222222221",
            "222333334333332223334333334332",
            "223334443444443334443444443332",
            "223334443444443334443444443332",
            "333443222333334443333222334333",
            "224333333444443333444443333442",
            "224333333444443333444443333442",
            "333444443333334443333334444333",
            "222333332222333332222333333222",
            "222333332222333332222333333222",
            "223334444333444443334444443332",
            "333443333222333332223333334333",
            "333443333222333332223333334333",
            "224333444443334444333444333442",
            "333442223333222333332222333443",
            "333442223333222333332222333443",
            "222333334444333444443443333222",
            "223334443333332223333334444332",
            "223334443333332223333334444332",
            "333443333444443334444333333443",
            "224333222333332223333222333442",
            "224333222333332223333222333442",
            "333444444333444443334444444333",
            "222333333222333332223333333222",
            "222333333222333332223333333222",
            "223334444443334444333444443332",
            "222333334333334333334333334332",
            "222333334333334333334333334332",
            "112222223222223222222332223221",
        ]

        for row in range(30):
            for col in range(30):
                c = pattern[row][col]
                pygame.draw.rect(surface, colors[c], (x + col, y + row, 1, 1))

    def draw_path_block1(self, surface, x, y):
        colors = {
            "1": (55, 55, 55),   
            "2": (75, 75, 75),   
            "3": (95, 95, 95),   
            "4": (120, 120, 120),
        }

        pattern = [
            "111111111111111111111111111111",
            "111111111111111111111111111111",
            "112222222222222222222222222221",
            "112332222222223222222222222221",
            "112332222222223222222222222221",
            "112222222222222222222224222221",
            "112222223222222222222222222221",
            "112222223222222222222222222221",
            "112222222222222222332222222221",
            "112222222442222222222222222221",
            "112222222442222222222222222221",
            "112222222222222223222222222221",
            "112222222222222222222222222221",
            "112222222222222222222222222221",
            "112222332222222222222222222221",
            "112222222222222222224222222221",
            "112222222222222222224222222221",
            "112222222222222222222223222221",
            "112222222222332222222222222221",
            "112222222222332222222222222221",
            "112222222222222222222222222221",
            "112224222222222222223222222221",
            "112224222222222222223222222221",
            "112222222222222222222222222221",
            "112222222332222222222222222221",
            "112222222332222222222222222221",
            "112222222222222222222224222221",
            "112222222222222222222222222221",
            "112222222222222222222222222221",
            "111111111111111111111111111111",
        ]

        for row in range(30):
            for col in range(30):
                c = pattern[row][col]
                pygame.draw.rect(surface, colors[c], (x + col, y + row, 1, 1))

    def draw_path_block2(self, surface, x, y):
        grass = [
            (118, 186, 20),
            (108, 172, 16),
            (98, 160, 12),
            (128, 196, 28),
        ]

        base = (108, 172, 16)
        pygame.draw.rect(surface, base, (x, y, 30, 30))

        for _ in range(45):
            gx = random.randint(0, 29)
            gy = random.randint(0, 29)

            w = random.randint(2, 4)
            h = random.randint(1, 3)

            color = random.choice(grass)

            pygame.draw.rect(surface, color, (x + gx, y + gy, w, h))
    
    def draw_path_block3(self, surface, x, y):
        pygame.draw.rect(surface, (64, 158, 180), (x, y, 30, 30))
        surface.blit(self.path_image3, (x, y))

    def draw_maze(self, game, type):
        self.maze_surface = pygame.Surface((game.maze.cols * 30, game.maze.rows * 30))
        arr = [[0 for _ in range(game.maze.cols)] for _ in range(game.maze.rows)]
        for x in range(game.maze.rows):
            for y in range(game.maze.cols):
                arr[x][y] = random.randint(0,3)

        for x in range(game.maze.rows):
            for y in range(game.maze.cols):
                cell=game.maze.grid[x][y]
                if type == 1:
                    if cell.type=="Wall": 
                        self.draw_wall_block1(self.maze_surface, y * 30, x * 30)
                    else: 
                        self.draw_path_block1(self.maze_surface, y * 30, x * 30)
                elif type == 2:
                    if cell.type=="Wall": 
                        self.draw_wall_block2(self.maze_surface, y * 30, x * 30, arr[x][y])
                    else: 
                        self.draw_path_block2(self.maze_surface, y * 30, x * 30)
                else:
                    if cell.type=="Wall": 
                        self.draw_wall_block3(self.maze_surface, y * 30, x * 30)
                    else: 
                        self.draw_path_block3(self.maze_surface, y * 30, x * 30)
        
        self.maze_surface.blit(self.exit_close_image, (game.goal_x * 30, game.goal_y * 30))
        if game.game.level_cnt != 3:
            self.maze_surface.blit(self.doraemon_image, (game.doraemon[1] * 30, game.doraemon[0] * 30))
                
    def draw_player(self, surface, player):
        surface.blit(self.player_image, (OFFSET + player.px, OFFSET + player.py))

    def draw_enemy(self, surface, enemy):
        surface.blit(self.enemy_image, (OFFSET + enemy.px, OFFSET + enemy.py))

    def draw_support_enemy(self, surface, support_enemy):
        surface.blit(self.support_enemy_image, (OFFSET + support_enemy.px, OFFSET + support_enemy.py))

    def draw_miniboss(self, surface, miniboss):
        surface.blit(self.miniboss_image, (OFFSET + miniboss.px, OFFSET + miniboss.py))

    def draw_home(self, surface, home):
        surface.blit(self.home_image, (OFFSET + home[0] * 30, OFFSET + home[1] * 30))