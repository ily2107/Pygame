import math
import auth
import pygame
import importlib
from setting import *
from ui.menu import Menu
from ui.TutorialOverlay import TutorialOverlay
from systems.renderer import Renderer
class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.menu = Menu(self)
        self.level_cnt = 1

        self.current_user = None
        self.user_data = None

        self.game_over = False
        self.game_victory = False

        self.renderer = Renderer(self.screen)
        self.pause_button_rect = None

    def load_level(self):
        module = importlib.import_module(f"levels.level{self.level_cnt}")
        importlib.reload(module)

        level_class = getattr(
            module,
            f"Level{self.level_cnt}"
        )

        self.level = level_class(self)

        self.game_over = False
        self.game_victory = False

        self.renderer.draw_maze(self.level, self.level.type)

    def run(self):
        while True:
            self.menu.run()

            while True:
                self.load_level()
                self.level.show_tutorial(self.screen, self.renderer, self.level.tutorial_data)

                if hasattr(self.level, "item_note_data"):
                    self.level.show_item_note(self.screen, self.renderer, self.level.item_note_data)

                result = self.run_game()

                if result == "menu":
                    break

    def play_music(self, path, volume=0.5):
        if getattr(self, "current_music", None) == path:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

        self.current_music = path

    def run_game(self):
        running = True

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.load_level()

            if self.game_over:
                auth.update_user(self.current_user, {
                    "level": self.level_cnt
                })

                self.show_game_over()
                self.load_level()
                return

            if self.game_victory:
                self.show_game_victory()

                self.level_cnt += 1

                auth.update_user(self.current_user, {
                    "level": self.level_cnt
                })

                return

            action = self.level.update(events, self.screen, self.renderer)

            if action == "menu":
                return "menu"

            self.level.draw(self.renderer, self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def get_slot_item_image(self, renderer, level, item_name):
        if item_name == "tranquillizer_tick":
            return renderer.item_image1

        elif item_name == "speed_gutsu":
            return renderer.item_image2

        elif item_name == "pass-through_hoop":
            return renderer.item_image3

        return None

    def draw_pause_button(self, screen, panel_rect, renderer, level):
        size = 36
        padding = 14

        x = panel_rect.x + panel_rect.w // 2 - size // 2
        y = panel_rect.y + padding

        self.pause_button_rect = pygame.Rect(x, y, size, size)

        pygame.draw.rect(screen, (35, 160, 85), self.pause_button_rect, border_radius=9)
        pygame.draw.rect(screen, (80, 230, 130), self.pause_button_rect, 2, border_radius=9)

        bar_w = 4
        bar_h = 16
        gap = 5

        cx = self.pause_button_rect.centerx
        cy = self.pause_button_rect.centery

        pygame.draw.rect(screen, (255, 255, 255), (cx - gap - bar_w, cy - bar_h // 2, bar_w, bar_h), border_radius=2)
        pygame.draw.rect(screen, (255, 255, 255), (cx + gap, cy - bar_h // 2, bar_w, bar_h), border_radius=2)

        circle_r = 19
        start_y = self.pause_button_rect.bottom + 48
        gap_y = 50
        cx = self.pause_button_rect.centerx

        if hasattr(level, "item_slots"):
            items = level.item_slots
            selected_slot = level.selected_item_slot
        else:
            items = [
                "tranquillizer_tick" if "tranquillizer_tick" in level.player.inventory else None,
                None,
                None
            ]
            selected_slot = None

        for i, item_name in enumerate(items):
            cy = start_y + i * gap_y

            selected = selected_slot == i

            if selected:
                border_color = (255, 230, 80)
                border_width = 3
            else:
                border_color = (80, 230, 130)
                border_width = 2

            if item_name:
                pygame.draw.circle(screen, (5, 7, 12), (cx, cy), circle_r)
                pygame.draw.circle(screen, border_color, (cx, cy), circle_r, border_width)

                item_img = self.get_slot_item_image(renderer, level, item_name)
                if item_img is None:
                    continue

                img_size = circle_r * 2 - 8
                img = pygame.transform.scale(item_img, (img_size, img_size)).convert_alpha()

                circle_img = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
                circle_img.blit(img, (0, 0))

                mask = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
                pygame.draw.circle(mask, (255, 255, 255, 255), (img_size // 2, img_size // 2), img_size // 2)

                circle_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                rect = circle_img.get_rect(center=(cx, cy))
                screen.blit(circle_img, rect)

            else:
                pygame.draw.circle(screen, (45, 45, 45), (cx, cy), circle_r)
                pygame.draw.circle(screen, (95, 95, 95), (cx, cy), circle_r, 2)

    def handle_pause_menu(self):
        font_big = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 80)
        font_small = pygame.font.Font("assets/Baloo2-VariableFont_wght.ttf", 45)

        options = ["Resume", "Back To Menu", "Quit"]
        selected = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, rect in enumerate(option_rects):
                            if rect.collidepoint(event.pos):
                                if i == 0:
                                    return "resume"

                                elif i == 1:
                                    return "menu"

                                elif i == 2:
                                    pygame.quit()
                                    exit()

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            title = font_big.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

            option_rects = []
            mouse_pos = pygame.mouse.get_pos()

            for i, option in enumerate(options):
                text = font_small.render(option, True, (255, 255, 255))
                rect = text.get_rect(center=(WIDTH // 2, 250 + i * 70 + text.get_height() // 2))

                if rect.collidepoint(mouse_pos):
                    selected = i

                color = (0, 255, 150) if i == selected else (255, 255, 255)

                text = font_small.render(option, True, color)
                rect = text.get_rect(center=(WIDTH // 2, 250 + i * 70 + text.get_height() // 2))

                option_rects.append(rect)
                self.screen.blit(text, rect)

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

        text2 = font_mid.render("YOU GOT CAUGHT!", True, (255, 255, 255))
        text3 = font_small.render("PRESS SPACE TO RESTART", True, (180, 180, 180))

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