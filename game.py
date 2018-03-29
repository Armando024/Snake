import pygame as sc
from states import States

class Game:
    def __init__(self):
        sc.init()
        States.__init__(self)
        self.next='Introduction'
    
    def get_event(self,event):
        if event.type==sc.KEYDOWN:
            if event.key==sc.K_SPACE:
                self.done=True
        return

    def update(self,screen,dt):
        
        self.draw(screen)
    def startup(self):
        return
    def draw(self,screen):
        screen.fill((1,166,17))
        sc.draw.rect(screen,(128,128,128),sc.Rect(250,400,15,15) )  
        return


    def cleanup(self):
        return
    
    
    
    
    
    
    
    
    
    
    
    
