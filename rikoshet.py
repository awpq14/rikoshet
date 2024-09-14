from pygame import*
class GameSprite (sprite.Sprite):
    def __init__(self, picture, x, y, w, h):
        super().__init__()
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
finish = False
window = display.set_mode((700, 500))
display.set_caption("labirunt")
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT: run = False
        elif e.type == MOUSEBUTTONDOWN:
            print(e.pos)
    display.update()
import pygame
import sys

size = width, height = 800, 600
black = 0, 0, 0


def main():

    pygame.init()
    screen = pygame.display.set_mode(size)
    ball_image = pygame.image.load("Без імені.png")
    ball_rect = ball_image.get_rect()
    ball_rect.x = 101
    ball_rect.y = 101
    game_over = False
    dx = 2
    dy = 2
    platform_x = 325
    platform_y = 500
    move_right = False
    move_left = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        screen.fill(black)
        pygame.draw.rect(screen, (255, 255, 255), (platform_x, platform_y, 150, 20))
        screen.blit(ball_image, ball_rect)
        ball_rect.x += dx
        ball_rect.y += dy
        #ball_rectan_x = ball_rect.x
        #ball_rectan_y = ball_rect.y
        #ball_rectan_x = ball_rectan_x + 150
        #ball_rectan_y= ball_rectan_y + 150
        if ball_rect.y < 0 or ball_rect.y > 500 and ball_rect.x > platform_x and ball_rect.x < platform_x + 150:
            dy *= -1
        if ball_rect.x < 0 or ball_rect.y > 500 and ball_rect.x > platform_x and ball_rect.x < platform_x + 150:
            dx *= -1
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == 'w':
                move_right = True
        elif event.type == pygame.KEYUP:
            if chr(event.key) == 'w':
                move_right = False
        if move_right:
            platform_x += 1
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == 's':
                move_left = True
        elif event.type == pygame.KEYUP:
            if chr(event.key) == 's':
                move_left = False
        if move_left:
            platform_x -= 1
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()