# Импортируем все функции и классы из библиотеки pygame
from pygame import *
# Импортируем функцию randint для генерации случайных чисел
from random import randint

# Базовый класс для всех игровых спрайтов (ракеток и мяча)
class GameSprite(sprite.Sprite):
    # Конструктор класса - вызывается при создании объекта
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор родительского класса Sprite
        super().__init__()
        
        # Загружаем изображение из файла
        self.original_image = image.load(player_image)
        
        # Сохраняем оригинальные размеры (в процентах от окна)
        self.orig_width_percent = size_x
        self.orig_height_percent = size_y
        
        # Масштабируем изображение до нужных размеров
        self.image = transform.scale(self.original_image, (size_x, size_y))
        
        # Убираем белый фон (цвет 255,255,255 делаем прозрачным)
        self.image.set_colorkey((255, 255, 255))
        
        # Конвертируем изображение с альфа-каналом для плавной прозрачности
        self.image = self.image.convert_alpha()
        
        # Сохраняем скорость движения спрайта
        self.speed = player_speed
        
        # Получаем прямоугольную область, которую занимает спрайт (для столкновений)
        self.rect = self.image.get_rect()
        
        # Устанавливаем начальную позицию спрайта по X (в процентах от ширины окна)
        self.rect.x = player_x
        # Устанавливаем начальную позицию спрайта по Y (в процентах от высоты окна)
        self.rect.y = player_y
    
    # Метод для обновления размера спрайта при изменении окна
    def update_scale(self, win_w, win_h):
        # Вычисляем новые размеры в пикселях
        new_width = int(win_w * self.orig_width_percent / 100)
        new_height = int(win_h * self.orig_height_percent / 100)
        
        # Масштабируем изображение
        self.image = transform.scale(self.original_image, (new_width, new_height))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()
        
        # Сохраняем старую позицию в процентах
        old_x_percent = self.rect.x / old_win_w if old_win_w > 0 else 0
        old_y_percent = self.rect.y / old_win_h if old_win_h > 0 else 0
        
        # Обновляем прямоугольник
        old_center_y = self.rect.centery
        self.rect = self.image.get_rect()
        
        # Устанавливаем новую позицию в процентах от нового окна
        self.rect.x = int(win_w * old_x_percent)
        self.rect.y = int(win_h * old_y_percent)
        
        return new_width, new_height
    
    # Метод для отображения спрайта на экране
    def reset(self):
        # Рисуем изображение спрайта на окне в его текущей позиции
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока (ракетки), наследуется от GameSprite
class Player(GameSprite):
    # Метод управления левой ракеткой (клавиши W и S)
    def update_l(self, win_h):
        # Получаем список всех нажатых клавиш
        keys = key.get_pressed()
        
        # Если нажата клавиша W и ракетка не уперлась в верхнюю границу
        if keys[K_w] and self.rect.y > 5:
            # Двигаем ракетку вверх (уменьшаем координату Y)
            self.rect.y -= self.speed
        
        # Если нажата клавиша S и ракетка не уперлась в нижнюю границу
        if keys[K_s] and self.rect.y < win_h - self.rect.height - 5:
            # Двигаем ракетку вниз (увеличиваем координату Y)
            self.rect.y += self.speed
    
    # Метод обновления позиции с учетом нового размера окна
    def update_position(self, win_h):
        # Проверяем, не вышла ли ракетка за границы
        if self.rect.y < 5:
            self.rect.y = 5
        if self.rect.y > win_h - self.rect.height - 5:
            self.rect.y = win_h - self.rect.height - 5

    # Метод управления правой ракеткой (для игры с другом)
    def update_r(self, win_h):
        # Получаем список всех нажатых клавиш
        keys = key.get_pressed()
        
        # Если нажата стрелка вверх и ракетка не уперлась в верхнюю границу
        if keys[K_UP] and self.rect.y > 5:
            # Двигаем ракетку вверх
            self.rect.y -= self.speed
        
        # Если нажата стрелка вниз и ракетка не уперлась в нижнюю границу
        if keys[K_DOWN] and self.rect.y < win_h - self.rect.height - 5:
            # Двигаем ракетку вниз
            self.rect.y += self.speed
    
    # Метод управления правой ракеткой компьютером (ИИ) с разной сложностью
    def update_ai(self, ball_rect, win_h, difficulty):
        # Получаем центр правой ракетки
        paddle_center = self.rect.y + self.rect.height // 2
        # Получаем центр мяча
        ball_center = ball_rect.y + ball_rect.height // 2
        
        # Разная точность слежения в зависимости от сложности
        if difficulty == "easy":
            # Лёгкий уровень: бот реагирует с задержкой и большим отклонением
            error_margin = int(win_h * 0.1)  # 10% от высоты экрана
            bot_speed = self.speed * 0.5
        elif difficulty == "medium":
            # Средний уровень: средняя точность
            error_margin = int(win_h * 0.05)  # 5% от высоты экрана
            bot_speed = self.speed * 0.8
        else:  # hard
            # Сложный уровень: высокая точность
            error_margin = int(win_h * 0.02)  # 2% от высоты экрана
            bot_speed = self.speed
        
        # Если мяч выше центра ракетки с учётом погрешности
        if ball_center < paddle_center - error_margin and self.rect.y > 5:
            # Двигаем ракетку вверх
            self.rect.y -= bot_speed
        
        # Если мяч ниже центра ракетки с учётом погрешности
        elif ball_center > paddle_center + error_margin and self.rect.y < win_h - self.rect.height - 5:
            # Двигаем ракетку вниз
            self.rect.y += bot_speed

