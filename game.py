import pygame as sc
import time
import random
from states import States
from game_map import Map 

class Game:
    def __init__(self):
        sc.mixer.pre_init(44100, 16, 2, 4096)
        sc.init()
        self.font=sc.font.SysFont(None,28)
        self.text=self.font.render("Score:",True,(0,0,0))
        States.__init__(self)
        self.next='Introduction'    
        self.score=0;        
        #creating map
        self.map=Map()
        self.historyX=[]
        self.historyY=[]
        self.TailSize=0
        self.x=1
        self.y=1 
        self.up=False
        self.down=False
        self.left=False
        self.right=True
       #fruit logic
        self.fruit=sc.image.load('fruit.png')
        self.fruit=sc.transform.scale(self.fruit,(20,20))
        self.fruitX=random.randint(1,22)
        self.fruitY=random.randint(1,29)
        self.count=0
        #adding sound
        self.sound=sc.mixer.Sound("apple1.wav")

    def get_event(self,event):
        if event.type==sc.KEYDOWN:
            if event.key==sc.K_UP:
                self.up=True
                self.down=False
                self.left=False
                self.right=False
            elif event.key==sc.K_DOWN:
                self.up=False
                self.down=True
                self.left=False
                self.right=False
            elif event.key==sc.K_LEFT:
                self.up=False
                self.down=False
                self.left=True
                self.right=False
            elif event.key==sc.K_RIGHT:
                self.up=False
                self.down=False
                self.left=False
                self.right=True
            elif event.key==sc.K_SPACE:
                self.done=True

        return

    def update(self,screen,dt):
        #wall boundaries
        if(self.x>22 or self.y>29 or self.x==0 or self.y==0):
            self.done=True
        #head not touching body
        for i in range(0,self.TailSize):
            print(self.historyX[i]," ",self.x," ",self.historyY[i]," ",self.y)
            if (self.historyX[i]==self.x and self.historyY[i]==self.y):
                self.done=True
        
        self.draw(screen)
    def startup(self):
        return
    def draw(self,screen):
        screen.fill((0,0,0))
        #sc.draw.rect(screen,(128,128,128),sc.Rect(self.x-5,self.y-5,20,20) )  
        #DRAWING MAP
        sumx=0
        sumy=0
        for y in range(0,self.map.get_H()):
            for x in range(0,self.map.get_W()):
                if(self.map.get_Value(x,y)==1): 
                    sc.draw.rect(screen,(128,128,128),sc.Rect(x+sumx,y+sumy,20,20) )
                else:
                    sc.draw.rect(screen,(1,166,17),sc.Rect(x+sumx,y+sumy,20,20))
                if (x==self.fruitX and y==self.fruitY):
                    screen.blit(self.fruit,(x+sumx,y+sumy))
                   # sc.draw.rect(screen,(128,128,128),sc.Rect(x+sumx,y+sumy,20,20) )
                    #print(x+sumx)
                    #print(y+sumy)    
                if (x==self.x and self.y==y):
                   # screen.blit(self.head,(x+sumx,y+sumy))   
                    sc.draw.rect(screen,(255,255,255),sc.Rect(x+sumx,y+sumy,20,20) )
                   # print("head x=",(x+sumx)," y=" ,(y+sumy),"\n")  
                    if (len(self.historyX)>self.TailSize and self.count==10 ):
#                        print("x+sumx=",x+sumx," x=",x," sumx=" ,sumx)
 #                       print("x=(x+sumx)%20",(x+sumx)%20)
  #                      print("y+sumy=",y+sumy," y=",y," sumy=",sumy)        
                        self.historyX.insert(0,x)
                        self.historyY.insert(0,y)
                      #  for z in self.historyX:
                    #        print(z,end=" ")
                     #   print("DONE\n") 
                        self.historyX.pop() 
                        self.historyY.pop() 
                    elif (self.count==10):
                         self.historyX.insert(0,x)
                         self.historyY.insert(0,y)
                
                sumx+=20
            sumx=0
            sumy+=20
        
        for i in range(0,self.TailSize):
            sc.draw.rect(screen,(255,255,255),sc.Rect(self.historyX[i]+20*(self.historyX[i] ),self.historyY[i]+20*(self.historyY[i]),20,20))
             
        if (self.fruitX==self.x and self.fruitY==self.y):
            self.fruitX=random.randint(1,22)
            self.fruitY=random.randint(1,29)
            inbody=True
            count=0;
            print("************************")
            #making sure fruit does not land in body            
            while(inbody and self.TailSize!=0):
                for z1 in  range(0,self.TailSize):
                    #print(self.historyX[z1]," ",self.historyY[z1]%20," ",self.fruitX," ",self.fruitY)
                    if (self.historyX[z1]==self.fruitX and self.historyY[z1]==self.fruitY):
                        self.fruitX=random.randint(1,22)
                        self.fruitY=random.randint(1,29)
                        inbody=True
                        break;
                    inbody=False
            
            #print("****generating new rand int ******")
            #print(self.fruitY)
            #print(self.fruitX)
            self.score+=10
            self.sound.play()
            self.TailSize+=1
        
        
        #screen.blit(self.head,(self.x,self.y))
        #screen.blit(self.body,(self.x1,self.y1))
        if (self.up and self.count==10):
            self.y-=1
            self.count=0
        elif (self.down and self.count==10):
            self.y+=1
            self.count=0
        elif (self.left and self.count==10):
            self.x-=1
            self.count=0
        elif (self.right and self.count==10):
            self.x+=1
            self.count=0
        else:
            self.count+=1         
        #printing score
        sc.draw.rect(screen,(255,255,255),sc.Rect(0,649,503,30 ) )
        screen.blit(self.text,(5,651)  )  
        screen.blit(self.font.render( ((str)(self.score)),True,(0,0,0)),(113,651 ) )   
        return


    def cleanup(self):
        self.historyX.clear()
        self.historyY.clear()
        self.TailSize=0
        self.x=1
        self.y=1 
        self.up=False
        self.down=False
        self.left=False
        self.right=True
        self.fruitX=random.randint(1,22)
        self.fruitY=random.randint(1,29)
        self.count=0
        return
    
    
    
    
    
    
    
    
    
    
    
    
