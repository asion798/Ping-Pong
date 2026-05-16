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

    # Метод управления правой ракеткой (для игры с другом)
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
    
    # ДОРАБОТКА 3: Метод управления правой ракеткой компьютером (ИИ)
    def update_ai(self, ball_rect):
        # Получаем центр правой ракетки
        paddle_center = self.rect.y + self.rect.height // 2
        # Получаем центр мяча
        ball_center = ball_rect.y + ball_rect.height // 2
        
        # Если мяч выше центра ракетки и ракетка не уперлась вверх
        if ball_center < paddle_center - 10 and self.rect.y > 5:
            # Двигаем ракетку вверх
            self.rect.y -= self.speed
        
        # Если мяч ниже центра ракетки и ракетка не уперлась вниз
        elif ball_center > paddle_center + 10 and self.rect.y < win_h - 135:
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
    
    # ДОРАБОТКА 1: Метод обновления позиции мяча с отскоками и счётом
    def update(self):
        # Двигаем мяч по горизонтали с учетом направления
        self.rect.x += self.speed * self.direction_x
        # Двигаем мяч по вертикали с учетом направления
        self.rect.y += self.speed * self.direction_y
        
        # Отскок от верхней и нижней стенки (меняем направление)
        if self.rect.y <= 0:
            self.direction_y *= -1
            # Немного сдвигаем мяч, чтобы он не залипал в стене
            self.rect.y = 0
        if self.rect.y >= win_h - self.rect.height:
            self.direction_y *= -1
            self.rect.y = win_h - self.rect.height
        
        # ДОРАБОТКА 1: Проверка гола (мяч коснулся левой или правой границы)
        # Если мяч коснулся левой стенки - очко получает правый игрок
        if self.rect.x <= 0:
            return "right_score"
        
        # Если мяч коснулся правой стенки - очко получает левый игрок
        elif self.rect.x >= win_w - self.rect.width:
            return "left_score"
        
        # Если мяч не коснулся стенок, возвращаем None (ничего не произошло)
        return None
    
    # ДОРАБОТКА 1: Метод сброса позиции мяча после гола (новая подача)
    def reset_position(self):
        # Ставим мяч в центр экрана по горизонтали
        self.rect.x = win_w // 2 - self.rect.width // 2
        # Ставим мяч в центр экрана по вертикали
        self.rect.y = win_h // 2 - self.rect.height // 2
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

# Создаем левого игрока (красная ракетка) - управляется игроком
# Параметры: картинка, x, y, ширина, высота, скорость
player_left = Player('red.png', 20, 225, 50, 150, 10)

# Создаем правого игрока (синяя ракетка)
player_right = Player('blue.png', win_w - 70, 225, 50, 150, 10)

