import pygame
import math
from setting import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        self.options = ["Start game", "Quit"]
        self.selected = 0 

        self.state = "auth"

        self.font = pygame.font.Font(FONT_NAME,FONT_SIZE)
        self.bg = pygame.image.load("assets/doraemon_tap_moi_nhat_2026_cover_62ebedefaf.webp")
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.username = ""
        self.password = ""
        self.active = "username"

        self.message = ""
        self.message_time = 0
        self.button_rect = pygame.Rect(WIDTH//2 - 100, 350, 200, 50)

        self.option_rects = []
        input_w = 520
        input_h = 45
        self.start_y = HEIGHT // 2 - 80

        self.username_rect = pygame.Rect(WIDTH // 2 - input_w // 2, self.start_y, input_w, input_h)
        self.password_rect = pygame.Rect(WIDTH // 2 - input_w // 2, self.start_y + 60, input_w, input_h)

        self.button_rect = pygame.Rect(WIDTH // 2 - 100, self.start_y + 150, 200, 50)

    def get_options(self):
        if self.state == "auth":
            return ["Login", "Register"]
        elif self.state == "main":
            return ["Continue", "New game"]
        
        return []
        
    def handle_events(self):
        self.options = self.get_options()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.state in ["auth", "main"]:
                # if event.type == pygame.KEYDOWN:

                #     if event.key == pygame.K_UP:
                #         self.selected = (self.selected - 1) % len(self.options)

                #     elif event.key == pygame.K_DOWN:
                #         self.selected = (self.selected + 1) % len(self.options)

                #     elif event.key == pygame.K_RETURN:
                #         self.select()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, rect in enumerate(self.option_rects):
                            if rect.collidepoint(event.pos):
                                self.selected = i
                                self.select()

            elif self.state in ["input_login", "input_register"]:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_TAB:
                        self.active = "password" if self.active == "username" else "username"

                    elif event.key == pygame.K_RETURN:
                        import auth

                        if self.state == "input_login":
                            ok, data = auth.login(self.username, self.password)
                            if ok:
                                self.game.current_user = self.username
                                self.game.user_data = data
                                self.state = "main"
                                self.selected = 0
                                self.username = ""
                                self.password = ""
                                self.active = "username"
                            else:
                                if data == "no_user":
                                    self.message = "Username khong ton tai!"
                                elif data == "wrong_pass":
                                    self.message = "Sai mat khau!"

                                self.message_time = pygame.time.get_ticks()

                        else:
                            ok, msg = auth.register(self.username, self.password)

                            if ok:
                                self.state = "auth"
                                self.username = ""
                                self.password = ""
                                self.active = "username"
                            else:
                                self.message = msg
                                self.message_time = pygame.time.get_ticks()

                    elif event.key == pygame.K_BACKSPACE:
                        if self.active == "username":
                            self.username = self.username[:-1]
                        else:
                            self.password = self.password[:-1]

                    elif event.key == pygame.K_ESCAPE:
                        self.state = "auth"
                        self.username = ""
                        self.password = ""
                        self.active = "username"

                    else:
                        if self.active == "username":
                            self.username += event.unicode
                        else:
                            self.password += event.unicode
                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_rect.collidepoint(event.pos):
                        self.active = "username"

                    elif self.password_rect.collidepoint(event.pos):
                        self.active = "password"

                    elif self.button_rect.collidepoint(event.pos):
                        import auth

                        if self.state == "input_login":
                            ok, data = auth.login(self.username, self.password)
                            if ok:
                                self.game.current_user = self.username
                                self.game.user_data = data
                                self.state = "main"
                                self.selected = 0
                                self.username = ""
                                self.password = ""
                                self.active = "username"
                            else:
                                if data == "no_user":
                                    self.message = "Username khong ton tai!"
                                elif data == "wrong_pass":
                                    self.message = "Sai mat khau!"

                                self.message_time = pygame.time.get_ticks()

                        else:
                            ok, msg = auth.register(self.username, self.password)

                            if ok:
                                self.state = "auth"
                                self.username = ""
                                self.password = ""
                                self.active = "username"
                            else:
                                self.message = msg
                                self.message_time = pygame.time.get_ticks()

    def select(self):
        if self.state == "auth":
            if self.selected == 0:
                self.state = "input_login"
                self.selected = 0
            elif self.selected == 1:
                self.state = "input_register"
                self.selected = 0

        elif self.state == "main":
            if self.selected == 1:  
                self.game.level_cnt = 1
                self.running = False

            elif self.selected == 0:  
                if self.game.user_data:
                    self.game.level_cnt = self.game.user_data["level"]
                else:
                    self.game.level_cnt = 1
                self.running = False

    def draw(self):
        font = pygame.font.Font(None, 40)

        if self.state in ["input_login", "input_register"]:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.Font(None, 40)

            title = "LOGIN" if self.state == "input_login" else "REGISTER"
            t = font.render(title, True, (255,255,255))
            self.screen.blit(t, (WIDTH//2 - t.get_width()//2, self.start_y - 80))

            user_text = "User: " + self.username

            if self.active == "username":
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    user_text += "|"

            u = font.render(user_text, True, (255,255,255))
            
            pass_text = "Pass: " + "*" * len(self.password)

            if self.active == "password":
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    pass_text += "|"

            p = font.render(pass_text, True, (255,255,255))

            user_border = (0, 255, 150) if self.active == "username" else (255, 255, 255)
            pass_border = (0, 255, 150) if self.active == "password" else (255, 255, 255)

            pygame.draw.rect(self.screen, (10, 12, 18), self.username_rect, border_radius=8)
            pygame.draw.rect(self.screen, user_border, self.username_rect, 2, border_radius=8)

            pygame.draw.rect(self.screen, (10, 12, 18), self.password_rect, border_radius=8)
            pygame.draw.rect(self.screen, pass_border, self.password_rect, 2, border_radius=8)

            self.screen.blit(u, (self.username_rect.x + 15, self.username_rect.y + 7))
            self.screen.blit(p, (self.password_rect.x + 15, self.password_rect.y + 7))

            mouse_pos = pygame.mouse.get_pos()
            color = (0, 255, 150) if self.button_rect.collidepoint(mouse_pos) else (0, 200, 100)

            pygame.draw.rect(self.screen, color, self.button_rect, border_radius=10)

            btn_text = "LOGIN" if self.state == "input_login" else "REGISTER"
            btn = font.render(btn_text, True, (255,255,255))

            self.screen.blit(
                btn,
                (self.button_rect.x + self.button_rect.width//2 - btn.get_width()//2,
                self.button_rect.y + self.button_rect.height//2 - btn.get_height()//2)
            )

            if self.message:
                if pygame.time.get_ticks() - self.message_time < 2000:

                    msg = font.render(self.message, True, (255,255,255))

                    box_width = msg.get_width() + 40
                    box_height = msg.get_height() + 30

                    box = pygame.Surface((box_width, box_height))
                    box.fill((150, 0, 0))
                    box.set_alpha(220)

                    box_x = WIDTH//2 - box_width//2
                    box_y = HEIGHT//2 - box_height//2

                    self.screen.blit(box, (box_x, box_y))
                    self.screen.blit(
                        msg,
                        (
                            WIDTH//2 - msg.get_width()//2,
                            HEIGHT//2 - msg.get_height()//2
                        )
                    )
                    self.screen.blit(
                        msg,
                        (WIDTH//2 - msg.get_width()//2,
                        HEIGHT//2 - msg.get_height()//2)
                    )
                else:
                    self.message = ""

            alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127

            hint = font.render("Press ESC to switch Login/Register", True, (200,200,200)).copy()
            hint.set_alpha(alpha)

            self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 80))

            pygame.display.flip()
            return
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(None, 60)
        title = title_font.render(TITLE_GAME, True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        self.option_rects = []
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(self.options):
            text = self.font.render(option, True, TEXT_COLOR)

            x = WIDTH//2 - text.get_width()//2
            y = 150 + i * 60
            rect = text.get_rect(topleft=(x, y))

            if rect.collidepoint(mouse_pos):
                self.selected = i

            color = HIGHLIGHT_COLOR if i == self.selected else TEXT_COLOR
            text = self.font.render(option, True, color)
            rect = text.get_rect(topleft=(x, y))

            self.option_rects.append(rect)
            self.screen.blit(text, rect)
        
        pygame.display.flip()
    
    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
