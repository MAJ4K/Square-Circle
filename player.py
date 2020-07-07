import pygame

def clamp(min,max,value):
    if value > max:
        value = max
    elif value < min:
        value = min
    return value

class Player():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.size = size
        self.color = color
        self.rect = (x,y,size,size)
        self.vel = 2
        self.charging = False
        self.bullets = []
        self.dir = (0,0)
    
    def draw(self, win):
        pygame.draw.rect(win, self.color,self.rect)
    
    def move(self):
        self.dir = (0,0)
        keys = pygame.key.get_pressed()
        self.dx, self.dy = 0,0
        if keys[pygame.K_w]:
            self.dir = (0,1)
            self.dy = -self.vel
        if keys[pygame.K_s]:
            self.dir = (0,-1)
            self.dy = self.vel
        if keys[pygame.K_a]:
            self.dir = (-1,0)
            self.dx = -self.vel
        if keys[pygame.K_d]:
            self.dir = (1,0)
            self.dx = self.vel

        self.rect = (self.x,self.y,self.size,self.size)
    
    def shoot(self,window):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if not self.charging:
                self.bullets.append(Bullet(self.x,self.y,self.size,self.dir))
            self.charging = True
        else:
            if self.charging:
                self.bullets.remove(self.bullets[-1])
            self.charging = False
        
        for X in self.bullets:
            if X:
                X.draw(window)
            """ if abs(X.getx()) > 800 or abs(X.gety()) > 800:
                self.bullets.remove(X)
            if X.isshot():
                X.addpos(self.dx,self.dy) """

        if self.charging:
            self.bullets[-1].grow()
            pass


class Bullet():
    def __init__(self, x, y, size, dir):
        self.x = int(x + size/2)
        self.y = int(y + size/2)
        self.size = 4
        self.maxSize = int(size/2)
        self.dir = dir
        self.shot = False

    def draw(self,win):
        if self.shot:
            self.x += self.dir[0]
            self.y += self.dir[1]
        pygame.draw.circle(win, (255,255,255), (self.x,self.y), int(self.size))
        
    def grow(self):
        self.size += .1
        self.size = clamp(0,self.maxSize,self.size)

    def shoot(self):
        self.shot = True
    
    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def isshot(self):
        return self.shot

    def addpos(self,x,y):
        self.x -= x
        self.y -= y
              