# Класс мяча, наследуется от GameSprite
class Ball(GameSprite):
    # Конструктор мяча
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор родительского класса
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        
        # Направление движения по горизонтали (1 - вправо, -1 - влево)
        self.direction_x = 1
        # Направление движения по вертикали (1 - вниз, -1 - вверх)
        self.direction_y = 1
        # Начальная скорость мяча (в пикселях в секунду)
        self.base_speed = player_speed
        # Текущая скорость мяча
        self.current_speed = player_speed
    
    # Метод обновления позиции мяча с отскоками и счётом
    def update(self, win_w, win_h):
        # Двигаем мяч по горизонтали с учетом направления
        self.rect.x += self.current_speed * self.direction_x
        # Двигаем мяч по вертикали с учетом направления
        self.rect.y += self.current_speed * self.direction_y
        
        # Отскок от верхней и нижней стенки (меняем направление)
        if self.rect.y <= 0:
            self.direction_y *= -1
            self.rect.y = 0
        if self.rect.y >= win_h - self.rect.height:
            self.direction_y *= -1
            self.rect.y = win_h - self.rect.height
        
        # Проверка гола (мяч коснулся левой или правой границы)
        if self.rect.x <= 0:
            return "right_score"
        elif self.rect.x >= win_w - self.rect.width:
            return "left_score"
        
        return None
    
    # Метод сброса позиции мяча после гола (новая подача)
    def reset_position(self, win_w, win_h):
        # Ставим мяч в центр экрана
        self.rect.x = win_w // 2 - self.rect.width // 2
        self.rect.y = win_h // 2 - self.rect.height // 2
        # Случайно выбираем начальное направление
        self.direction_x = 1 if randint(0, 1) else -1
        self.direction_y = 1 if randint(0, 1) else -1
        # Сбрасываем скорость до базовой
        self.current_speed = self.base_speed
    
    # Метод ускорения мяча при отскоке
    def speed_up(self):
        # Увеличиваем скорость на 5% при каждом отскоке, но не более чем в 2 раза
        self.current_speed = min(self.current_speed * 1.05, self.base_speed * 2)
    
    # Метод получения текущей скорости (для отображения)
    def get_speed_percent(self):
        return int((self.current_speed / self.base_speed) * 100)

# ========== НАСТРОЙКИ ИГРЫ ==========

# Начальные размеры окна
win_w = 1000
win_h = 700

# Создаем изменяемое окно (RESIZABLE позволяет менять размер)
window = display.set_mode((win_w, win_h), RESIZABLE)
# Устанавливаем заголовок окна
display.set_caption('Ping-Pong - Тяните за края или F11 для полноэкранного режима')

# Загрузка фонового изображения
background = transform.scale(
    image.load("background.jpg"),
    (win_w, win_h)
)

# СОЗДАНИЕ ОБЪЕКТОВ С ОТНОСИТЕЛЬНЫМИ РАЗМЕРАМИ (в процентах от окна)
# Размеры в процентах: ширина 5% от окна, высота 20% от окна
player_width_percent = 5
player_height_percent = 20

# Левая ракетка (x=2% от ширины, y=40% от высоты)
player_left = Player('red.png', 
                     int(win_w * 0.02), 
                     int(win_h * 0.4), 
                     int(win_w * player_width_percent / 100), 
                     int(win_h * player_height_percent / 100), 
                     int(win_h * 0.03))  # скорость = 3% от высоты экрана

