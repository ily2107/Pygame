import random
import time
import math
import pygame
from setting import *
from core.maze import Maze
from entities.player import Player
from entities.foe.enemy import Enemy

class Level1:
    def __init__(self, game):
        self.game = game

        self.type = 3
        self.map = random.randint(1, 3)

        self.maze = Maze.load_from_txt(f"maps/level1/map{self.map}.txt")

        self.player_spawn = (0, 0)
        self.goal_x = self.maze.cols - 1
        self.goal_y = self.maze.rows - 1

        self.enemy_spawn = self.get_enemy_spawn()

        self.player = Player(*self.player_spawn)
        self.enemy = Enemy(*self.enemy_spawn)

        self.carry = False
        self.points = 0
        self.satisfy = False
        self.change = False

        self.alpha = 255
        self.alpha_dir = -5
        self.sun_angle = 0

        self.tutorial_data = {
            "lines": [
                "Collect Dorayaki and give them to Doraemon",
                "Get enough to unlock the Magic Door and escape!",
                "Avoid Jaian!"
            ],
            "note": "Note: You can carry only one Dorayaki at a time."
        }
        self.randomize_dorayaki()

    def get_enemy_spawn(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y)):
                    walkable.append((j, i))

        def far(cell):
            return abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1])

        walkable.sort(key=far, reverse=True)

        enemy = walkable[:len(walkable) // 4]

        return enemy[0]

    def randomize_dorayaki(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y) and (i, j) != self.enemy_spawn): 
                    walkable.append((j, i))

        def far_doraemon(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]),
            )

        def far_dorayaki(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.doraemon[0]) + abs(cell[1] - self.doraemon[1]),
                abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]),
            )

        far_cells = sorted(walkable, key=far_doraemon, reverse=True)
        positions = random.sample(far_cells[:len(far_cells) // 2], 1)
        self.doraemon = positions[0]

        far_cells = sorted(walkable, key=far_dorayaki, reverse=True)
        positions = random.sample(far_cells[:len(far_cells)], 3)
        self.dorayaki = positions[:3]
        

    def update(self, events, screen, renderer):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game.pause_button_rect and self.game.pause_button_rect.collidepoint(event.pos):
                        result = self.game.handle_pause_menu()

                        if result == "menu":
                            return "menu"
                        
        keys = pygame.key.get_pressed()

        self.player.handle_input(keys, self.maze)
        self.player.update()

        if self.carry or self.points:
            if time.time() - self.enemy.last_move > 0.4 - (self.carry + self.points) * 0.05:
                self.enemy.update(self.player, self.maze)
                self.enemy.last_move = time.time()

        if (self.enemy.grid_x == self.player.grid_x and self.enemy.grid_y == self.player.grid_y):
            self.game.game_over = True

        if (self.satisfy and self.player.grid_x == self.goal_x and self.player.grid_y == self.goal_y):
            self.game.game_victory = True

        px = self.player.grid_x
        py = self.player.grid_y

        for item in self.dorayaki[:]:
            if self.carry:
                break

            if item == (py, px):
                self.dorayaki.remove(item)
                self.carry = True

        if (self.carry and self.player.grid_x == self.doraemon[1] and self.player.grid_y == self.doraemon[0]):
            self.points += 1
            self.carry = False

        if self.points == 3:
            self.satisfy = True

    def draw_five_point_star(self, screen, x, y, outer=9, inner=4, color=(255, 255, 255)):
        points = []
        start = -math.pi / 2

        for i in range(10):
            angle = start + i * math.pi / 5
            r = outer if i % 2 == 0 else inner
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))

        pygame.draw.polygon(screen, color, points)


    def draw_magic_border(self, screen):
        maze_x = OFFSET
        maze_y = OFFSET
        maze_w = self.maze.cols * 30
        maze_h = self.maze.rows * 30

        gap = 15
        corner_gap = 36

        left = maze_x - gap
        top = maze_y - gap
        right = maze_x + maze_w + gap
        bottom = maze_y + maze_h + gap

        color = (255, 255, 255)
        width = 2

        pygame.draw.line(screen, color, (left + corner_gap, top), (right - corner_gap, top), width)
        pygame.draw.line(screen, color, (left + corner_gap, bottom), (right - corner_gap, bottom), width)
        pygame.draw.line(screen, color, (left, top + corner_gap), (left, bottom - corner_gap), width)
        pygame.draw.line(screen, color, (right, top + corner_gap), (right, bottom - corner_gap), width)

        self.draw_five_point_star(screen, left + 10, top + 10, 8, 3, color)
        self.draw_five_point_star(screen, right - 10, top + 10, 8, 3, color)
        self.draw_five_point_star(screen, left + 10, bottom - 10, 8, 3, color)
        self.draw_five_point_star(screen, right - 10, bottom - 10, 8, 3, color)

        self.draw_five_point_star(screen, left + 40, top + 8, 4, 2, color)
        self.draw_five_point_star(screen, right - 40, top + 8, 4, 2, color)
        self.draw_five_point_star(screen, left + 40, bottom - 8, 4, 2, color)
        self.draw_five_point_star(screen, right - 40, bottom - 8, 4, 2, color)

    def draw_side_frame(self, screen):
        margin = 30
        maze_border_gap = 30

        maze_x = OFFSET
        maze_y = OFFSET
        maze_w = self.maze.cols * 30
        maze_h = self.maze.rows * 30

        x = maze_x + maze_w + maze_border_gap
        y = margin
        w = WIDTH - x - margin
        h = HEIGHT - margin * 2

        if w <= 0 or h <= 0:
            return

        color = (255, 255, 255)
        width = 2

        radius = 12

        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (5, 7, 12, 220), (0, 0, w, h), border_radius=radius)
        screen.blit(panel, (x, y))

        pygame.draw.rect(screen, color, (x, y, w, h), width, border_radius=radius)

        return pygame.Rect(x, y, w, h)

    def draw(self, renderer, screen):
        screen.blit(renderer.background, (0, 0))

        dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 90))
        screen.blit(dark_overlay, (0, 0))

        self.draw_magic_border(screen)
        panel_rect = self.draw_side_frame(screen)

        if panel_rect:
            self.game.draw_pause_button(screen, panel_rect, renderer, self)

        if self.satisfy and self.change == False:
            gx = self.goal_x
            gy = self.goal_y

            renderer.maze_surface.blit(renderer.exit_open_image, (gx * 30, gy * 30))

            self.change = True

        if self.points:
            gx, gy = self.doraemon

            if self.type == 1:
                renderer.draw_path_block1(renderer.maze_surface, gy * 30, gx * 30)

            elif self.type == 2:
                renderer.draw_path_block2(renderer.maze_surface, gy * 30, gx * 30)

            else:
                renderer.draw_path_block3(renderer.maze_surface, gy * 30, gx * 30)

            renderer.maze_surface.blit(renderer.doraemon_eating_image, (gy * 30, gx * 30))

        screen.blit(renderer.maze_surface, (OFFSET, OFFSET))

        renderer.draw_player(screen, self.player)

        renderer.draw_enemy(screen, self.enemy)

        self.alpha += self.alpha_dir

        if self.alpha <= 120 or self.alpha >= 255:
            self.alpha_dir *= -1

        self.sun_angle += 2

        img = renderer.dorayaki_image.copy()
        img.set_alpha(self.alpha)

        for x, y in self.dorayaki:
            cx = y * 30 + 15
            cy = x * 30 + 15

            for i in range(12):
                angle = math.radians(i * 30 + self.sun_angle)

                length1 = 11
                length2 = 21

                x1 = cx + math.cos(angle) * length1
                y1 = cy + math.sin(angle) * length1

                x2 = cx + math.cos(angle) * length2
                y2 = cy + math.sin(angle) * length2

                pygame.draw.line(screen, (255, 200, 0), (OFFSET + x1, OFFSET + y1), (OFFSET + x2, OFFSET + y2), 3)

            screen.blit(img, (OFFSET + y * 30, OFFSET + x * 30))

    def show_tutorial(self, screen, renderer, data):
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 32)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 26)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        box_w, box_h = 720, 480
        box_x = (WIDTH - box_w) // 2
        box_y = (HEIGHT - box_h) // 2

        title = font_big.render("LEVEL 1", True, (255, 255, 0))

        lines = [font_small.render(line, True, (255,255,255)) for line in data["lines"]]

        note_text = None
        if "note" in data:
            note_text = font_note.render(data["note"], True, (150,150,150))

        press_text = font_small.render("Press SPACE to start", True, (200, 200, 200))

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    
            screen.blit(renderer.background, (0, 0))
            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (200, 200, 200), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            screen.blit(title, (WIDTH//2 - title.get_width()//2, box_y + 50))

            y = box_y + 140
            for line in lines:
                screen.blit(line, (WIDTH//2 - line.get_width()//2, y))
                y += 50

            if note_text:
                screen.blit(note_text, (WIDTH//2 - note_text.get_width()//2, y))
                y += 60

            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            img = press_text.copy()
            img.set_alpha(alpha)

            screen.blit(img, (WIDTH//2 - img.get_width()//2, box_y + 360))

            pygame.display.flip()