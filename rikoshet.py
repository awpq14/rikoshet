from pygame import*
import math
class GameSprite (sprite.Sprite):
    def __init__(self, picture, x, y, w, h):
        super().__init__()
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Player (GameSprite):
    def __init__(self, picture, x, y, w, h):
        super().__init__(picture, x, y, w, h)
        self.start_image=self.image
    def rotate(self):
        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = transform.rotate(self.start_image, int(angle))
class Ball(GameSprite):
    def init(self, player_image, x, y, w, h, speed, x2, y2):
        super().init(player_image, x, y, w, h)
        self.speed = speed
        self.x_speed = ((x2 - self.rect.x) * speed) / (((x2 - self.rect.x)  **2 + (y2 - self.rect.y)  **2)  **0.5)
        self.y_speed = ((y2 - self.rect.y) * speed) / (((x2 - self.rect.x)  **2 + (y2 - self.rect.y)  **2)  **0.5)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if abs(self.rect.right - platform.rect.left) <= self.speed:
                    self.rect.right = platform.rect.left
                    self.x_speed *= -1
                elif abs(self.rect.left - platform.rect.right) <= self.speed:
                    self.rect.left = platform.rect.right
                    self.x_speed *= -1
                elif abs(self.rect.bottom - platform.rect.top) <= self.speed:
                    self.rect.bottom = platform.rect.top
                    self.y_speed *= -1
                elif abs(self.rect.top - platform.rect.bottom) <= self.speed:
                    self.rect.top = platform.rect.bottom
                    self.y_speed *= -1
wall_1 = GameSprite('stina.png', 330, 90, 40, 400)

wall_4 = GameSprite('stina.png', 0, 0, 10, 500)
wall_5 = GameSprite('stina.png', 0, 0, 700, 10)
wall_6 = GameSprite('stina.png', 0, 0, 700, 10)
wall_7 = GameSprite('stina.png', 650, 0, 50, 500)
wall_8 = GameSprite('stina.png', 0, 490, 700, 10)

platforms = sprite.Group(wall_1,  wall_4, wall_5, wall_6, wall_7, wall_8)
hero=Player("ryka-removebg-preview.png", 200 ,300, 50 ,50)

ball = sprite.GroupSingle()

finish = False
window = display.set_mode((700, 500))
display.set_caption("labirunt")
background = transform.scale(image.load('2304.w026.n002.3516B.p1.3516.jpg'), (700, 500))
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT: run = False
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            ball.add(Ball('cyborg.png', hero.rect.centerx, hero.rect.centery, 30, 30, 15, x, y))
            print(e.pos)
    window.blit(background, (0, 0))
    hero.rotate()
    hero.reset()
    platforms.draw(window)
    ball.update()
    ball.draw(window)
    display.update()
    