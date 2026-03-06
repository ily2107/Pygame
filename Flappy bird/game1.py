# CHÚ THÍCH
# rect trong code này sẽ là lấy rectangle là lấy phạm vi
# của 1 đối tượng để em có thể xử lý va chạm như là bird, pipe, floor
# 
# P là trọng lực, velocity là tốc tốc theo trục y(dọc) hiện tại của chim
#
# self của mỗi class là cách để em chạy các biến số của bản thân class đó khi em gọi class
# 
# __init__ sẽ là khi em gọi ở ngoài 1 biến bird=Bird() thì __init__ trong class sẽ tự khởi tạo ngay lập tức
#
# SCROLL_SPEED thì là tốc độ dịch sang trái(phải) của các đối tượng trên màn hình của em
# anh trừ đi SCROLL_SPEED=1 nghĩa là màn hình của anh sẽ dịch sang trái 1 pixel trên mỗi frame
#
# mấy ảnh trong bài anh gọi nó nằm trong file trong máy em anh sẽ gửi kèm theo ạ
#
# ở class pipe thì gap là khoảng cách giữa 2 cột pipe của anh mỗi lần sinh ra
# 
# offset sẽ là khoảng trống giữa 2 cột kế tiếp nhau
#
# midtop và midbottom trong bài sẽ có gtri như này để em xử lý va chạm khi chạm vào phần rect của pipe
#    midtop pipe
#       |
#       |
#       |
# ------gap------
#       |
#       |
#    midbottom pipe

#Created by Vu Thi Thu Huong
import pygame
import random

# ==================================================
# CONSTANTS
# ==================================================
WIDTH=432
HEIGHT=768
FLOOR_Y=600
SCROLL_SPEED=1
P=0.2


# ==================================================
# CLASSES
# ==================================================
class Bird:
    def __init__(self):
        self.fall_image=pygame.image.load("Flappy bird/assets/yellowbird-upflap.png")
        self.fall_image=pygame.transform.scale2x(self.fall_image)
        self.rect=self.fall_image.get_rect(center=(100,300))       
        self.tap_image=pygame.image.load("Flappy bird/assets/yellowbird-downflap.png")
        self.tap_image=pygame.transform.scale2x(self.tap_image)
        self.swap=False
        self.velocity=0

    def update(self):
        self.velocity+=P
        self.rect.y+=self.velocity
        if self.velocity>0: self.swap=False
    
    def draw(self,screen):
        if self.swap:
            screen.blit(self.tap_image,self.rect)
        else: 
            screen.blit(self.fall_image,self.rect)


class Floor:
    def __init__(self,image,y):
        self.image=image
        self.y=y
        self.x=0
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)

    def update(self):
        self.x-=SCROLL_SPEED
        if self.x<=-self.width:
            self.x=0
        self.rect.x=self.x

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
        screen.blit(self.image,(self.x+self.width,self.y))


class Pipe:

    def __init__(self,image,bird):
        self.image=image
        self.image_flipped=pygame.transform.flip(image,False,True)

        self.x=WIDTH
        self.speed=SCROLL_SPEED
        self.GAP=random.randint(150,240)

        offset=random.randint(-100,100)
        center_y=bird.rect.centery+offset
        center_y=min(center_y,400)
        center_y=max(center_y,100)

        top_height=center_y-self.GAP//2
        bottom_y=center_y+self.GAP//2     

        self.top_rect=self.image_flipped.get_rect(
            midbottom=(self.x,top_height)
        )

        self.bottom_rect=self.image.get_rect(
            midtop=(self.x,bottom_y)
        )

        self.passed=False
    
    def update(self):
        self.top_rect.x-=self.speed
        self.bottom_rect.x-=self.speed

    def draw(self,screen):
        screen.blit(self.image, self.top_rect)
        screen.blit(self.image_flipped, self.bottom_rect)

    def offscreen(self):
        return self.top_rect.right<0
    

