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
        img = image.load(player_image)
        
        # Масштабируем изображение до нужных размеров
        self.image = transform.scale(img, (size_x, size_y))
        
        # Убираем белый фон (цвет 255,255,255 делаем прозрачным)
        self.image.set_colorkey((255, 255, 255))
        
        # Конвертируем изображение с альфа-каналом для плавной прозрачности
        self.image = self.image.convert_alpha()
        
        # Сохраняем скорость движения спрайта
        self.speed = player_speed
        
        # Получаем прямоугольную область, которую занимает спрайт (для столкновений)
        self.rect = self.image.get_rect()
        
        # Устанавливаем начальную позицию спрайта по X
        self.rect.x = player_x
        # Устанавливаем начальную позицию спрайта по Y
        self.rect.y = player_y
    
    # Метод для отображения спрайта на экране
    def reset(self):
        # Рисуем изображение спрайта на окне в его текущей позиции
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока (ракетки), наследуется от GameSprite
class Player(GameSprite):
    # Метод управления левой ракеткой (клавиши W и S)
    def update_l(self):
        # Получаем список всех нажатых клавиш
        keys = key.get_pressed()
        
        # Если нажата клавиша W и ракетка не уперлась в верхнюю границу
        if keys[K_w] and self.rect.y > 5:
            # Двигаем ракетку вверх (уменьшаем координату Y)
            self.rect.y -= self.speed
        
        # Если нажата клавиша S и ракетка не уперлась в нижнюю границу
        if keys[K_s] and self.rect.y < win_h - 135:
            # Двигаем ракетку вниз (увеличиваем координату Y)
            self.rect.y += self.speed

    # Метод управления правой ракеткой (клавиши стрелки вверх и вниз)
    def update_r(self):
        # Получаем список всех нажатых клавиш
        keys = key.get_pressed()
        
        # Если нажата стрелка вверх и ракетка не уперлась в верхнюю границу
        if keys[K_UP] and self.rect.y > 5:
            # Двигаем ракетку вверх
            self.rect.y -= self.speed
        
        # Если нажата стрелка вниз и ракетка не уперлась в нижнюю границу
        if keys[K_DOWN] and self.rect.y < win_h - 135:
            # Двигаем ракетку вниз
            self.rect.y += self.speed

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
    
    # Метод обновления позиции мяча
    def update(self):
        # Двигаем мяч по горизонтали с учетом направления
        self.rect.x += self.speed * self.direction_x
        # Двигаем мяч по вертикали с учетом направления
        self.rect.y += self.speed * self.direction_y
        
        # Если мяч коснулся верхней или нижней границы
        if self.rect.y <= 0 or self.rect.y >= win_h - 50:
            # Меняем направление по вертикали на противоположное (отскок)
            self.direction_y *= -1
        
        # Если мяч коснулся левой стенки
        if self.rect.x <= 0:
            # Возвращаем сигнал, что правый игрок получил очко
            return "right_score"
        
        # Если мяч коснулся правой стенки
        elif self.rect.x >= win_w - 50:
            # Возвращаем сигнал, что левый игрок получил очко
            return "left_score"
        
        # Если мяч не коснулся стенок, возвращаем None (ничего не произошло)
        return None
    
    # Метод сброса позиции мяча после начисления очка
    def reset_position(self):
        # Ставим мяч в центр экрана по горизонтали
        self.rect.x = win_w // 2
        # Ставим мяч в центр экрана по вертикали
        self.rect.y = win_h // 2
        # Случайно выбираем начальное направление по горизонтали
        self.direction_x = 1 if randint(0, 1) else -1
        # Случайно выбираем начальное направление по вертикали
        self.direction_y = 1 if randint(0, 1) else -1

# ========== НАСТРОЙКИ ИГРЫ ==========

# Ширина окна игры
win_w = 700
# Высота окна игры
win_h = 500

# Создаем игровое окно с указанными размерами
window = display.set_mode((win_w, win_h))
# Устанавливаем заголовок окна
display.set_caption('Ping-Pong')

# Загрузка фонового изображения
background = transform.scale(
    image.load("background.jpg"),  # Загружаем файл с фоном
    (win_w, win_h)  # Масштабируем под размер окна
)

# Создаем левого игрока (красная ракетка)
# Параметры: картинка, x, y, ширина, высота, скорость
player_left = Player('red.png', 20, 225, 50, 150, 10)

# Создаем правого игрока (синяя ракетка)
player_right = Player('blue.png', win_w - 70, 225, 50, 150, 10)

