import pygame
from network import Network
from player import Player
from data import Data

N = Network()

wwidth = 800
wheight = 600
window = pygame.display.set_mode((wwidth,wheight))
pygame.display.set_caption("Player")

clientNumber = N.id            

def redrawWindow(win,plist):
    win.fill((0,0,0))
    for X in plist:
        dx = ((plist[0].x - X.x) * -2.5) + wwidth/2
        dy = ((plist[0].y - X.y) * -2.5) + wheight/2
        pl = Player(dx,dy,25,X.color)
        pl.draw(win)
    pygame.display.update()
    


def main():
    p = Player(wwidth/2,wheight/2,25,N.id.color)
    run = True
    D = Data(p.x,p.y,p.color)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        D.x = p.dx 
        D.y = p.dy
        redrawWindow(window,N.send(D))
        
        
        
main()