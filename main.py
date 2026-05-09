from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.image.set_colorkey((255, 255, 255))  # Убираем белый фон
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed 
        if keys[K_s] and self.rect.y < win_h - 135:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed 
        if keys[K_DOWN] and self.rect.y < win_h - 135:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction_x = 1  # Направление по X (1 - вправо, -1 - влево)
        self.direction_y = 1  # Направление по Y (1 - вниз, -1 - вверх)
    
    def update(self):
        # Движение мяча
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        
        # Отскок от верхней и нижней стенки
        if self.rect.y <= 0 or self.rect.y >= win_h - 50:
            self.direction_y *= -1  # Меняем направление
        
        # Коснулись левой стенки - выиграл 2 игрок
        if self.rect.x <= 0:
            return "right_score"  # Очко правому игроку
        
        # Коснулись правой стенки - выиграл 1 игрок
        elif self.rect.x >= win_w - 50:
            return "left_score"  # Очко левому игроку
        
        return None  # Никто не выиграл
    
    def reset_position(self):
        """Сброс позиции мяча после очка"""
        self.rect.x = win_w // 2
        self.rect.y = win_h // 2
        self.direction_x = 1 if randint(0, 1) else -1  # Случайное направление
        self.direction_y = 1 if randint(0, 1) else -1

win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
display.set_caption("Ping-Pong")

# Загрузка фона
background = transform.scale(
    image.load("background.jpg"),
    (win_w, win_h)
)

# Игроки
player_left = Player('red.png', 20, 225, 50, 150, 10)
player_right = Player('blue.png', win_w - 70, 225, 50, 150, 10)

# Мяч
ball = Ball('ball.png', win_w // 2, win_h // 2, 50, 50, 5)

# Счет
font.init()
score_font = font.Font(None, 74)
score_left = 0
score_right = 0
winner = None  # Победитель: "left" или "right"

clock = time.Clock()
FPS = 60
run = True
finish = False

# Звук (опционально)
try:
    mixer.init()
    hit_sound = mixer.Sound('hit.wav')  # Добавьте звук при ударе
    score_sound = mixer.Sound('score.wav')
except:
    hit_sound = None
    score_sound = None

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and finish:
            # Перезапуск игры по пробелу
            if e.key == K_SPACE:
                score_left = 0
                score_right = 0
                finish = False
                winner = None
                ball.reset_position()
                # Сброс позиций игроков
                player_left.rect.y = 225
                player_right.rect.y = 225
    
    if not finish:
        # Обновление игроков
        player_left.update_l()
        player_right.update_r()
        
        # Обновление мяча
        result = ball.update()
        
        # Проверка отскока от ракеток
        if sprite.collide_rect(ball, player_left) or sprite.collide_rect(ball, player_right):
            ball.direction_x *= -1  # Отскок
            if hit_sound:
                hit_sound.play()
        
        # Проверка очков
        if result == "left_score":
            score_left += 1
            if score_sound:
                score_sound.play()
            ball.reset_position()
        elif result == "right_score":
            score_right += 1
            if score_sound:
                score_sound.play()
            ball.reset_position()
        
        # Проверка победы (до 5 очков)
        if score_left >= 5:
            winner = "Левый игрок"
            finish = True
        elif score_right >= 5:
            winner = "Правый игрок"
            finish = True
        
        # Отрисовка
        window.blit(background, (0, 0))
        player_left.reset()
        player_right.reset()
        ball.reset()
        
        # Отображение счета
        left_text = score_font.render(str(score_left), True, (255, 255, 255))
        right_text = score_font.render(str(score_right), True, (255, 255, 255))
        window.blit(left_text, (win_w // 4, 20))
        window.blit(right_text, (win_w * 3 // 4 - 50, 20))
    
    else:
        # Экран победы
        win_text = score_font.render(f"Победил {winner}!", True, (255, 255, 0))
        restart_text = font.Font(None, 36).render("Нажмите ПРОБЕЛ для новой игры", True, (255, 255, 255))
        
        window.blit(background, (0, 0))
        window.blit(win_text, (win_w // 2 - win_text.get_width() // 2, win_h // 2 - 50))
        window.blit(restart_text, (win_w // 2 - restart_text.get_width() // 2, win_h // 2 + 50))
    
    display.update()
    clock.tick(FPS)