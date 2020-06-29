import pygame
from network import Network
from player import Player
from data import Data

N = Network()
N.send("spec")

wwidth = 600
wheight = 800
window = pygame.display.set_mode((wwidth,wheight))
pygame.display.set_caption("Spectator")

clientNumber = N.id

class Wall():
    def __init__(self,win,x,y,width,height,color):
        x = x - (width/2)
        y = y - (height/2)
        pygame.draw.rect(win, color, (x,y,width,height))



def redrawWindow(win,data):
    pSize = 10
    win.fill((0,0,0))
    players = []
    for Data in data:
        if Data:
            p = Player(Data.x - 5,Data.y - 5,pSize,Data.color)
            players.append(p)
    for X in players:
        X.draw(win)        
    Wall(win,300,400,100,100,(255,255,255))
    Wall(win,125,25,250,100,(255,255,255))
    Wall(win,475,25,250,100,(255,255,255))
    Wall(win,125,775,250,100,(255,255,255))
    Wall(win,475,775,250,100,(255,255,255))
    Wall(win,525,450,250,50,(255,255,255))
    Wall(win,75,350,250,50,(255,255,255))
    Wall(win,10,450,50,50,(255,255,255))
    Wall(win,590,350,50,50,(255,255,255))
    Wall(win,300,150,50,50,(255,255,255))
    Wall(win,150,200,50,50,(255,255,255))
    Wall(win,450,200,50,50,(255,255,255))
    Wall(win,0,250,50,50,(255,255,255))
    Wall(win,600,250,50,50,(255,255,255))
    Wall(win,300,558,200,50,(255,255,255))
    Wall(win,50,667,200,50,(255,255,255))
    pygame.display.update()

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        redrawWindow(window, N.send("1"))

main()