class Score:
    def __init__(self):
        self.value=0
        self.h_value=0
        self.font=pygame.font.Font("Flappy bird/04B_19.TTF",40)
        self.h_font=pygame.font.Font("Flappy bird/04B_19.TTF",50)

    def update(self):
        self.value+=1

    def draw(self,screen):
        surface=self.font.render(f'Score: {(self.value)}',True,(255,255,255))
        rect=surface.get_rect(center=(WIDTH//2,100))
        screen.blit(surface,rect)

    def end_draw(self,screen):
        surface=self.font.render(f'Score: {(self.value)}',True,(255,255,255))
        h_surface=self.h_font.render(f'High score: {(self.h_value)}',True,(255,0,0))
        rect=surface.get_rect(center=(WIDTH//2,60))
        h_rect=h_surface.get_rect(center=(WIDTH//2,125))
        screen.blit(surface,rect)
        screen.blit(h_surface,h_rect)


class Sound:
    def __init__(self):
        self.jump_sound=pygame.mixer.Sound("Flappy bird/sound/sfx_wing.wav")
        self.die_sound=pygame.mixer.Sound("Flappy bird/sound/sfx_die.wav")
        self.hit_sound=pygame.mixer.Sound("Flappy bird/sound/sfx_hit.wav")
        self.point_sound=pygame.mixer.Sound("Flappy bird/sound/sfx_point.wav")
        self.fall_sound=pygame.mixer.Sound("Flappy bird/sound/sfx_swooshing.wav")


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        icon, self.background, floor_img = load_assets()
        pygame.display.set_icon(icon)
        self.pipe_image = pygame.image.load("Flappy bird/assets/pipe-green.png")
        self.pipe_image = pygame.transform.scale2x(self.pipe_image)

        self.pipes = []
        self.spawn_time = 0

        self.bird = Bird()
        self.floor = Floor(floor_img, FLOOR_Y)
        self.score = Score()
        self.sound=Sound()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(120)

            self.handle_events()
            self.update()
            self.check_collision()
            self.draw()

        self.game_over()
        pygame.display.update()
        # pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and self.running:
                    self.bird.velocity=-5
                    self.sound.jump_sound.play()
                    self.bird.swap=True


    def update(self):
        self.floor.update()
        self.bird.update()
        self.spawn_time += 1

        self.delay=random.randint(180,480)
        if self.spawn_time>self.delay:
            self.pipes.append(Pipe(self.pipe_image,self.bird))
            self.spawn_time=0

        for pipe in self.pipes:
            if not pipe.passed and pipe.top_rect.right<self.bird.rect.left:
                self.sound.point_sound.play()
                self.score.update()
                pipe.passed=True
            pipe.update()

        self.pipes = [pipe for pipe in self.pipes if not pipe.offscreen()]

    def check_collision(self):
        if self.bird.rect.top<=-75: 
            self.running=False
            self.sound.hit_sound.play()
            pygame.time.delay(500)
            self.sound.die_sound.play()

        if self.bird.rect.colliderect(self.floor.rect):
            self.running=False
            self.sound.hit_sound.play()
            pygame.time.delay(500)
            self.sound.die_sound.play()

        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or \
            self.bird.rect.colliderect(pipe.bottom_rect):
                self.running = False
                self.sound.hit_sound.play()
                pygame.time.delay(500)
                self.sound.die_sound.play()

    def draw(self):
        self.screen.blit(self.background,(0,0))   
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.floor.draw(self.screen)
        if self.running:
            self.bird.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.update()

    def restart(self):
        self.bird=Bird()
        self.pipes=[]
        self.spawn_time=0
        self.score.value=0
        self.running=True
        self.run()

    def game_over(self):
        if self.score.h_value<self.score.value: self.score.h_value=self.score.value
        self.screen_end=pygame.image.load("Flappy bird/assets/message.png")
        self.screen_end=pygame.transform.scale2x(self.screen_end)
        game_over=True;
        while game_over:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over=False
                    exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                        self.running=True
                        self.restart()
                        game_over=True
            
            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.screen_end,(71,174))
            self.score.end_draw(self.screen)

            pygame.display.update()
        pygame.quit()


# ==================================================
# FUNCTIONS
# ==================================================
def load_assets():
    icon=pygame.image.load("Flappy bird/assets/yellowbird-upflap.png")

    background=pygame.image.load("Flappy bird/assets/background-night.png")
    background=pygame.transform.scale2x(background)
    
    floor=pygame.image.load("Flappy bird/assets/floor.png")
    floor=pygame.transform.scale2x(floor)
    return icon,background,floor


# ==================================================
# MAIN
# ==================================================

game=Game()
game.run()