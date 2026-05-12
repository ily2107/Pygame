import random
import time
import math
import pygame
from setting import *
from core.maze import Maze
from entities.player import Player
from entities.foe.enemy import Enemy
from entities.foe.catch import Catch
from entities.foe.support_enemy import Support_enemy

class Level3:
    def __init__(self, game):
        self.game = game

        self.type = 2
        self.map = random.randint(1, 3)

        self.game.play_music("sounds/snaptik.vn_7516189863394315527.mp3", 0.5)

        self.maze = Maze.load_from_txt(f"maps/level3/map{self.map}.txt")

        self.player_spawn = (0, 0)
        self.goal_x = self.maze.cols - 1
        self.goal_y = self.maze.rows - 1

        self.enemy_spawn = self.get_enemy_spawn()

        self.player = Player(*self.player_spawn)
        self.enemy = Enemy(*self.enemy_spawn)

        self.randomize()

        self.support_enemy_spawn = self.get_support_enemy_spawn()
        self.support_enemy = Support_enemy(*self.support_enemy_spawn)

        self.points = 0
        self.satisfy = False
        self.change = False

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

        self.event_boss_image = pygame.image.load("assets/123346557_846479352823688_3443841625736522494_n.png").convert_alpha()
        self.event_boss_image.set_colorkey((0, 0, 0))
        self.event_boss_image = pygame.transform.scale(self.event_boss_image, (120, 120))

        self.event_boss_active = False
        self.event_boss_last_time = pygame.time.get_ticks()
        self.event_boss_duration = 2500
        self.event_boss_interval = 8000
        self.event_boss_start_time = 0
        self.event_boss_row = 0
        self.event_boss_x = 0
        self.event_boss_scan_rows = 5

        self.event_boss_bombs = []
        self.player_slow_until = 0
        self.last_player_move = 0
        self.normal_move_delay = 120
        self.slow_move_delay = 160

        self.dorayaki_progress = 0
        self.item_slots = [None, None, None]
        self.selected_item_slot = None

        self.speed_boost_until = 0
        self.enemy_stun_time = 180
 
        self.static_boss_active = False
        self.static_boss_pos = None
        self.static_boss_image = pygame.image.load("assets/images.png").convert_alpha()
        w, h = self.static_boss_image.get_size()
        target_h = 45
        target_w = int(w * target_h / h)

        self.static_boss_image = pygame.transform.smoothscale(self.static_boss_image, (target_w, target_h))
        self.static_boss_scream_sound = pygame.mixer.Sound("sounds/mama.mp3")
        self.static_boss_scream_sound.set_volume(0.8)

        self.static_boss_last_scream = 0
        self.static_boss_scream_interval = 10000
        self.static_boss_fear_until = 0
        self.static_boss_fear_move_delay = 220
        self.static_boss_last_fear_move = 0
        self.static_boss_scream_start = 0

        self.slot_items = [
            "tranquillizer_tick",
            "speed_gutsu",
            "pass-through_hoop"
        ]

        self.tutorial_data = {
            "pages": [
                {
                    "title": "LEVEL 3",
                    "lines": [
                        "The number of enemies is increasing...",
                        "Collect 30 dorayaki to bribe Doraemon",
                        "so you can escape from the maze."
                    ],
                    "note": [
                        "You will receive 1 of 3 random gadgets",
                        "after collecting every 6 items."
                    ]
                },
                {
                    "title": "NEW ENEMY",
                    "image": "assets/123346557_846479352823688_3443841625736522494_n.png",
                    "lines": [
                        "Doraemon patrols the maze every 6 seconds.",
                        "Do not get spotted."
                    ],
                    "note": [
                        "Each patrol leaves 3 bombs on the path.",
                        "If you step on them, you will be slowed down."
                    ]
                }
            ]
        }

        self.item_note_data = {
            "title": "NEW ITEM",
            "items": [
                {
                    "image": "assets/Ma_Ma_Boo.PNG.jpg",
                    "text": "Stuns enemies within 2 walkable tiles."
                },
                {
                    "image": "assets/Gi3Fi_z3F_z3F_t%3Fk.webp",
                    "text": "Triples your movement speed for a short time."
                },
                {
                    "image": "assets/Vongxuyenthau.webp",
                    "text": [
                        "Lets you pass through a wall toward ",
                        "the mouse direction."
                    ]
                }
            ],
            "note": [
                "Press 1, 2, or 3 to select an item.",
                "Press SPACE to activate the selected item."
            ]
        }

    def spawn_static_boss(self):
        walkable = []

        min_dist_player = 8
        min_dist_goal = 6

        for y in range(self.maze.rows):
            for x in range(self.maze.cols):
                if self.maze.is_walkable(x, y):
                    dist_player = abs(x - self.player.grid_x) + abs(y - self.player.grid_y)
                    dist_goal = abs(x - self.goal_x) + abs(y - self.goal_y)

                    if dist_player >= min_dist_player and dist_goal >= min_dist_goal:
                        walkable.append((x, y))

        if not walkable:
            for y in range(self.maze.rows):
                for x in range(self.maze.cols):
                    if self.maze.is_walkable(x, y):
                        if (x, y) != (self.player.grid_x, self.player.grid_y):
                            if (x, y) != (self.goal_x, self.goal_y):
                                walkable.append((x, y))

        if not walkable:
            return

        self.static_boss_pos = random.choice(walkable)
        self.static_boss_active = True
        self.static_boss_last_scream = pygame.time.get_ticks()

    def get_support_enemy_spawn(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(j, i) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y)) and (i, j) != self.enemy_spawn:
                    walkable.append((j, i))

        def far(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
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

    def randomize(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y) and (i, j) != self.enemy_spawn): 
                    walkable.append((j, i))

        def far_dorayaki(cell):
            return min(
                abs(cell[0] - self.player.grid_x) + abs(cell[1] - self.player.grid_y),
                abs(cell[0] - self.enemy.grid_x) + abs(cell[1] - self.enemy.grid_y),
            )

        far_cells = sorted(walkable, key=far_dorayaki, reverse=True)
        positions = random.sample(far_cells[:len(far_cells)], 3)
        self.dorayaki = positions[:3]
        
    def give_random_slot_item(self):
        empty_slots = []

        for i in range(3):
            if self.item_slots[i] is None:
                empty_slots.append(i)

        if not empty_slots:
            return

        available_items = []

        for item in self.slot_items:
            if item not in self.item_slots:
                available_items.append(item)

        if not available_items:
            return

        slot_index = random.choice(empty_slots)
        item_name = random.choice(available_items)

        self.item_slots[slot_index] = item_name

    def select_item_slot(self, slot_index):
        if slot_index < 0 or slot_index >= 3:
            return

        if self.item_slots[slot_index] is not None:
            self.selected_item_slot = slot_index

    def get_selected_item(self):
        if self.selected_item_slot is None:
            return None

        return self.item_slots[self.selected_item_slot]


    def remove_selected_item(self):
        if self.selected_item_slot is None:
            return

        self.item_slots[self.selected_item_slot] = None
        self.selected_item_slot = None

    def in_item_range(self, ax, ay, bx, by, radius=2):
        if ax == bx and abs(ay - by) <= radius:
            return True

        if ay == by and abs(ax - bx) <= radius:
            return True

        return False

    def use_tranquillizer_tick(self):
        px = self.player.grid_x
        py = self.player.grid_y

        used = False

        if self.in_item_range(px, py, self.enemy.grid_x, self.enemy.grid_y, 2):
            self.enemy.daze = self.enemy_stun_time
            used = True

        if self.in_item_range(px, py, self.support_enemy.grid_x, self.support_enemy.grid_y, 2):
            self.support_enemy.daze = self.enemy_stun_time
            used = True

        return used

    def use_speed_gutsu(self):
        self.speed_boost_until = pygame.time.get_ticks() + 4000
        return True

    def use_pass_through_hoop(self):
        mx, my = pygame.mouse.get_pos()

        player_screen_x = OFFSET + self.player.grid_x * 30 + 15
        player_screen_y = OFFSET + self.player.grid_y * 30 + 15

        dx = mx - player_screen_x
        dy = my - player_screen_y

        if abs(dx) > abs(dy):
            step_x = 1 if dx > 0 else -1
            step_y = 0
        else:
            step_x = 0
            step_y = 1 if dy > 0 else -1

        x = self.player.grid_x + step_x
        y = self.player.grid_y + step_y

        if x < 0 or x >= self.maze.cols or y < 0 or y >= self.maze.rows:
            return False

        if self.maze.is_walkable(x, y):
            return False

        while 0 <= x < self.maze.cols and 0 <= y < self.maze.rows:
            if self.maze.is_walkable(x, y):
                self.player.grid_x = x
                self.player.grid_y = y
                self.player.px = x * 30
                self.player.py = y * 30
                return True

            x += step_x
            y += step_y

        return False

    def use_selected_item(self):
        item = self.get_selected_item()

        if item is None:
            return

        used = False

        if item == "tranquillizer_tick":
            used = self.use_tranquillizer_tick()

        elif item == "speed_gutsu":
            used = self.use_speed_gutsu()

        elif item == "pass-through_hoop":
            used = self.use_pass_through_hoop()

        if used:
            self.remove_selected_item()

    def move_player_toward_static_boss(self):
        if not self.static_boss_pos:
            return

        bx, by = self.static_boss_pos
        px = self.player.grid_x
        py = self.player.grid_y

        options = []

        if bx > px:
            options.append((px + 1, py))
        elif bx < px:
            options.append((px - 1, py))

        if by > py:
            options.append((px, py + 1))
        elif by < py:
            options.append((px, py - 1))

        random.shuffle(options)

        for nx, ny in options:
            if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows:
                if self.maze.is_walkable(nx, ny):
                    self.player.grid_x = nx
                    self.player.grid_y = ny
                    self.player.px = nx * 30
                    self.player.py = ny * 30
                    return

    def update_static_boss(self):
        now = pygame.time.get_ticks()

        if not self.static_boss_active:
            if self.points >= 15:
                self.spawn_static_boss()
            return

        bx, by = self.static_boss_pos

        if self.player.grid_x == bx and self.player.grid_y == by:
            self.game.game_over = True
            return

        if now - self.static_boss_last_scream >= self.static_boss_scream_interval:
            self.static_boss_last_scream = now
            self.static_boss_scream_start = now
            self.static_boss_fear_until = now + 3000

            self.static_boss_scream_sound.play(maxtime=3000)

        if now < self.static_boss_fear_until:
            if now - self.static_boss_last_fear_move >= self.static_boss_fear_move_delay:
                self.move_player_toward_static_boss()
                self.static_boss_last_fear_move = now

    def update(self, events, screen, renderer):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game.pause_button_rect and self.game.pause_button_rect.collidepoint(event.pos):
                        pause_start = pygame.time.get_ticks()

                        result = self.game.handle_pause_menu()

                        self.pause_timers(pause_start)

                        if result == "menu":
                            return "menu"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.select_item_slot(0)

                elif event.key == pygame.K_2:
                    self.select_item_slot(1)

                elif event.key == pygame.K_3:
                    self.select_item_slot(2)

                elif event.key == pygame.K_SPACE:
                    self.use_selected_item()
                
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
                now = pygame.time.get_ticks()

                if now >= self.static_boss_fear_until:
                    if now < self.player_slow_until:
                        if now - self.last_player_move >= self.slow_move_delay:
                            self.player.handle_input(keys, self.maze)
                            self.player.update()
                            self.last_player_move = now

                    elif now < self.speed_boost_until:
                        for _ in range(3):
                            self.player.handle_input(keys, self.maze)
                            self.player.update()

                        self.last_player_move = now

                    else:
                        self.player.handle_input(keys, self.maze)
                        self.player.update()
                        self.last_player_move = now

            self.update_event_boss()
            self.update_static_boss()

            if hasattr(self.enemy, "daze") and self.enemy.daze > 0:
                self.enemy.daze -= 1
            else:
                if time.time() - self.enemy.last_move > 0.5 - self.points // 6 * 0.05:
                    self.enemy.update(self.player, self.maze)
                    self.enemy.last_move = time.time()

            if (self.points) and self.support_enemy.daze==0 and self.detained == 0:
                self.support_enemy.update(self.player, self.maze)

            if self.enemy.grid_x == self.player.grid_x and self.enemy.grid_y == self.player.grid_y:
                self.game.game_over = True

            if self.points and self.support_enemy.grid_x == self.player.grid_x and self.support_enemy.grid_y == self.player.grid_y and self.support_enemy.daze == 0 and self.detained == 0:
                self.get_catch()
            
            if self.satisfy and self.player.grid_x == self.goal_x and self.player.grid_y == self.goal_y:
                self.game.game_victory = True

            px, py = self.player.grid_x, self.player.grid_y

            for item in self.dorayaki[:]:
                if item == (py, px):
                    self.dorayaki.remove(item)
                    self.points += 1

                    if self.points == 15:
                        self.show_boss(screen, renderer)
                        
                    if self.points % 3 == 0:
                        self.dorayaki_progress += 10
                        if self.dorayaki_progress == 100:
                            self.satisfy = True
                    
                    if self.points % 6 == 0:
                        self.give_random_slot_item()

            if not self.dorayaki:
                self.randomize()

            if self.support_enemy.daze > 0:
                self.support_enemy.daze -= 1
            
            if self.detained > 0:
                self.detained -= 1
                if self.detained == 0:
                    self.support_enemy.daze = 180

    def in_bomb_range(self, px, py, bx, by):
        if px == bx:
            if abs(py - by) > 2:
                return False

            step = 1 if py > by else -1

            for y in range(by, py + step, step):
                if not self.maze.is_walkable(px, y):
                    return False

            return True

        if py == by:
            if abs(px - bx) > 2:
                return False

            step = 1 if px > bx else -1

            for x in range(bx, px + step, step):
                if not self.maze.is_walkable(x, py):
                    return False

            return True

        return False

    def pause_timers(self, pause_start):
        paused_ms = pygame.time.get_ticks() - pause_start

        self.event_boss_last_time += paused_ms

        if self.event_boss_active:
            self.event_boss_start_time += paused_ms

        self.event_boss_bombs = [
            (x, y, spawn_time + paused_ms)
            for x, y, spawn_time in self.event_boss_bombs
        ]

        self.static_boss_last_scream += paused_ms

        if self.static_boss_fear_until > 0:
            self.static_boss_fear_until += paused_ms

        if self.static_boss_scream_start > 0:
            self.static_boss_scream_start += paused_ms

        if self.player_slow_until > 0:
            self.player_slow_until += paused_ms

        if self.speed_boost_until > 0:
            self.speed_boost_until += paused_ms

    def spawn_event_boss_bombs(self):
        cells = []

        top = self.event_boss_row
        bottom = self.event_boss_row + self.event_boss_scan_rows

        for y in range(top, bottom):
            for x in range(self.maze.cols):
                if self.maze.is_walkable(x, y):
                    cells.append((x, y))

        random.shuffle(cells)
        now = pygame.time.get_ticks()
        self.event_boss_bombs = [(x, y, now) for x, y in cells[:3]]

    def update_event_boss(self):
        now = pygame.time.get_ticks()

        if not self.event_boss_active:
            if now - self.event_boss_last_time >= self.event_boss_interval:
                self.event_boss_active = True
                self.event_boss_start_time = now
                self.event_boss_row = random.randint(0, self.maze.rows - self.event_boss_scan_rows)
                self.event_boss_x = self.maze.cols * 30 + 140
        else:
            elapsed = now - self.event_boss_start_time
            progress = min(1, elapsed / self.event_boss_duration)

            self.event_boss_x = self.maze.cols * 30 + 140 - progress * (self.maze.cols * 30 + 280)

            if self.event_boss_row <= self.player.grid_y < self.event_boss_row + self.event_boss_scan_rows:
                if self.event_boss_x <= self.player.grid_x * 30:
                    self.game.game_over = True

            if elapsed >= self.event_boss_duration:
                self.event_boss_active = False
                self.event_boss_last_time = now
                self.spawn_event_boss_bombs()

        px = self.player.grid_x
        py = self.player.grid_y

        for bx, by, spawn_time in self.event_boss_bombs[:]:
            if now - spawn_time >= 10000:
                self.event_boss_bombs.remove((bx, by, spawn_time))
                continue

            if self.in_bomb_range(px, py, bx, by):
                self.event_boss_bombs.remove((bx, by, spawn_time))
                self.player_slow_until = now + 3000
                break

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

    def draw_dorayaki_progress(self, screen, panel_rect, renderer):
        bar_w = 34
        bar_h = 250

        x = panel_rect.centerx - bar_w // 2
        y = panel_rect.bottom - bar_h - 35

        progress = self.dorayaki_progress
        fill_h = int(bar_h * progress / 100)

        pygame.draw.rect(screen, (35, 35, 35), (x, y, bar_w, bar_h), border_radius=12)
        pygame.draw.rect(screen, (95, 95, 95), (x, y, bar_w, bar_h), 2, border_radius=12)

        if fill_h > 0:
            fill_rect = pygame.Rect(x + 4, y + bar_h - fill_h + 4, bar_w - 8, max(0, fill_h - 8))
            pygame.draw.rect(screen, (35, 160, 85), fill_rect, border_radius=9)

        font = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 22)
        percent_text = font.render(f"{progress}%", True, (255, 255, 255))
        screen.blit(percent_text, (panel_rect.centerx - percent_text.get_width() // 2, y - 35))

        icon = pygame.transform.scale(renderer.dorayaki_image, (28, 28))
        icon_rect = icon.get_rect(center=(panel_rect.centerx, y + bar_h + 22))
        screen.blit(icon, icon_rect)
    
    def draw_event_boss(self, screen):
        if self.event_boss_active:
            scan_x = OFFSET
            scan_y = OFFSET + self.event_boss_row * 30
            scan_w = self.maze.cols * 30
            scan_h = self.event_boss_scan_rows * 30

            scan_surface = pygame.Surface((scan_w, scan_h), pygame.SRCALPHA)
            scan_surface.fill((255, 0, 0, 55))
            screen.blit(scan_surface, (scan_x, scan_y))

            pygame.draw.rect(screen, (255, 70, 70), (scan_x, scan_y, scan_w, scan_h), 2)

            boss_y = scan_y + scan_h // 2 - self.event_boss_image.get_height() // 2
            screen.blit(self.event_boss_image, (OFFSET + self.event_boss_x, boss_y))

        for bx, by, spawn_time in self.event_boss_bombs:
            cx = OFFSET + bx * 30 + 15
            cy = OFFSET + by * 30 + 15

            pygame.draw.circle(screen, (210, 60, 60), (cx, cy), 10)
            pygame.draw.circle(screen, (35, 35, 35), (cx, cy), 6)
            pygame.draw.circle(screen, (255, 220, 120), (cx + 4, cy - 6), 3)

    def draw(self, renderer, screen):
        screen.blit(renderer.background, (0, 0))

        dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 90))
        screen.blit(dark_overlay, (0, 0))

        self.draw_magic_border(screen)
        panel_rect = self.draw_side_frame(screen)

        if panel_rect:
            self.game.draw_pause_button(screen, panel_rect, renderer, self)
            self.draw_dorayaki_progress(screen, panel_rect, renderer)

        if self.satisfy and self.change == False:
            gx = self.goal_x
            gy = self.goal_y

            renderer.maze_surface.blit(renderer.exit_open_image, (gx * 30, gy * 30))

            self.change = True

        screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
        self.draw_event_boss(screen)
        self.draw_static_boss(screen)

        renderer.draw_player(screen, self.player)
        renderer.draw_enemy(screen, self.enemy)

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

        self.catch.draw(screen)

    def draw_static_boss(self, screen):
        if not self.static_boss_active or not self.static_boss_pos:
            return

        bx, by = self.static_boss_pos

        x = OFFSET + bx * 30 + 15
        y = OFFSET + by * 30 + 15

        img = self.static_boss_image
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)

        now = pygame.time.get_ticks()

        if now < self.static_boss_fear_until:
            maze_w = self.maze.cols * 30
            maze_h = self.maze.rows * 30
            max_radius = int(math.sqrt(maze_w * maze_w + maze_h * maze_h))

            elapsed = now - self.static_boss_scream_start
            duration = 3000

            base_radius = int((elapsed / duration) * max_radius)

            for offset in [0, 90, 180]:
                radius = base_radius - offset

                if radius > 0:
                    alpha = max(0, 160 - radius // 3)

                    wave_surface = pygame.Surface((self.maze.cols * 30, self.maze.rows * 30), pygame.SRCALPHA)

                    local_x = x - OFFSET
                    local_y = y - OFFSET

                    pygame.draw.circle(wave_surface, (255, 80, 80, alpha), (local_x, local_y), radius, 3)
                    screen.blit(wave_surface, (OFFSET, OFFSET))

    def show_tutorial(self, screen, renderer, data):
        pause_start = pygame.time.get_ticks()
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 30)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 24)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

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
            if cur["title"] == "NEW ENEMY":
                title_color = (255, 80, 80)

            title = font_big.render(cur["title"], True, title_color)

            tx = WIDTH // 2 - title.get_width() // 2
            ty = box_y + 35 if "image" in cur else box_y + 45

            if cur["title"] == "NEW ENEMY":
                for _ in range(8):
                    ox = random.randint(-3, 3)
                    oy = random.randint(-3, 3)
                    glow = font_big.render(cur["title"], True, (255, 40, 40))
                    screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))

            if "image" in cur:
                y = box_y + 118
                line_gap = 45
                note_gap = 8
                note_line_gap = 24
            else:
                y = box_y + 155
                line_gap = 50
                note_gap = 20
                note_line_gap = 30

            if "image" in cur:
                tutorial_img = pygame.image.load(cur["image"]).convert_alpha()
                tutorial_img = pygame.transform.scale(tutorial_img, (135, 135))
                img_rect = tutorial_img.get_rect(center=(WIDTH // 2, y + tutorial_img.get_height() // 2))
                screen.blit(tutorial_img, img_rect)
                y += 140

            for line in cur["lines"]:
                text = font_small.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, y + text.get_height() // 2))
                screen.blit(text, text_rect)
                y += line_gap

            if "note" in cur:
                y += note_gap

                note_lines = cur["note"] if isinstance(cur["note"], list) else [cur["note"]]

                rendered_lines = []

                first_text = font_note.render("Note: " + note_lines[0], True, (160, 160, 160))
                rendered_lines.append(first_text)

                for note_line in note_lines[1:]:
                    rendered_lines.append(font_note.render(note_line, True, (160, 160, 160)))

                for note_surface in rendered_lines:
                    note_rect = note_surface.get_rect(center=(WIDTH // 2, y + note_surface.get_height() // 2))
                    screen.blit(note_surface, note_rect)
                    y += note_line_gap

            press = font_small.render("Press SPACE to continue", True, (220, 220, 220))

            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127

            press_img = press.copy()
            press_img.set_alpha(alpha)

            screen.blit(press_img, (WIDTH // 2 - press_img.get_width() // 2, box_y + 430))

            pygame.display.flip()

    def show_item_note(self, screen, renderer, data):
        pause_start = pygame.time.get_ticks()
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 25)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 22)

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
                        self.pause_timers(pause_start)
                        return

            screen.blit(renderer.background, (0, 0))
            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (0, 0))

            box_w, box_h = 720, 500
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2

            pygame.draw.rect(screen, (25, 25, 25), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (190, 190, 190), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            title = font_big.render(data["title"], True, (80, 220, 255))
            tx = WIDTH // 2 - title.get_width() // 2
            ty = box_y + 35

            for _ in range(8):
                ox = random.randint(-3, 3)
                oy = random.randint(-3, 3)
                glow = font_big.render(data["title"], True, (80, 180, 255))
                screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))

            item_size = 58
            start_y = box_y + 125
            gap_y = 82
            img_x = box_x + 120
            text_x = box_x + 190

            for idx, item in enumerate(data["items"]):
                y = start_y + idx * gap_y

                item_img = pygame.image.load(item["image"]).convert_alpha()
                item_img = pygame.transform.scale(item_img, (item_size, item_size))
                img_rect = item_img.get_rect(center=(img_x, y + item_size // 2))
                screen.blit(item_img, img_rect)

                text_lines = item["text"] if isinstance(item["text"], list) else [item["text"]]

                for line_idx, line in enumerate(text_lines):
                    text = font_small.render(line, True, (255, 255, 255))
                    screen.blit(text, (text_x, y + 6 + line_idx * 28))

            note_y = box_y + 390

            note_lines = data["note"] if isinstance(data["note"], list) else [data["note"]]

            first = font_note.render("Note: " + note_lines[0], True, (160, 160, 160))
            first_rect = first.get_rect(center=(WIDTH // 2, note_y))
            screen.blit(first, first_rect)

            note_y += 26

            for line in note_lines[1:]:
                note = font_note.render(line, True, (160, 160, 160))
                note_rect = note.get_rect(center=(WIDTH // 2, note_y))
                screen.blit(note, note_rect)
                note_y += 26

            press = font_note.render("Press SPACE to continue", True, (220, 220, 220))
            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            press_img = press.copy()
            press_img.set_alpha(alpha)

            screen.blit(press_img, (WIDTH // 2 - press_img.get_width() // 2, box_y + 450))

            pygame.display.flip()
    
    def show_boss(self, screen, renderer):
        pause_start = pygame.time.get_ticks()
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 30)
        font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 24)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        boss_data = {
            "title": "NEW BOSS",
            "image": "assets/images.png",  
            "lines": [
                "Nobita's mom is furious!",
                "Don't let her catch you.",
                "Her scream can terrify you and pull you toward her."
            ],
            "note": "You cannot control yourself while Mom's scream is active."
        }

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause_timers(pause_start)
                        return

            screen.blit(renderer.background, (0, 0))
            screen.blit(renderer.maze_surface, (OFFSET, OFFSET))
            screen.blit(overlay, (0, 0))

            box_w, box_h = 720, 500
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2

            pygame.draw.rect(screen, (25, 25, 25), (box_x, box_y, box_w, box_h), border_radius=20)
            pygame.draw.rect(screen, (190, 190, 190), (box_x, box_y, box_w, box_h), 3, border_radius=20)

            title_color = (255, 80, 80)
            title_text = boss_data["title"]

            title = font_big.render(title_text, True, title_color)

            tx = WIDTH // 2 - title.get_width() // 2
            ty = box_y + 35

            for _ in range(8):
                ox = random.randint(-3, 3)
                oy = random.randint(-3, 3)
                glow = font_big.render(title_text, True, (255, 40, 40))
                screen.blit(glow, (tx + ox, ty + oy))

            screen.blit(title, (tx, ty))

            y = box_y + 118
            line_gap = 38
            note_gap = 12
            note_line_gap = 22

            boss_img = pygame.image.load(boss_data["image"]).convert_alpha()
            boss_img = pygame.transform.scale(boss_img, (236, 135))
            img_rect = boss_img.get_rect(center=(WIDTH // 2, y + boss_img.get_height() // 2))
            screen.blit(boss_img, img_rect)

            y += 145

            for line in boss_data["lines"]:
                text = font_small.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, y + text.get_height() // 2))
                screen.blit(text, text_rect)
                y += line_gap

            y += note_gap

            note_text = font_note.render("Note: " + boss_data["note"], True, (160, 160, 160))
            note_rect = note_text.get_rect(center=(WIDTH // 2, y + note_text.get_height() // 2))
            screen.blit(note_text, note_rect)

            press = font_small.render("Press SPACE to continue", True, (220, 220, 220))

            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127

            press_img = press.copy()
            press_img.set_alpha(alpha)

            screen.blit(
                press_img,
                (WIDTH // 2 - press_img.get_width() // 2, box_y + 430)
            )

            pygame.display.flip()