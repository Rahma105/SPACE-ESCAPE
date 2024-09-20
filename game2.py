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

# Игровые параметры
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

asteroid_size = 50
asteroid_speed = 7

score = 0
game_over = False

clock = pygame.time.Clock()

# Загрузка изображений (замени на свои изображения)
player_image = pygame.image.load('image/Без названия (3).jpeg')
asteroid_image = pygame.image.load('image/Без названия (2).jpeg')
player_image = pygame.transform.scale(player_image, (player_size, player_size))
asteroid_image = pygame.transform.scale(asteroid_image, (asteroid_size, asteroid_size))

# Функция для создания астероида
def drop_asteroids(asteroid_list):
    delay = random.random()
    if len(asteroid_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - asteroid_size)
        asteroid_list.append([x_pos, 0])

# Функция для отрисовки астероидов
def draw_asteroids(asteroid_list):
    for asteroid_pos in asteroid_list:
        screen.blit(asteroid_image, (asteroid_pos[0], asteroid_pos[1]))

# Функция для обновления позиции астероидов
def update_asteroid_positions(asteroid_list, score):
    for idx, asteroid_pos in enumerate(asteroid_list):
        if asteroid_pos[1] >= 0 and asteroid_pos[1] < HEIGHT:
            asteroid_pos[1] += asteroid_speed
        else:
            asteroid_list.pop(idx)
            score += 1
    return score

# Функция для проверки столкновения
def collision_check(asteroid_list, player_pos):
    for asteroid_pos in asteroid_list:
        if detect_collision(asteroid_pos, player_pos):
            return True
    return False

# Функция для детекции столкновения
def detect_collision(player_pos, asteroid_pos):
    p_x, p_y = player_pos
    a_x, a_y = asteroid_pos

    if (a_x >= p_x and a_x < (p_x + player_size)) or (p_x >= a_x and p_x < (a_x + asteroid_size)):
        if (a_y >= p_y and a_y < (p_y + player_size)) or (p_y >= a_y and p_y < (a_y + asteroid_size)):
            return True
    return False

# Меню игры
def game_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        font = pygame.font.SysFont("monospace", 50)
        title = font.render("SPACE ESCAPE", True, WHITE)
        start_button = font.render("Start", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_button, (WIDTH // 2 - exit_button.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Нажатие 's' для старта
                    menu = False
                if event.key == pygame.K_e:  # Нажатие 'e' для выхода
                    pygame.quit()
                    sys.exit()

# Основной игровой цикл
def game_loop():
    asteroid_list = []
    global score, game_over, player_pos

    game_over = False
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed

        screen.fill(BLACK)

        drop_asteroids(asteroid_list)
        score = update_asteroid_positions(asteroid_list, score)
        draw_asteroids(asteroid_list)

        if collision_check(asteroid_list, player_pos):
            game_over = True

        screen.blit(player_image, (player_pos[0], player_pos[1]))

        font = pygame.font.SysFont("monospace", 35)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        clock.tick(30)
        pygame.display.update()

    # Показать итоговый счет после завершения игры
    font = pygame.font.SysFont("monospace", 50)
    game_over_text = font.render("Game Over", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)

    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()
    pygame.time.wait(3000)

# Запуск игры
game_menu()
game_loop()
pygame.quit()
