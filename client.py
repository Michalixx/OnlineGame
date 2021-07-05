import pygame as pg
from network import Network
from player import Player

width = 700
height = 700
window = pg.display.set_mode((width, height))
pg.display.set_caption("Client")
pg.init()

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x+self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False



def redrawWindow(win, game, p):
    window.fill((255,255,255))

    if not(game.connected()):
        font = pg.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player...", 1, (255, 0, 0), True)
        win.blit(text, (width/2-text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pg.font.SysFont("comicsans", 60)
        text = font.render("Your move", 1, (0, 255, 255))
        win.blit(text, (80,200))
        text = font.render("Opponent move", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 0:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p1Went:
                text2 = font.render("Locked In", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

            if p == 1:
                win.blit(text2, (100,350))
                win.blit(text1, (400,350))
            else:
                win.blit(text1, (100, 350))
                win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

        pg.display.update()





btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (0, 255, 0)), Button("Paper", 450, 500, (255, 0, 0))]

def main():
    run = True
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(window, game, player)
            pg.time.delay(500)
            try:
                game.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pg.font.SysFont("comicsans", 90)
            if(game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie game!", 1, (255, 0, 0))
            else:
                text = font.render("You lost!", 1, (255, 0, 0))


            window.blit(text, (width/2-text.get_width()/2, height/2 - text.get_height()/2))
            pg.display.update()
            pg.time.delay(2000)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        redrawWindow(window, game, player)







main()