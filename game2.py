import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Escape")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

# Игровые параметры
PLAYER_SIZE = 50
PLAYER_POS = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]
PLAYER_SPEED = 10

ASTEROID_SIZE = 50
ASTEROID_SPEED = 7

BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 15

score = 0
game_over = False

clock = pygame.time.Clock()

# Загрузка изображений (замени на свои изображения)
try:
    player_image = pygame.image.load('image/Без названия (3).jpeg')
    asteroid_image = pygame.image.load('image/Без названия (2).jpeg')
except pygame.error as e:
    print(f"Ошибка загрузки изображения: {e}")
    pygame.quit()
    sys.exit()

player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
asteroid_image = pygame.transform.scale(asteroid_image, (ASTEROID_SIZE, ASTEROID_SIZE))

# Класс для пули
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)

    def move(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)

# Функция для создания астероида
def drop_asteroids(asteroid_list):
    delay = random.random()
    if len(asteroid_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - ASTEROID_SIZE)
        asteroid_list.append([x_pos, 0])

# Функция для отрисовки астероидов
def draw_asteroids(asteroid_list):
    for asteroid_pos in asteroid_list:
        screen.blit(asteroid_image, (asteroid_pos[0], asteroid_pos[1]))

# Функция для обновления позиции астероидов
def update_asteroid_positions(asteroid_list, current_score):
    for asteroid_pos in asteroid_list[:]:
        if 0 <= asteroid_pos[1] < HEIGHT:
            asteroid_pos[1] += ASTEROID_SPEED
        else:
            asteroid_list.remove(asteroid_pos)
            current_score += 1
    return current_score

# Функция для проверки столкновения
def collision_check(asteroid_list, player_pos):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    for asteroid_pos in asteroid_list:
        asteroid_rect = pygame.Rect(asteroid_pos[0], asteroid_pos[1], ASTEROID_SIZE, ASTEROID_SIZE)
        if player_rect.colliderect(asteroid_rect):
            return True
    return False

# Функция для проверки столкновений пуль и астероидов
def bullet_collision_check(bullet_list, asteroid_list, current_score):
    for bullet in bullet_list[:]:
        bullet_rect = bullet.rect
        for asteroid in asteroid_list[:]:
            asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], ASTEROID_SIZE, ASTEROID_SIZE)
            if bullet_rect.colliderect(asteroid_rect):
                bullet_list.remove(bullet)
                asteroid_list.remove(asteroid)
                current_score += 1
                break
    return current_score

# Класс кнопки
class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.font = pygame.font.SysFont("monospace", 40)

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse):
            pygame.draw.rect(surface, self.active_color, self.rect)
            if click[0] == 1 and self.action:
                pygame.time.delay(200)  # Небольшая задержка для предотвращения множественных срабатываний
                self.action()
        else:
            pygame.draw.rect(surface, self.inactive_color, self.rect)

        text_surface = self.font.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

# Функция для выхода из игры
def quit_game():
    pygame.quit()
    sys.exit()

# Функция для запуска игры
def start_game():
    game_loop()

# Меню игры
def game_menu():
    menu = True

    # Создание кнопок
    start_button = Button("Start", WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, GRAY, DARK_GRAY, start_game)
    exit_button = Button("Exit", WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, GRAY, DARK_GRAY, quit_game)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        screen.fill(BLACK)

        # Отрисовка заголовка
        font = pygame.font.SysFont("monospace", 70)
        title = font.render("SPACE ESCAPE", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        # Отрисовка кнопок
        start_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(30)

# Основной игровой цикл
def game_loop():
    global score, game_over, PLAYER_POS

    asteroid_list = []
    bullet_list = []
    game_over = False
    score = 0
    PLAYER_POS = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Создание новой пули
                    bullet_x = PLAYER_POS[0] + PLAYER_SIZE // 2 - BULLET_WIDTH // 2
                    bullet_y = PLAYER_POS[1]
                    bullet = Bullet(bullet_x, bullet_y)
                    bullet_list.append(bullet)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and PLAYER_POS[0] > 0:
            PLAYER_POS[0] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and PLAYER_POS[0] < WIDTH - PLAYER_SIZE:
            PLAYER_POS[0] += PLAYER_SPEED

        screen.fill(BLACK)

        drop_asteroids(asteroid_list)
        score = update_asteroid_positions(asteroid_list, score)

        # Обновление и отрисовка пуль
        for bullet in bullet_list[:]:
            bullet.move()
            if bullet.rect.y < 0:
                bullet_list.remove(bullet)
            else:
                bullet.draw(screen)

        # Проверка столкновений пуль и астероидов
        score = bullet_collision_check(bullet_list, asteroid_list, score)

        draw_asteroids(asteroid_list)

        if collision_check(asteroid_list, PLAYER_POS):
            game_over = True

        screen.blit(player_image, (PLAYER_POS[0], PLAYER_POS[1]))

        # Отображение счета
        font = pygame.font.SysFont("monospace", 35)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        clock.tick(30)
        pygame.display.update()

    # Показать итоговый счет после завершения игры
    show_game_over()

# Экран завершения игры
def show_game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()

        screen.fill(BLACK)

        font = pygame.font.SysFont("monospace", 70)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

        font = pygame.font.SysFont("monospace", 50)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))

        font_small = pygame.font.SysFont("monospace", 30)
        restart_text = font_small.render("Press 'R' to Restart or 'ESC' to Quit", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_loop()
        if keys[pygame.K_ESCAPE]:
            quit_game()

# Запуск игры
game_menu()
pygame.quit()
