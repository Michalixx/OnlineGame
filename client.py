import pygame as pg

width = 500
height = 500
window = pg.display.set_mode((width, height))
pg.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 0.1

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= self.vel

        if keys[pg.K_RIGHT]:
            self.x += self.vel

        if keys[pg.K_UP]:
            self.y -= self.vel

        if keys[pg.K_DOWN]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win, player):
    window.fill((255,255,255))
    player.draw(win)
    pg.display.update()


def main():
    run = True
    p = Player(50,50,100,100,(0,255,0))

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

        p.move()
        redrawWindow(window, p)

main()