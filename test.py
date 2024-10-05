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
enemy_radius = 50
enemies = [(440, 430)]

# Перешкоди (список прямокутників: (x, y, ширина, висота))
obstacles = [(341, 179, 20, 420)]

# Функція для малювання гравця
def draw_player(pos, angle):

    screen.blit(pygame.transform.scale(pygame.image.load("Без_імені-removebg-preview.png"),(50,100)),pos)
    gun_length = 40
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - pos[0], mouse_y - pos[1]
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    
    
    screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ryka-removebg-preview.png"),(50,20)),int(angle)),(70,480))

# Функція для малювання патронів
def draw_bullet(pos):
    pygame.draw.circle(screen, BLACK, pos, bullet_radius)

# Функція для малювання ворогів
def draw_enemy(pos):
    screen.blit(pygame.transform.scale(pygame.image.load("depositphotos_654170370-stock-illustration-western-cowboy-bandit-gangster-standing-removebg-preview.png"),(200,200)),pos)

# Функція для малювання перешкод
def draw_obstacle(rect):
    screen.blit(pygame.transform.scale(pygame.image.load("stina.png"),(40,430)),rect)

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
finsh = "none"
back=pygame.transform.scale(pygame.image.load("2304.w026.n002.3516B.p1.3516.jpg"),(800,600))
running = True
while running:
    screen.blit(back,(0,0))


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
        finsh="loss"
        running=False
        

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
                finsh = "win"
                running = False
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
while finsh != "none":
    screen.blit(back,(0,0))
    if finsh=="win":

        screen.blit(pygame.font.SysFont("Arial", 70).render("Ви виграли!", True, (255, 0, 0)), (200, 210))
    else:
        screen.blit(pygame.font.SysFont("Arial", 70).render("Ви програли((!", True, (255, 0, 0)), (200, 210))
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finsh = "none"
pygame.quit()
