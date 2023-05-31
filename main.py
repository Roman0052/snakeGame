import pygame
import random
import math

# Ініціалізація Pygame
pygame.init()

# Розміри вікна гри
WIDTH = 640
HEIGHT = 360

# Кольори
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Розміри блоку змійки та їжі
BLOCK_SIZE = 20

# Завантаження зображень
head_img = pygame.image.load("head.png")
body_img = pygame.image.load("body.jpg")
food_img = pygame.image.load("food.png")
background_img = pygame.image.load("background.jpg")

# Зміна розмірів зображень
head_img = pygame.transform.scale(head_img, (BLOCK_SIZE, BLOCK_SIZE))
body_img = pygame.transform.scale(body_img, (BLOCK_SIZE, BLOCK_SIZE))
food_img = pygame.transform.scale(food_img, (BLOCK_SIZE, BLOCK_SIZE))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Створення вікна гри
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змійка")

clock = pygame.time.Clock()

# Функція для відображення повідомлення на екрані
def message(msg, color, y_displacement=0):
    font_style = pygame.font.SysFont(None, 30)
    rendered_msg = font_style.render(msg, True, color)
    text_rect = rendered_msg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_displacement))
    window.blit(rendered_msg, text_rect)

# Основна функція гри
def game_loop():
    game_over = False
    game_close = False

    # Початкові координати та швидкість змійки
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0

    # Створення початкової довжини змійки
    snake_length = 1
    snake_segments = []

    # Генерація випадкової позиції їжі
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Рахунок та рекорд
    score = 0
    record_score = 0

    # Початкова швидкість змійки
    snake_speed = 10
    # Швидкість збільшується кожних 5 з'їдених яблук
    speed_increment = 3

    while not game_over:

        while game_close:
            window.blit(background_img, (0, 0))
            message("Гра закінчена! Натисніть Q-Вихід або C-Нова гра", RED, -50)
            message("Рахунок: " + str(score), WHITE, 50)
            message("Рекорд: " + str(record_score), WHITE, 100)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Перевірка виходу за межі вікна
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # Оновлення координат змійки
        x += x_change
        y += y_change

        # Відображення заднього фону
        window.blit(background_img, (0, 0))

        # Відображення їжі
        window.blit(food_img, (food_x, food_y))

        # Створення голови змійки
        snake_head = [x, y]
        snake_segments.append(snake_head)

        # Видалення зайвих сегментів змійки, якщо її довжина перевищує snake_length
        if len(snake_segments) > snake_length:
            del snake_segments[0]

        # Перевірка на зіткнення з самою собою
        for segment in snake_segments[:-1]:
            if segment == snake_head:
                game_close = True

        # Відображення змійки
        for segment in snake_segments:
            angle = math.degrees(math.atan2(y_change, x_change))
            rotated_body = pygame.transform.rotate(body_img, -angle)
            window.blit(rotated_body, (segment[0], segment[1]))

        window.blit(head_img, (x, y))

        # Відображення рахунку та рекорду
        font_style = pygame.font.SysFont(None, 25)
        score_text = font_style.render("Рахунок: " + str(score), True, WHITE)
        record_text = font_style.render("Рекорд: " + str(record_score), True, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(record_text, (10, 35))

        # Оновлення екрану
        pygame.display.update()

        # Перевірка з'їдання їжі
        if x == food_x and y == food_y:
            # Генерація нової позиції їжі
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            # Збільшення довжини змійки
            snake_length += 1
            # Збільшення рахунку
            score += 1
            # Перевірка, чи треба збільшити швидкість
            if score % speed_increment == 0:
                snake_speed += 2

        # Оновлення рекорду
        if score > record_score:
            record_score = score

        # Обмеження FPS (швидкості оновлення екрану)
        clock.tick(snake_speed)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    game_loop()
    pygame.quit()
