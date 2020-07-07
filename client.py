import pygame
from network import Network
from player import Player
from data import Data

N = Network()

WHITE = (255,255,255)

wwidth = 800
wheight = 600
window = pygame.display.set_mode((wwidth,wheight))
pygame.display.set_caption("Player")

clientNumber = N.id            

def redrawWindow(win,plist,me):
    win.fill((0,0,0))
    me.draw(win)
    me.shoot(win)
    for X in plist:
        if X.color != plist[0].color:
            dx = ((plist[0].x - X.x) * -2.4) + wwidth/2
            dy = ((plist[0].y - X.y) * -2.4) + wheight/2
            pl = Player(dx,dy,24,X.color)
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
        D.shooing = pygame.key.get_pressed()[pygame.K_SPACE]
        redrawWindow(window,N.send(D),p)
        
        
        
        
main()