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
        self.tutorial = TutorialOverlay(self.screen)


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
            self.load_level()
            self.tutorial.show(self.level_cnt, self.renderer,self.level.tutorial_data)
            self.run_game()

    def run_game(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.load_level()
                    elif event.key == pygame.K_p:
                        action = self.handle_pause_menu()
                        if action == "menu":
                            return

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

                self.load_level()
                return

            self.level.update()
            self.level.draw(self.renderer, self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)

                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)

                    elif event.key == pygame.K_p:
                        return

                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            return "resume"

                        elif selected == 1:
                            self.load_level()
                            return "menu"

                        elif selected == 2:
                            pygame.quit()
                            exit()

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            title = font_big.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

            for i, option in enumerate(options):
                color = (0, 255, 150) if i == selected else (255, 255, 255)

                text = font_small.render(option, True, color)

                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 70))

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