# Правая ракетка (x=93% от ширины)
player_right = Player('blue.png', 
                      int(win_w * 0.93), 
                      int(win_h * 0.4), 
                      int(win_w * player_width_percent / 100), 
                      int(win_h * player_height_percent / 100), 
                      int(win_h * 0.03))

# Мяч (размер 4% от ширины окна)
ball_size = int(win_w * 0.04)
ball = Ball('ball.png', 
            win_w // 2 - ball_size // 2, 
            win_h // 2 - ball_size // 2, 
            ball_size, 
            ball_size, 
            int(win_h * 0.01))  # скорость = 1% от высоты экрана

# Обновляем оригинальные размеры в процентах для всех объектов
player_left.orig_width_percent = player_width_percent
player_left.orig_height_percent = player_height_percent
player_right.orig_width_percent = player_width_percent
player_right.orig_height_percent = player_height_percent
ball.orig_width_percent = 4
ball.orig_height_percent = 4

# Инициализируем модуль работы со шрифтами
font.init()
# Шрифты будут создаваться динамически при изменении размера окна

# Счет левого игрока
score_left = 0
# Счет правого игрока
score_right = 0
# Победитель
winner = None
# Флаг окончания игры
finish = False

# Режим игры
vs_computer = True
# Сложность бота
difficulties = ["easy", "medium", "hard"]
difficulty_index = 1
bot_difficulty = difficulties[difficulty_index]

# Создаем игровой таймер
clock = time.Clock()
FPS = 60
run = True

# Переменные для отслеживания изменения размера окна
old_win_w = win_w
old_win_h = win_h
fullscreen = False

# ========== НАСТРОЙКА ЗВУКОВ ==========
try:
    mixer.init()
    hit_sound = mixer.Sound('hit.wav')
    score_sound = mixer.Sound('score.wav')
except:
    hit_sound = None
    score_sound = None

# ========== ФУНКЦИЯ ДЛЯ ОБНОВЛЕНИЯ РАЗМЕРОВ ОКНА ==========
def resize_window(new_w, new_h):
    global win_w, win_h, background, old_win_w, old_win_h
    
    # Обновляем размеры окна
    win_w = new_w
    win_h = new_h
    
    # Пересоздаем фон с новым размером
    background = transform.scale(
        image.load("background.jpg"),
        (win_w, win_h)
    )
    
    # Обновляем размеры и позиции всех спрайтов
    player_left.update_scale(win_w, win_h)
    player_right.update_scale(win_w, win_h)
    ball.update_scale(win_w, win_h)
    
    # Обновляем скорость объектов (относительно высоты экрана)
    player_left.speed = int(win_h * 0.03)
    player_right.speed = int(win_h * 0.03)
    ball.base_speed = int(win_h * 0.01)
    ball.current_speed = ball.base_speed
    
    # Проверяем границы
    player_left.update_position(win_h)
    player_right.update_position(win_h)
    
    # Обновляем старые размеры
    old_win_w = win_w
    old_win_h = win_h

# ========== ФУНКЦИЯ ДЛЯ ПЕРЕКЛЮЧЕНИЯ ПОЛНОЭКРАННОГО РЕЖИМА ==========
def toggle_fullscreen():
    global fullscreen, window, win_w, win_h
    
    fullscreen = not fullscreen
    
    if fullscreen:
        # Переключаемся в полноэкранный режим
        window = display.set_mode((0, 0), FULLSCREEN)
        win_w, win_h = window.get_size()
    else:
        # Возвращаемся в оконный режим
        window = display.set_mode((1000, 700), RESIZABLE)
        win_w, win_h = 1000, 700
    
    # Обновляем все объекты под новый размер окна
    resize_window(win_w, win_h)

