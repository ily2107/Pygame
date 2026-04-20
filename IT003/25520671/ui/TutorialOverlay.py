import math
import pygame
from setting import *

class TutorialOverlay:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 60)
        self.font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 32)
        self.font_note = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 26)  # 👈 font nhỏ hơn

    def show(self, level_num, renderer):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        box_w, box_h = 720, 480
        box_x = (WIDTH - box_w) // 2
        box_y = (HEIGHT - box_h) // 2

        title = self.font_big.render(f"LEVEL {level_num}", True, (255, 255, 0))

        line1 = self.font_small.render(
            "Collect Dorayaki and give them to Doraemon",
            True, (255, 255, 255)
        )

        line2 = self.font_small.render(
            "Get enough to unlock the Magic Door and escape!",
            True, (255, 255, 255)
        )

        line3 = self.font_small.render(
            "Avoid Jaian!",
            True, (255, 255, 255)
        )

        # 👇 NOTE MỚI
        note_text = self.font_note.render(
            "Note: You can carry only one Dorayaki at a time.",
            True, (150, 150, 150)
        )

        press_text = self.font_small.render(
            "Press SPACE to start",
            True, (200, 200, 200)
        )

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            self.screen.blit(renderer.maze_surface, (0, 0))
            self.screen.blit(overlay, (0, 0))

            pygame.draw.rect(
                self.screen,
                (30, 30, 30),
                (box_x, box_y, box_w, box_h),
                border_radius=20
            )

            pygame.draw.rect(
                self.screen,
                (200, 200, 200),
                (box_x, box_y, box_w, box_h),
                3,
                border_radius=20
            )

            # ===== TEXT =====
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, box_y + 50))
            self.screen.blit(line1, (WIDTH//2 - line1.get_width()//2, box_y + 140))
            self.screen.blit(line2, (WIDTH//2 - line2.get_width()//2, box_y + 190))
            self.screen.blit(line3, (WIDTH//2 - line3.get_width()//2, box_y + 240))

            # 👇 NOTE (nằm dưới Avoid Jaian)
            self.screen.blit(
                note_text,
                (WIDTH//2 - note_text.get_width()//2, box_y + 290)
            )

            # ===== PRESS SPACE NHẤP NHÁY =====
            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127
            img = press_text.copy()
            img.set_alpha(alpha)

            self.screen.blit(
                img,
                (WIDTH//2 - img.get_width()//2, box_y + 360)
            )

            pygame.display.flip()