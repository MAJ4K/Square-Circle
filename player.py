import pygame

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
    
    def draw(self, win):
        pygame.draw.rect(win, self.color,self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()
        self.dx, self.dy = 0,3
        if keys[pygame.K_w]:
            self.dy = -self.vel
        if keys[pygame.K_s]:
            self.dy = self.vel
        if keys[pygame.K_a]:
            self.dx = -self.vel
        if keys[pygame.K_d]:
            self.dx = self.vel

        self.rect = (self.x,self.y,self.size,self.size)
    
    """ def shoot(self,window):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.draw.elipse(window,(255,255,255),(self.x,self.y),self.size) """