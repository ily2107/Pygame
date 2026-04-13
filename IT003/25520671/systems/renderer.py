import pygame
import random
from setting import *

class Renderer:
    def __init__(self,screen):
        self.screen=screen
        self.maze_surface = None

    def draw_wall_block1(self, surface, x, y):
        colors = {
            "1": (10, 45, 18),    # nền xanh rất đậm
            "2": (18, 78, 30),    # xanh đậm
            "3": (28, 120, 45),   # xanh lá
            "4": (55, 170, 70),   # xanh sáng
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

    def draw_wall_block2_1(self, surface, x, y):
        pygame.draw.rect(surface, (98, 150, 58), (x, y, 40, 40))

        outline = (6, 72, 30)
        leaf_dark = (20, 168, 52)
        leaf_mid = (28, 196, 58)
        leaf_light = (64, 230, 82)

        trunk_dark = (90, 52, 28)
        trunk_mid = (122, 74, 42)
        trunk_light = (150, 96, 58)

        pygame.draw.circle(surface, outline, (x + 13, y + 12), 8)
        pygame.draw.circle(surface, outline, (x + 27, y + 12), 8)
        pygame.draw.circle(surface, outline, (x + 20, y + 9), 10)

        pygame.draw.circle(surface, leaf_mid, (x + 13, y + 12), 7)
        pygame.draw.circle(surface, leaf_mid, (x + 27, y + 12), 7)
        pygame.draw.circle(surface, leaf_mid, (x + 20, y + 9), 9)

        pygame.draw.circle(surface, leaf_light, (x + 15, y + 9), 4)
        pygame.draw.circle(surface, leaf_light, (x + 25, y + 10), 4)

        pygame.draw.circle(surface, outline, (x + 10, y + 20), 7)
        pygame.draw.circle(surface, outline, (x + 20, y + 20), 9)
        pygame.draw.circle(surface, outline, (x + 30, y + 20), 7)

        pygame.draw.circle(surface, leaf_dark, (x + 10, y + 20), 6)
        pygame.draw.circle(surface, leaf_dark, (x + 20, y + 20), 8)
        pygame.draw.circle(surface, leaf_dark, (x + 30, y + 20), 6)

        for px in [6, 11, 16, 21, 26, 31]:
            pygame.draw.circle(surface, outline, (x + px, y + 25), 3)
        for px in [7, 12, 17, 22, 27, 32]:
            pygame.draw.circle(surface, leaf_dark, (x + px, y + 24), 2)

        pygame.draw.ellipse(surface, leaf_light, (x + 7, y + 15, 10, 6))
        pygame.draw.ellipse(surface, leaf_light, (x + 17, y + 14, 12, 7))
        pygame.draw.ellipse(surface, leaf_mid,   (x + 24, y + 16, 8, 5))

        pygame.draw.ellipse(surface, (16, 140, 46), (x + 7,  y + 20, 9, 5))
        pygame.draw.ellipse(surface, (16, 140, 46), (x + 18, y + 19, 10, 5))
        pygame.draw.ellipse(surface, (16, 140, 46), (x + 26, y + 21, 7, 4))

        pygame.draw.rect(surface, trunk_dark, (x + 16, y + 22, 8, 12), border_radius=2)
        pygame.draw.rect(surface, trunk_mid,  (x + 17, y + 22, 6, 12), border_radius=2)
        pygame.draw.rect(surface, trunk_light,(x + 19, y + 22, 2, 12), border_radius=1)

        pygame.draw.polygon(surface, trunk_dark, [(x + 16, y + 24), (x + 12, y + 22), (x + 13, y + 21), (x + 17, y + 23)])
        pygame.draw.polygon(surface, trunk_dark, [(x + 24, y + 24), (x + 28, y + 22), (x + 27, y + 21), (x + 23, y + 23)])

        pygame.draw.polygon(surface, trunk_dark, [(x + 16, y + 34), (x + 11, y + 38), (x + 14, y + 38), (x + 18, y + 35)])
        pygame.draw.polygon(surface, trunk_dark, [(x + 24, y + 34), (x + 29, y + 38), (x + 26, y + 38), (x + 22, y + 35)])
        pygame.draw.polygon(surface, trunk_mid,  [(x + 18, y + 34), (x + 20, y + 39), (x + 22, y + 34)])

        pygame.draw.circle(surface, outline, (x + 26, y + 29), 3)
        pygame.draw.circle(surface, leaf_dark, (x + 26, y + 29), 2)

    def draw_wall_block2_2(self, surface, x, y):
        pygame.draw.rect(surface, (98, 150, 58), (x, y, 40, 40))

        outline    = (8, 70, 24)
        leaf_dark  = (92, 192, 18)
        leaf_mid   = (108, 212, 20)
        leaf_light = (132, 228, 32)

        pygame.draw.circle(surface, outline, (x + 14, y + 15), 12)
        pygame.draw.circle(surface, outline, (x + 26, y + 15), 11)
        pygame.draw.circle(surface, outline, (x + 31, y + 16), 8)

        pygame.draw.circle(surface, leaf_mid,   (x + 14, y + 15), 10)
        pygame.draw.circle(surface, leaf_mid,   (x + 26, y + 15), 9)
        pygame.draw.circle(surface, leaf_mid,   (x + 31, y + 16), 6)

        pygame.draw.ellipse(surface, leaf_light, (x + 8,  y + 7, 12, 7))
        pygame.draw.ellipse(surface, leaf_light, (x + 21, y + 8, 10, 6))

        pygame.draw.circle(surface, outline, (x + 12, y + 24), 8)
        pygame.draw.circle(surface, leaf_dark, (x + 12, y + 24), 6)

        pygame.draw.circle(surface, outline, (x + 28, y + 24), 10)
        pygame.draw.circle(surface, leaf_dark, (x + 28, y + 24), 8)

        for cx, cy, r in [
            (x + 6,  y + 29, 3),
            (x + 10, y + 30, 3),
            (x + 14, y + 29, 3),
            (x + 24, y + 31, 3),
            (x + 28, y + 32, 3),
            (x + 32, y + 31, 3),
            (x + 36, y + 30, 3),
        ]:
            pygame.draw.circle(surface, outline, (cx, cy), r)
            pygame.draw.circle(surface, leaf_dark, (cx, cy - 1), max(1, r - 1))

        pygame.draw.ellipse(surface, outline,    (x + 4,  y + 18, 13, 12))
        pygame.draw.ellipse(surface, leaf_dark,  (x + 5,  y + 19, 11, 10))

        pygame.draw.ellipse(surface, outline,    (x + 18, y + 17, 17, 14))
        pygame.draw.ellipse(surface, leaf_dark,  (x + 19, y + 18, 15, 12))

        pygame.draw.ellipse(surface, outline,    (x + 25, y + 17, 11, 11))
        pygame.draw.ellipse(surface, leaf_dark,  (x + 26, y + 18, 9,  9))

        pygame.draw.ellipse(surface, leaf_mid,   (x + 6,  y + 19, 8, 5))
        pygame.draw.ellipse(surface, leaf_mid,   (x + 22, y + 18, 10, 6))
        pygame.draw.ellipse(surface, leaf_light, (x + 24, y + 20, 6, 4))

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
        colors = {
            "1": (98, 150, 58),   # màu chủ đạo
            "2": (118, 170, 76),  # sáng hơn
            "3": (74, 124, 42),   # đậm hơn
            "4": (56, 94, 30),    # rất đậm
        }

        pattern = [
            "11111111111111111111",
            "11211111111111112111",
            "11111131111111111111",
            "11121111111113111111",
            "11111111121111111111",
            "11311111111111111121",
            "11111112111111131111",
            "11111111111111111111",
            "11113111111121111111",
            "11111111111111111111",
            "11111111131111111111",
            "11211111111111112111",
            "11111111111111111111",
            "11111112111111131111",
            "11111111111111111111",
            "11311111111111111121",
            "11111111121111111111",
            "11121111111113111111",
            "11111131111111111111",
            "11111111111111111111",
        ]

        pixel_size = 2   # 20x20 -> 40x40

        for row in range(20):
            for col in range(20):
                c = pattern[row][col]
                pygame.draw.rect(
                    surface,
                    colors[c],
                    (x + col * pixel_size, y + row * pixel_size, pixel_size, pixel_size)
                )

    def draw_maze(self, maze, type):
        self.maze_surface = pygame.Surface((maze.cols * 40, maze.rows * 40))
        arr = [[0 for _ in range(maze.cols)] for _ in range(maze.rows)]
        for x in range(maze.rows):
            for y in range(maze.cols):
                arr[x][y] = random.randint(1,2)

        for x in range(maze.rows):
            for y in range(maze.cols):
                cell=maze.grid[x][y]
                if type == 1:
                    if cell.type=="Wall": 
                        self.draw_wall_block1(self.maze_surface, y*40, x*40)
                    else: 
                        self.draw_path_block1(self.maze_surface, y*40, x*40)
                elif type == 2:
                    if cell.type=="Wall": 
                        if arr[x][y] == 1: self.draw_wall_block2_1(self.maze_surface, y*40, x*40)
                        else: self.draw_wall_block2_2(self.maze_surface, y*40, x*40)
                    else: 
                        self.draw_path_block2(self.maze_surface, y*40, x*40)
                else:
                    if cell.type=="Wall": 
                        if arr[x][y] == 1: self.draw_wall_block2_1(self.maze_surface, y*40, x*40)
                        else: self.draw_wall_block2_2(self.maze_surface, y*40, x*40)
                    else: 
                        self.draw_path_block2(self.maze_surface, y*40, x*40)
                
                