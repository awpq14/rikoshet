import pygame
import math
import random
bullet_count=0

# Ініціалізація Pygame
pygame.init()

# Налаштування вікна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spy Puzzles")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Персонаж
player_pos = (100, HEIGHT - 100)
player_radius = 20
player_color = BLUE
player_angle = 0

# Патрони
bullet_radius = 5
bullets = []

# Ліміт пострілів
max_shots = 5
shots_fired = 0

# Вороги
enemy_radius = 20
enemies = [(440, 540)]

# Перешкоди (список прямокутників: (x, y, ширина, висота))
obstacles = [(341, 179, 20, 420)]

# Функція для малювання гравця
def draw_player(pos, angle):
    pygame.draw.circle(screen, player_color, pos, player_radius)
    gun_length = 40
    end_pos = (pos[0] + gun_length * math.cos(angle), pos[1] - gun_length * math.sin(angle))
    pygame.draw.line(screen, BLACK, pos, end_pos, 5)

# Функція для малювання патронів
def draw_bullet(pos):
    pygame.draw.circle(screen, BLACK, pos, bullet_radius)

# Функція для малювання ворогів
def draw_enemy(pos):
    screen.blit(pygame.transform.scale(pygame.image.load("ryka-removebg-preview.png"),(40,40)),pos)

# Функція для малювання перешкод
def draw_obstacle(rect):
    pygame.draw.rect(screen, GRAY, rect)

# Перевірка на зіткнення кулі зі стінами (краї вікна)
def bullet_collision_with_walls(bullet):
    bx, by = bullet["pos"]

    # Якщо куля стикається з лівою або правою стіною
    if bx - bullet_radius <= 0 or bx + bullet_radius >= WIDTH:
        bullet["ctuk"]-= 1
        bullet["angle"] = math.pi - bullet["angle"]

    # Якщо куля стикається з верхньою або нижньою стіною
    if by - bullet_radius <= 0 or by + bullet_radius >= HEIGHT:
        bullet["ctuk"]-= 1
        bullet["angle"] = -bullet["angle"]

# Перевірка на зіткнення кулі з перешкодами
def bullet_collision_with_obstacles(bullet):
    for obstacle in obstacles:
        x, y, w, h = obstacle
        bx, by = bullet["pos"]

        # Визначаємо положення кулі відносно перешкоди
        if x - bullet_radius <= bx <= x + w + bullet_radius and y - bullet_radius <= by <= y + h + bullet_radius:
            bullet["ctuk"]-= 1
            # Перевіряємо, з якою стороною перешкоди є зіткнення
            # Відскок по вертикалі
            if y <= by <= y + h:
                if bx < x:  # Зіткнення з лівою стороною перешкоди
                    bullet["angle"] = math.pi - bullet["angle"]
                elif bx > x + w:  # Зіткнення з правою стороною перешкоди
                    bullet["angle"] = math.pi - bullet["angle"]
            # Відскок по горизонталі
            if x <= bx <= x + w:
                if by < y:  # Зіткнення з верхньою стороною перешкоди
                    bullet["angle"] = -bullet["angle"]
                elif by > y + h:  # Зіткнення з нижньою стороною перешкоди
                    bullet["angle"] = -bullet["angle"]

# Основний цикл гри
running = True
while running:
    screen.fill(WHITE)

    # Отримання координат курсора миші
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Обчислення кута для стрільби
    dx, dy = mouse_x - player_pos[0], player_pos[1] - mouse_y
    player_angle = math.atan2(dy, dx)

    # Малюємо гравця, ворогів і перешкоди
    draw_player(player_pos, player_angle)
    for enemy in enemies:
        draw_enemy(enemy)

    for obstacle in obstacles:
        draw_obstacle(obstacle)
    if bullet_count==5:
        running = False

    # Відслідковуємо постріли
    for bullet in bullets:
        if bullet["ctuk"] ==0:
            bullets.remove(bullet)
            bullet_count+=1
        bullet["pos"] = (bullet["pos"][0] + bullet["speed"] * math.cos(bullet["angle"]),
                         bullet["pos"][1] - bullet["speed"] * math.sin(bullet["angle"]))
        draw_bullet(bullet["pos"])

        # Перевірка на зіткнення з ворогом
        for enemy in enemies:
            ex, ey = enemy
            bx, by = bullet["pos"]
            distance = math.hypot(ex - bx, ey - by)
            if distance < enemy_radius + bullet_radius:
                enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)

        # Перевірка на зіткнення зі стінами
        bullet_collision_with_walls(bullet)

        # Перевірка на зіткнення з перешкодами
        bullet_collision_with_obstacles(bullet)

    # Перевірка на події
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Стріляємо при натисканні кнопки миші, якщо ще не вичерпано ліміт пострілів
        if event.type == pygame.MOUSEBUTTONDOWN and shots_fired < max_shots:
            bullets.append({
                "pos": player_pos,
                "angle": player_angle,
                "speed": 9,
                "ctuk": 5
            })
            shots_fired += 1  # Збільшуємо лічильник пострілів
        if event.type == pygame.MOUSEBUTTONDOWN:
            print (event.pos)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
