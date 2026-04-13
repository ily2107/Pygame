import pygame
from setting import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        self.options = ["Start game", "Quit"]
        self.selected = 0 

        self.font = pygame.font.Font(FONT_NAME,FONT_SIZE)
        self.bg = pygame.image.load("assets/doraemon_tap_moi_nhat_2026_cover_62ebedefaf.webp")
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)

                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                
                elif event.key == pygame.K_SPACE:
                    self.select()

    def select(self):
        if self.selected == 0:
            self.running = False

        elif self.selected == 1:
            pygame.quit()
            exit()

    def draw(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(None, 60)
        title = title_font.render(TITLE_GAME, True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        for i,option in enumerate(self.options):
            color = HIGHLIGHT_COLOR if i == self.selected else TEXT_COLOR
            text = self.font.render(option, True, color)

            x = WIDTH//2 - text.get_width()//2
            y = 150 + i * 60

            self.screen.blit(text, (x, y))
        
        pygame.display.flip()
    
    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
