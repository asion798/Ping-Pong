from pygame import *
from random import randint, random

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.x < win_w - 70:
            self.rect.x += self.speed

    def update_r(self):
        pass
class Ball(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_h:
            self.rect.y = randint(-65, 0)
            self.rect.x = randint(20, win_w - 20)

win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))

display.set_caption("Ping-Pong")

background = transform.scale(
    image.load("background.jpg"),
    (win_w, win_h)
)

clock = time.Clock()
FPS = 60
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.blit(background, (0, 0))

    display.update()
    clock.tick(FPS)