# ========== ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ ==========
while run:
    # Перебираем все события
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        # Обработка изменения размера окна
        if e.type == VIDEORESIZE and not fullscreen:
            window = display.set_mode((e.w, e.h), RESIZABLE)
            resize_window(e.w, e.h)
        
        # Проверка нажатия клавиш
        if e.type == KEYDOWN:
            # Перезапуск матча по R
            if e.key == K_r:
                score_left = 0
                score_right = 0
                finish = False
                winner = None
                ball.reset_position(win_w, win_h)
                player_left.rect.y = win_h // 2 - player_left.rect.height // 2
                player_right.rect.y = win_h // 2 - player_right.rect.height // 2
            
            # Переключение сложности бота по клавише D
            if e.key == K_d and vs_computer:
                difficulty_index = (difficulty_index + 1) % 3
                bot_difficulty = difficulties[difficulty_index]
                time.delay(200)
            
            # Переключение полноэкранного режима по F11
            if e.key == K_F11:
                toggle_fullscreen()
    
    # Если игра не закончена
    if not finish:
        # Обновляем позицию левой ракетки (игрок)
        player_left.update_l(win_h)
        
        # Выбор управления для правой ракетки
        if vs_computer:
            player_right.update_ai(ball.rect, win_h, bot_difficulty)
        else:
            player_right.update_r(win_h)
        
        # Обновляем позицию мяча
        result = ball.update(win_w, win_h)
        
        # Проверяем столкновение мяча с ракетками
        if sprite.collide_rect(ball, player_left):
            ball.direction_x *= -1
            ball.rect.x = player_left.rect.x + player_left.rect.width
            ball.speed_up()
            if hit_sound:
                hit_sound.play()
        
        if sprite.collide_rect(ball, player_right):
            ball.direction_x *= -1
            ball.rect.x = player_right.rect.x - ball.rect.width
            ball.speed_up()
            if hit_sound:
                hit_sound.play()
        
        # Обработка голов
        if result == "right_score":
            score_right += 1
            if score_sound:
                score_sound.play()
            ball.reset_position(win_w, win_h)
        elif result == "left_score":
            score_left += 1
            if score_sound:
                score_sound.play()
            ball.reset_position(win_w, win_h)
        
        # Проверка победы (игра до 5 очков)
        if score_left >= 5:
            winner = "Левый игрок"
            finish = True
        elif score_right >= 5:
            winner = "Правый игрок"
            finish = True
        
        # ========== ОТРИСОВКА ИГРЫ ==========
        window.blit(background, (0, 0))
        player_left.reset()
        player_right.reset()
        ball.reset()
        
        # Динамический размер шрифтов (относительно размера окна)
        score_font = font.Font(None, int(win_h * 0.1))
        message_font = font.Font(None, int(win_h * 0.035))
        
        # Отображение счета
        left_text = score_font.render(str(score_left), True, (255, 255, 255))
        right_text = score_font.render(str(score_right), True, (255, 255, 255))
        window.blit(left_text, (win_w // 4 - left_text.get_width() // 2, 20))
        window.blit(right_text, (win_w * 3 // 4 - right_text.get_width() // 2, 20))
        
        # Отображение скорости мяча
        speed_text = message_font.render(f"Скорость мяча: {ball.get_speed_percent()}%", True, (255, 255, 0))
        window.blit(speed_text, (win_w // 2 - speed_text.get_width() // 2, 10))
        
        # Отображение режима игры (внизу слева)
        if vs_computer:
            if bot_difficulty == "easy":
                diff_text = "ЛЁГКИЙ"
                diff_color = (0, 255, 0)
            elif bot_difficulty == "medium":
                diff_text = "СРЕДНИЙ"
                diff_color = (255, 255, 0)
            else:
                diff_text = "СЛОЖНЫЙ"
                diff_color = (255, 0, 0)
            mode_text = message_font.render(f"ПРОТИВ КОМПА [{diff_text}]", True, diff_color)
        else:
            mode_text = message_font.render("2 ИГРОКА", True, (200, 200, 200))
        window.blit(mode_text, (10, win_h - mode_text.get_height() - 10))
        
        # Отображение подсказок (внизу)
        hint1 = message_font.render("W/S - движение | R - рестарт | D - сложность | F1 - режим | F11 - полный экран", True, (200, 200, 200))
        window.blit(hint1, (win_w // 2 - hint1.get_width() // 2, win_h - hint1.get_height() - 5))
    
    else:
        # ========== ЭКРАН ПОБЕДЫ ==========
        win_font = font.Font(None, int(win_h * 0.08))
        msg_font = font.Font(None, int(win_h * 0.04))
        
        win_text = win_font.render(f"Победил {winner}!", True, (255, 255, 0))
        restart_text = msg_font.render("Нажмите R для новой игры", True, (255, 255, 255))
        
        window.blit(background, (0, 0))
        window.blit(win_text, (win_w // 2 - win_text.get_width() // 2, win_h // 2 - 50))
        window.blit(restart_text, (win_w // 2 - restart_text.get_width() // 2, win_h // 2 + 50))
    
    # Переключение режима игры по клавише F1
    keys = key.get_pressed()
    if keys[K_F1]:
        vs_computer = not vs_computer
        score_left = 0
        score_right = 0
        finish = False
        winner = None
        ball.reset_position(win_w, win_h)
        player_left.rect.y = win_h // 2 - player_left.rect.height // 2
        player_right.rect.y = win_h // 2 - player_right.rect.height // 2
        time.delay(200)
    
    # Обновляем содержимое окна
    display.update()
    clock.tick(FPS)