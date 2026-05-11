import random
import time
import math
import pygame
from setting import *
from core.maze import Maze
from entities.player import Player
from entities.foe.enemy import Enemy
from entities.foe.catch import Catch
from entities.foe.miniboss import MiniBoss
from entities.foe.support_enemy import Support_enemy

class Level2:
    def __init__(self, game):
        self.game = game

        self.type = 1
        self.map = random.randint(1, 3)

        self.maze = Maze.load_from_txt(f"maps/level2/map{self.map}.txt")

        self.player_spawn = (0, 0)
        self.goal_x = self.maze.cols - 1
        self.goal_y = self.maze.rows - 1

        self.enemy_spawn = self.get_enemy_spawn()
        self.miniboss_spawn = self.get_miniboss_spawn()
        self.home = self.get_home()

        self.player = Player(*self.player_spawn)
        self.enemy = Enemy(*self.enemy_spawn)
        self.miniboss = MiniBoss(*self.miniboss_spawn)

        self.randomize()
        self.random_paper()

        self.support_enemy_spawn = self.get_support_enemy_spawn()
        self.support_enemy = Support_enemy(*self.support_enemy_spawn)

        self.carry = False
        self.points = 0
        self.satisfy = False
        self.change = False

        self.count_down = 0
        self.respond = False
        self.close = False

        self.alpha = 255
        self.alpha_dir = -5
        self.sun_angle = 0
        self.last_move = 0

        self.catch = Catch()
        self.be_catch = False
        self.detained = 0

        self.end = False
        self.img = []
        self.item_image = pygame.image.load("assets/Ma_Ma_Boo.PNG.jpg").convert_alpha()

        self.tutorial_data = {
            "pages": [
                {
                    "title": "LEVEL 2",
                    "lines": [
                        "Complete all tasks and escape!",
                        "Something has changed in this maze...",
                    ]
                },

                {
                    "title": "NEW ENEMY",
                    "lines": [
                        "Suneo patrols around the maze and will detain you",
                        "when he spots you.",
                    ],
                    "note": "Try to escape quickly, or you will be detained for 5 seconds."
                }
            ]
        }

        self.note_data = {
            "title": "EVENT BOSS",

            "lines": [
                "Stop the Teacher from reaching Nobita's house",
                "Use Doraemon's gadgets wisely to complete the mission"
            ],

            "note": "If the Teacher catches you, you will lose"
        }

    def get_support_enemy_spawn(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(j, i) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y)) and (i, j) != self.enemy_spawn:
                    walkable.append((j, i))

        def far(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.doraemon[0]) + abs(cell[1] - self.doraemon[1]),
                abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]),
            )

        walkable.sort(key=far, reverse=True)

        return walkable[0]
    
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

    def get_miniboss_spawn(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y)):
                    walkable.append((j, i))

        def far(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.goal_y) + abs(cell[1] - self.goal_x),
            )
        
        walkable.sort(key=far, reverse=True)

        miniboss = walkable[:len(walkable) // 4]

        return miniboss[0]

    def get_home(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if self.maze.is_walkable(i, j) and (j, i) != (self.goal_x, self.goal_y):
                    walkable.append((j, i))

        def far(cell):
            return abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1])

        walkable.sort(key=far, reverse=True)

        home = walkable[:len(walkable) // 4]

        return home[0]

    def randomize(self):
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

        far_cells = sorted(walkable, key=far_doraemon, reverse=True)
        positions = random.sample(far_cells[:len(far_cells) // 2], 1)
        self.doraemon = positions[0]

        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y) and (j, i) != self.doraemon and (i, j) != self.enemy_spawn): 
                    walkable.append((j, i))

        def far_dorayaki(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.doraemon[0]) + abs(cell[1] - self.doraemon[1]),
                abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]),
            )

        far_cells = sorted(walkable, key=far_dorayaki, reverse=True)
        positions = random.sample(far_cells[:len(far_cells)], 3)
        self.dorayaki = positions[:3]
    
    def random_paper(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (j, i) != (self.goal_x, self.goal_y) and (i, j) != self.enemy_spawn): 
                    walkable.append((j, i))

        def far(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]),
            )

        far_cells = sorted(walkable, key=far, reverse=True)
        positions = random.sample(far_cells[:len(far_cells)], 3)
        self.paper = positions[:3]
        
    def update(self, events, screen, renderer):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game.pause_button_rect and self.game.pause_button_rect.collidepoint(event.pos):
                        result = self.game.handle_pause_menu()

                        if result == "menu":
                            return "menu"
                
        if self.be_catch:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.catch.on_press()

            self.catch.update()
            if not self.catch.active:
                self.be_catch = False

                if not self.catch.failed:
                    self.support_enemy.daze = 180
                else: self.detained = 300
        else:
            keys = pygame.key.get_pressed()
            
            if not self.detained:
                self.player.handle_input(keys, self.maze)
                self.player.update()

            if self.carry or self.points or self.close:
                if time.time() - self.enemy.last_move > 0.5 - 0.15 * self.close - (self.carry + self.points) * 0.05:
                    self.enemy.update(self.player, self.maze)
                    self.enemy.last_move = time.time()

            if ((self.points and self.close == False) or self.close) and self.support_enemy.daze==0 and self.detained == 0:
                self.support_enemy.update(self.player, self.maze)

            if self.enemy.grid_x == self.player.grid_x and self.enemy.grid_y == self.player.grid_y:
                self.game.game_over = True

            if self.points and self.support_enemy.grid_x == self.player.grid_x and self.support_enemy.grid_y == self.player.grid_y and self.support_enemy.daze == 0 and self.detained == 0:
                self.get_catch()

            if self.satisfy and self.player.grid_x == self.goal_x and self.player.grid_y == self.goal_y:
                self.game.game_victory = True

            px, py = self.player.grid_x, self.player.grid_y

            for item in self.dorayaki[:]:
                if self.carry:
                    break

                if item == (py, px):
                    self.dorayaki.remove(item)
                    self.carry = True

            if (self.carry and self.player.grid_x == self.doraemon[1] and self.player.grid_y == self.doraemon[0]):
                self.points += 1
                self.carry = False

            if self.points == 3 and self.close == False and self.count_down == 0:
                self.satisfy = True
                self.player.inventory.append("tranquillizer_tick")
                self.show_first_pick_item(screen, renderer, self.item_image)
                self.count_down = 180

            if self.count_down > 0:
                self.count_down -= 1
                if self.count_down == 0:
                    warning = pygame.image.load("assets/Screenshot 2026-05-10 131018.png").convert_alpha()
                    warning = pygame.transform.scale(warning, (960, 200))

                    self.show_warning(screen, self.game.clock, warning, renderer)
                    self.show_note(screen, renderer, self.note_data)
                    self.respond = True
                    self.satisfy = False
                    self.close = True

            if self.respond and not self.end:
                if pygame.time.get_ticks() % 30 == 0:
                    target = (self.home[0], self.home[1])
                    self.miniboss.go_to(target, self.maze)

                if (self.miniboss.grid_x == self.home[0] and self.miniboss.grid_y == self.home[1]) or (self.miniboss.grid_x == self.player.grid_x and self.miniboss.grid_y == self.player.grid_y):
                    self.game.game_over = True

                if "tranquillizer_tick" in self.player.inventory:
                    def get_range(a, b, x, y):
                        if abs(a - x) == 0 and abs(b - y) <= 2:
                            return True
                        if abs(b - y) == 0 and abs(a - x) <= 2:
                            return True
                    if get_range(self.player.grid_x, self.player.grid_y, self.miniboss.grid_x, self.miniboss.grid_y):
                        for event in events:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.end = True

                if not self.end: 
                    self.miniboss.update()
                else: 
                    self.points = 0
                    self.show_task_notice(screen, renderer)
            
            if self.end:
                px, py = self.player.grid_x, self.player.grid_y
                for item in self.paper[:]:
                    if item == (py, px):
                        self.paper.remove(item)
                        self.points += 1

            if self.end and self.points == 3:
                self.satisfy = True

            if self.support_enemy.daze > 0:
                self.support_enemy.daze -= 1
            
            if self.detained > 0:
                self.detained -= 1
                if self.detained == 0:
                    self.support_enemy.daze = 180

    def get_catch(self):
        if self.be_catch:
            return
        
        self.be_catch = True
        self.catch.start(WIDTH // 2, HEIGHT * 0.65)

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
        elif self.satisfy == False and self.change:
            gx = self.goal_x
            gy = self.goal_y

            renderer.maze_surface.blit(renderer.exit_close_image, (gx * 30, gy * 30))

            self.change = False

        if self.points and self.points != 3 and self.close == False:
            gx, gy = self.doraemon

            if self.type == 1:
                renderer.draw_path_block1(renderer.maze_surface, gy * 30, gx * 30)

            elif self.type == 2:
                renderer.draw_path_block2(renderer.maze_surface, gy * 30, gx * 30)

            else:
                renderer.draw_path_block3(renderer.maze_surface, gy * 30, gx * 30)

            renderer.maze_surface.blit(renderer.doraemon_eating_image, (gy * 30, gx * 30))
        
        if self.points == 3:
            gx, gy = self.doraemon

            if self.type == 1:
                renderer.draw_path_block1(renderer.maze_surface, gy * 30, gx * 30)

            elif self.type == 2:
                renderer.draw_path_block2(renderer.maze_surface, gy * 30, gx * 30)

            else:
                renderer.draw_path_block3(renderer.maze_surface, gy * 30, gx * 30)

        screen.blit(renderer.maze_surface, (OFFSET, OFFSET))

        renderer.draw_player(screen, self.player)
        renderer.draw_enemy(screen, self.enemy)

        if self.respond and not self.end:
            renderer.draw_miniboss(screen, self.miniboss)
            renderer.draw_home(screen, self.home)
        else: 
            gy, gx = self.miniboss.grid_x, self.miniboss.grid_y

            if self.type == 1:
                renderer.draw_path_block1(renderer.maze_surface, gy * 30, gx * 30)

            elif self.type == 2:
                renderer.draw_path_block2(renderer.maze_surface, gy * 30, gx * 30)

            else:
                renderer.draw_path_block3(renderer.maze_surface, gy * 30, gx * 30)

        renderer.draw_support_enemy(screen, self.support_enemy)

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

        if self.end:
            if not self.img:
                for idx in range(3):
                    self.img.append(renderer.paper_image[idx].copy())

            self.alpha += self.alpha_dir

            if self.alpha <= 120 or self.alpha >= 255:
                self.alpha_dir *= -1

            self.sun_angle += 2
            for idx in range(3):
                self.img[idx].set_alpha(self.alpha)

            for idx, (x, y) in enumerate(self.paper):
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

                screen.blit(self.img[idx], (OFFSET + y * 30, OFFSET + x * 30))

        self.catch.draw(screen)

    def show_tutorial(self, screen, renderer, data):
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 30)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 24)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        enemy_img = pygame.image.load("assets/anh-suneo-02_preview_rev_1.png").convert_alpha()
        enemy_img.set_colorkey((0, 0, 0))
        enemy_img = pygame.transform.scale(enemy_img, (140, 140))

        pages = data["pages"]
        page = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        page += 1

                        if page >= len(pages):
                            return
                        
            screen.blit(renderer.background, (0, 0))
            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (0, 0))

            box_w, box_h = 720, 500
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2

            pygame.draw.rect(screen, (25, 25, 25), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (190, 190, 190), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            cur = pages[page]
            title_color = (255, 255, 0)

            if page == 1:
                title_color = (255, 80, 80)

            title = font_big.render(cur["title"], True, title_color)

            tx = WIDTH//2 - title.get_width()//2
            ty = box_y + 40

            if page == 1:
                for _ in range(8):
                    ox = random.randint(-3, 3)
                    oy = random.randint(-3, 3)

                    glow = font_big.render(cur["title"], True, (255, 40, 40))

                    screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))    
            
            y = box_y + 140
        
            if page == 1:
                screen.blit(enemy_img, (WIDTH//2 - enemy_img.get_width()//2, y))

                y += 140

            for line in cur["lines"]:
                text = font_small.render(line, True, (255,255,255))
                screen.blit(text, (WIDTH//2 - text.get_width()//2, y))

                y += 38

            if "note" in cur:
                y += 15

                note = font_note.render(f'Note: {cur["note"]}', True, (160,160,160))
                screen.blit(note, (WIDTH//2 - note.get_width()//2, y))

            press = font_small.render("Press SPACE to continue", True, (220,220,220))

            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127

            press_img = press.copy()
            press_img.set_alpha(alpha)

            screen.blit(press_img, (WIDTH//2 - press_img.get_width()//2, box_y + 430))

            pygame.display.flip()

    def show_first_pick_item(self, screen, renderer, item_img):
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 30)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 24)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        item_img = pygame.transform.scale(item_img, (140, 140))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (OFFSET, OFFSET))

            box_w, box_h = 720, 500
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2

            pygame.draw.rect(screen, (25, 25, 25), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (190, 190, 190), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            title = font_big.render("NEW ITEM", True, (80, 220, 255))
            tx = WIDTH // 2 - title.get_width() // 2
            ty = box_y + 40

            for _ in range(8):
                ox = random.randint(-3, 3)
                oy = random.randint(-3, 3)
                glow = font_big.render("NEW ITEM", True, (80, 180, 255))
                screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))

            y = box_y + 140
            screen.blit(item_img, (WIDTH // 2 - item_img.get_width() // 2, y))

            y += 160
            lines = [
                "Used to stun or stop enemies",
                "Effective within 2 tiles of range"
            ]

            for line in lines:
                text = font_small.render(line, True, (255, 255, 255))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
                y += 36

            note = font_note.render("Note: An essential tool for emergency events", True, (160, 160, 160))
            screen.blit(note, (WIDTH // 2 - note.get_width() // 2, y + 15))

            press = font_small.render("Press SPACE to continue", True, (220, 220, 220))
            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            press_img = press.copy()
            press_img.set_alpha(alpha)

            screen.blit(press_img, (WIDTH // 2 - press_img.get_width() // 2, box_y + 430))

            pygame.display.flip()

    def show_task_notice(self, screen, renderer):
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 30)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 24)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        item_img = pygame.image.load("assets/d3ed1459-e77e-43eb-89e8-7d87eae58ee0.png").convert_alpha()
        item_img = pygame.transform.scale(item_img, (140, 140))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (OFFSET, OFFSET))

            box_w, box_h = 720, 500
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2

            pygame.draw.rect(screen, (25, 25, 25), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (190, 190, 190), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            title = font_big.render("TASK", True, (80, 220, 255))
            tx = WIDTH // 2 - title.get_width() // 2
            ty = box_y + 40

            for _ in range(8):
                ox = random.randint(-3, 3)
                oy = random.randint(-3, 3)
                glow = font_big.render("TASK", True, (80, 180, 255))
                screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))

            y = box_y + 140
            screen.blit(item_img, (WIDTH // 2 - item_img.get_width() // 2, y))

            y += 160
            lines = [
                "Collect all zero-point test papers",
                "to escape"
            ]

            for line in lines:
                text = font_small.render(line, True, (255, 255, 255))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
                y += 36

            note = font_note.render("Note: You can pick up multiple objects at once", True, (160, 160, 160))
            screen.blit(note, (WIDTH // 2 - note.get_width() // 2, y + 15))

            press = font_small.render("Press SPACE to continue", True, (220, 220, 220))
            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            press_img = press.copy()
            press_img.set_alpha(alpha)
            screen.blit(press_img, (WIDTH // 2 - press_img.get_width() // 2, box_y + 430))

            pygame.display.flip()

    def show_note(self, screen, renderer, data):
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 30)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 24)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (OFFSET, OFFSET))

            box_w, box_h = 720, 460
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2

            pygame.draw.rect(screen, (25, 25, 25), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (190, 190, 190), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            title = font_big.render(data["title"], True, (255, 80, 80))

            tx = WIDTH // 2 - title.get_width() // 2
            ty = box_y + 45

            for _ in range(8):
                ox = random.randint(-3, 3)
                oy = random.randint(-3, 3)

                glow = font_big.render(data["title"], True, (255, 40, 40))
                screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))

            y = box_y + 180

            for line in data["lines"]:
                text = font_small.render(line, True, (255, 255, 255))

                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))

                y += 45

            note = font_note.render(f'Note: {data["note"]}', True, (160, 160, 160))

            screen.blit(note, (WIDTH // 2 - note.get_width() // 2, y + 20))

            press = font_small.render("Press SPACE to continue", True, (220, 220, 220))

            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127

            press_img = press.copy()
            press_img.set_alpha(alpha)

            screen.blit(press_img, (WIDTH // 2 - press_img.get_width() // 2, box_y + 390))

            pygame.display.flip()

    def show_warning(self, screen, clock, warning_img, renderer):
        start = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start < 2500:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))

            renderer.draw_player(screen, self.player)
            renderer.draw_enemy(screen, self.enemy)
            renderer.draw_support_enemy(screen, self.support_enemy)

            maze_w = self.maze.cols * 30
            maze_h = self.maze.rows * 30

            overlay = pygame.Surface((maze_w, maze_h))
            overlay.set_alpha(60)
            overlay.fill((0, 0, 0))

            alpha = 180 + math.sin(pygame.time.get_ticks() * 0.01) * 75

            img = warning_img.copy()
            img.set_alpha(alpha)

            shake_x = random.randint(-3, 3)
            shake_y = random.randint(-2, 2)

            screen.blit(overlay, (OFFSET, OFFSET))

            screen.blit(img, (OFFSET + maze_w // 2 - img.get_width() // 2 + shake_x, OFFSET + maze_h // 2 - img.get_height() // 2 + shake_y))

            pygame.display.flip()
            clock.tick(FPS)