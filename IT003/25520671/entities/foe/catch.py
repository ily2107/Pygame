import pygame
import random
import time
import math
from setting import *

class Catch:
    def __init__(self):
        self.active = False
        self.failed = False

        self.progress = 0
        self.max_progress = 100

        self.center = (400, 300)

        self.scale = 1.0
        self.shake = 0
        self.flash_timer = 0

        self.last_press_time = 0

        self.time_limit = 10.0
        self.start_time = 0

        self.decay_rate = 12      
        self.slow_threshold = 0.25

        pygame.mixer.init()

    def start(self, x, y):
        self.active = True
        self.failed = False

        self.progress = 0
        self.center = (x, y)

        self.scale = 1.0
        self.shake = 0
        self.flash_timer = 0

        self.start_time = time.time()
        self.last_press_time = self.start_time

    def on_press(self):
        if not self.active:
            return

        now = time.time()
        delta = now - self.last_press_time
        self.last_press_time = now

        if delta < 0.12:
            gain = 10
        elif delta < 0.2:
            gain = 8
        else:
            gain = 6.5

        self.progress += gain

        if delta > 0.4:
            self.progress -= 2
            self.shake = 10

        self.scale = 1.15
        self.shake = max(self.shake, 5)
        self.flash_timer = 4

    def update(self):
        if not self.active:
            return

        now = time.time()

        if now - self.start_time >= self.time_limit:
            if self.progress < self.max_progress:
                self.active = False
                self.failed = True
            return

        idle_time = now - self.last_press_time

        if idle_time > self.slow_threshold:
            decay = self.decay_rate * (idle_time - self.slow_threshold)
            self.progress -= decay

        if self.progress < 0:
            self.progress = 0
        elif self.progress > self.max_progress:
            self.progress = self.max_progress

        if self.progress >= self.max_progress:
            self.active = False
            return

        self.scale += (1.0 - self.scale) * 0.2
        self.shake *= 0.85

        if self.flash_timer > 0:
            self.flash_timer -= 1

    def draw(self, screen):
        if not self.active:
            return

        shake_x = random.randint(-int(self.shake), int(self.shake))
        shake_y = random.randint(-int(self.shake), int(self.shake))

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        cx, cy = self.center
        cx += shake_x
        cy += shake_y

        radius = int(40 * self.scale)

        color = (255, 255, 0)
        if self.flash_timer > 0:
            color = (255, 255, 255)

        pygame.draw.circle(screen, color, (cx, cy), radius)

        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 40)
        font_small.set_bold(True)
        text1 = font_small.render("SPAM SPACE TO RESIST", True, (180, 180, 180))
        alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
        img = text1.copy()
        img.set_alpha(alpha)
        screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT - 100))

        font = pygame.font.SysFont(None, int(30 * self.scale))
        text = font.render("SPACE", True, (0, 0, 0))
        rect = text.get_rect(center=(cx, cy))
        screen.blit(text, rect)

        bar_w = 260
        bar_h = 20

        px = cx - bar_w // 2
        py = cy + 70

        pygame.draw.rect(screen, (60, 60, 60), (px, py, bar_w, bar_h))

        fill_w = int(bar_w * (self.progress / self.max_progress))

        color = (255, 200, 0)
        if self.progress > 70:
            color = (255, 100, 0)

        pygame.draw.rect(screen, color, (px, py, fill_w, bar_h))

        elapsed = time.time() - self.start_time
        remain = max(0, self.time_limit - elapsed)

        tbar_w = 260
        tbar_h = 10

        tx = cx - tbar_w // 2
        ty = cy - 60

        pygame.draw.rect(screen, (80, 80, 80), (tx, ty, tbar_w, tbar_h))

        fill_t = int(tbar_w * (remain / self.time_limit))
        pygame.draw.rect(screen, (100, 200, 255), (tx, ty, fill_t, tbar_h))