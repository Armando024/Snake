import pygame as sc
from gui.states import States

class Intro:
    def __init__(self):
        sc.init()
        States.__init__(self)
        self.font=sc.font.SysFont(None,30)
        self.txta=self.font.render("Welcome to the Snake Game",True,(255,255,255))        
        self.txtb=self.font.render("Re-constructed in pygame",True,(255,255,255))
        self.txtc=self.font.render("by Armando Aguirre",True,(255,255,255))

        
        self.txtd=self.font.render("Pressed the space bar to start",True,(255,255,255))
        self.txte=self.font.render("Used the arrow keys to move",True,(255,255,255))
        self.next='Game'    
    def get_event(self,event):
        if event.type==sc.KEYDOWN:
            if event.key==sc.K_SPACE:
                self.done=True #To move to the game
        return

    def update(self,screen,dt):
        self.draw(screen)
        return

    def draw(self,screen):
        screen.fill((1,166,17))
        sc.draw.rect(screen,(0,123,12),sc.Rect(0,0,50,679))
        sc.draw.rect(screen,(0,123,12),sc.Rect(0,0,503,50))    
        sc.draw.rect(screen,(0,123,12),sc.Rect(453,0,50,679)) 
        sc.draw.rect(screen,(0,123,12),sc.Rect(0,629,679,50))

        screen.blit(self.txta,(110,200))
        screen.blit(self.txtb,(110,240))
        screen.blit(self.txtc,(110,280))
        screen.blit(self.txtd,(110,320))
        screen.blit(self.txte,(110,360))
        return


    def startup(self):
        return
    def cleanup(self):
        return
    
    
    
    
    
    
    
    
    
    
    
    