# Создаем мяч
ball = Ball('ball.png', win_w // 2, win_h // 2, 50, 50, 5)

# Инициализируем модуль работы со шрифтами
font.init()
# Создаем шрифт для счета (размер 74)
score_font = font.Font(None, 74)

# Счет левого игрока
score_left = 0
# Счет правого игрока
score_right = 0
# Победитель (начинается как None - нет победителя)
winner = None
# Флаг окончания игры (False - игра идет, True - игра закончена)
finish = False

# Создаем игровой таймер
clock = time.Clock()
# Количество кадров в секунду
FPS = 60
# Флаг работы игры (True - игра работает, False - выход)
run = True

# ========== НАСТРОЙКА ЗВУКОВ (опционально) ==========
try:
    # Инициализируем звуковой модуль
    mixer.init()
    # Загружаем звук удара мяча о ракетку
    hit_sound = mixer.Sound('hit.wav')
    # Загружаем звук начисления очка
    score_sound = mixer.Sound('score.wav')
except:
    # Если звуковые файлы не найдены, отключаем звуки
    hit_sound = None
    score_sound = None

# ========== ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ ==========
while run:
    # Перебираем все события, произошедшие в игре
    for e in event.get():
        # Если нажата кнопка закрытия окна
        if e.type == QUIT:
            # Завершаем игру
            run = False
        
        # Если игра закончена и нажата клавиша
        if e.type == KEYDOWN and finish:
            # Если нажат пробел
            if e.key == K_SPACE:
                # Сбрасываем счет левого игрока
                score_left = 0
                # Сбрасываем счет правого игрока
                score_right = 0
                # Возобновляем игру
                finish = False
                # Сбрасываем победителя
                winner = None
                # Возвращаем мяч в центр
                ball.reset_position()
                # Возвращаем левую ракетку в начальное положение
                player_left.rect.y = 225
                # Возвращаем правую ракетку в начальное положение
                player_right.rect.y = 225
    
    # Если игра не закончена
    if not finish:
        # Обновляем позицию левой ракетки
        player_left.update_l()
        # Обновляем позицию правой ракетки
        player_right.update_r()
        
        # Обновляем позицию мяча и получаем результат (кто получил очко)
        result = ball.update()
        
        # Проверяем столкновение мяча с ракетками
        if sprite.collide_rect(ball, player_left) or sprite.collide_rect(ball, player_right):
            # Меняем направление мяча по горизонтали (отскок)
            ball.direction_x *= -1
            # Воспроизводим звук удара, если он есть
            if hit_sound:
                hit_sound.play()
        
        # Если мяч коснулся левой стены (очко левому игроку)
        if result == "left_score":
            # Увеличиваем счет левого игрока
            score_left += 1
            # Воспроизводим звук очка
            if score_sound:
                score_sound.play()
            # Возвращаем мяч в центр
            ball.reset_position()
        
        # Если мяч коснулся правой стены (очко правому игроку)
        elif result == "right_score":
            # Увеличиваем счет правого игрока
            score_right += 1
            # Воспроизводим звук очка
            if score_sound:
                score_sound.play()
            # Возвращаем мяч в центр
            ball.reset_position()
        
        # Проверяем победу (игра до 5 очков)
        if score_left >= 5:
            # Победил левый игрок
            winner = "Левый игрок"
            # Завершаем игру
            finish = True
        elif score_right >= 5:
            # Победил правый игрок
            winner = "Правый игрок"
            # Завершаем игру
            finish = True
        
        # ========== ОТРИСОВКА ИГРЫ ==========
        # Рисуем фон
        window.blit(background, (0, 0))
        # Рисуем левую ракетку
        player_left.reset()
        # Рисуем правую ракетку
        player_right.reset()
        # Рисуем мяч
        ball.reset()
        
        # Создаем текстовое изображение счета левого игрока
        left_text = score_font.render(str(score_left), True, (255, 255, 255))
        # Создаем текстовое изображение счета правого игрока
        right_text = score_font.render(str(score_right), True, (255, 255, 255))
        # Отображаем счет левого игрока
        window.blit(left_text, (win_w // 4, 20))
        # Отображаем счет правого игрока
        window.blit(right_text, (win_w * 3 // 4 - 50, 20))
    
    else:
        # ========== ЭКРАН ПОБЕДЫ ==========
        # Создаем текст с именем победителя
        win_text = score_font.render(f"Победил {winner}!", True, (255, 255, 0))
        # Создаем текст с инструкцией по перезапуску
        restart_text = font.Font(None, 36).render("Нажмите ПРОБЕЛ для новой игры", True, (255, 255, 255))
        
        # Рисуем фон
        window.blit(background, (0, 0))
        # Отображаем текст победителя (по центру)
        window.blit(win_text, (win_w // 2 - win_text.get_width() // 2, win_h // 2 - 50))
        # Отображаем инструкцию по перезапуску
        window.blit(restart_text, (win_w // 2 - restart_text.get_width() // 2, win_h // 2 + 50))
    
    # Обновляем содержимое окна
    display.update()
    # Ограничиваем количество кадров в секунду
    clock.tick(FPS)