# Создаем мяч
ball = Ball('ball.png', win_w // 2 - 25, win_h // 2 - 25, 50, 50, 5)

# Инициализируем модуль работы со шрифтами
font.init()
# Создаем шрифт для счета (размер 74)
score_font = font.Font(None, 74)
# Создаем шрифт для сообщений (размер 36)
message_font = font.Font(None, 36)

# Счет левого игрока
score_left = 0
# Счет правого игрока
score_right = 0
# Победитель (начинается как None - нет победителя)
winner = None
# Флаг окончания игры (False - игра идет, True - игра закончена)
finish = False

# ДОРАБОТКА 3: Режим игры (True - игра против компьютера, False - игра с другом)
vs_computer = True  # Можете изменить на False для игры с другом

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
    # Загружаем звук гола
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
        
        # ДОРАБОТКА 2: Проверка нажатия клавиши R для перезапуска матча
        if e.type == KEYDOWN:
            # Если нажата клавиша R (независимо от того, закончена игра или нет)
            if e.key == K_r:
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
        # Обновляем позицию левой ракетки (всегда управляется игроком)
        player_left.update_l()
        
        # ДОРАБОТКА 3: Выбор управления для правой ракетки
        if vs_computer:
            # Режим игры против компьютера - ИИ управляет правой ракеткой
            player_right.update_ai(ball.rect)
        else:
            # Режим игры с другом - стрелочки управляют правой ракеткой
            player_right.update_r()
        
        # Обновляем позицию мяча и получаем результат (кто получил очко)
        result = ball.update()
        
        # Проверяем столкновение мяча с левой ракеткой
        if sprite.collide_rect(ball, player_left):
            # Меняем направление мяча по горизонтали (отскок)
            ball.direction_x *= -1
            # Немного сдвигаем мяч, чтобы он не залипал в ракетке
            ball.rect.x = player_left.rect.x + player_left.rect.width
            # Воспроизводим звук удара, если он есть
            if hit_sound:
                hit_sound.play()
        
        # Проверяем столкновение мяча с правой ракеткой
        if sprite.collide_rect(ball, player_right):
            # Меняем направление мяча по горизонтали (отскок)
            ball.direction_x *= -1
            # Немного сдвигаем мяч, чтобы он не залипал в ракетке
            ball.rect.x = player_right.rect.x - ball.rect.width
            # Воспроизводим звук удара, если он есть
            if hit_sound:
                hit_sound.play()
        
        # ДОРАБОТКА 1: Обработка голов (мяч коснулся левой или правой границы)
        # Если мяч коснулся левой стены (очко правому игроку)
        if result == "right_score":
            # Увеличиваем счет правого игрока
            score_right += 1
            # Воспроизводим звук гола
            if score_sound:
                score_sound.play()
            # Возвращаем мяч в центр (новая подача)
            ball.reset_position()
        
        # Если мяч коснулся правой стены (очко левому игроку)
        elif result == "left_score":
            # Увеличиваем счет левого игрока
            score_left += 1
            # Воспроизводим звук гола
            if score_sound:
                score_sound.play()
            # Возвращаем мяч в центр (новая подача)
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
        
        # ДОРАБОТКА 3: Отображаем режим игры на экране
        if vs_computer:
            mode_text = message_font.render("Режим: Против компьютера (нажмите F1 для игры с другом)", True, (200, 200, 200))
        else:
            mode_text = message_font.render("Режим: 2 игрока (нажмите F1 для игры с компьютером)", True, (200, 200, 200))
        window.blit(mode_text, (10, win_h - 25))
        
        # ДОРАБОТКА 2: Отображаем подсказку о перезапуске
        restart_hint = message_font.render("Нажмите R для перезапуска матча", True, (200, 200, 200))
        window.blit(restart_hint, (win_w - 220, win_h - 25))
    
    else:
        # ========== ЭКРАН ПОБЕДЫ ==========
        # Создаем текст с именем победителя
        win_text = score_font.render(f"Победил {winner}!", True, (255, 255, 0))
        # Создаем текст с инструкцией по перезапуску
        restart_text = message_font.render("Нажмите R для новой игры", True, (255, 255, 255))
        
        # Рисуем фон
        window.blit(background, (0, 0))
        # Отображаем текст победителя (по центру)
        window.blit(win_text, (win_w // 2 - win_text.get_width() // 2, win_h // 2 - 50))
        # Отображаем инструкцию по перезапуску
        window.blit(restart_text, (win_w // 2 - restart_text.get_width() // 2, win_h // 2 + 50))
        
        # Отображаем подсказку о переключении режима
        mode_text = message_font.render("Нажмите F1 для смены режима игры", True, (200, 200, 200))
        window.blit(mode_text, (win_w // 2 - mode_text.get_width() // 2, win_h // 2 + 100))
    
    # ДОРАБОТКА 3: Переключение режима игры по клавише F1
    keys = key.get_pressed()
    if keys[K_F1]:
        # Меняем режим с компьютера на друга и наоборот
        vs_computer = not vs_computer
        # Сбрасываем игру при смене режима
        score_left = 0
        score_right = 0
        finish = False
        winner = None
        ball.reset_position()
        player_left.rect.y = 225
        player_right.rect.y = 225
        # Небольшая задержка, чтобы не сработало несколько раз подряд
        time.delay(200)
    
    # Обновляем содержимое окна
    display.update()
    # Ограничиваем количество кадров в секунду
    clock.tick(FPS)