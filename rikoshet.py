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