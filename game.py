import pygame as sc
import time
import random
from states import States
from game_map import Map 

class Game:
    def __init__(self):
        sc.init()
        States.__init__(self)
        self.next='Introduction'    
        #creating head images
        self.head=sc.image.load('head.png')
        self.head=sc.transform.scale(self.head,(20,20))
        self.head0=sc.transform.rotate(self.head,0)
        self.head1=sc.transform.rotate(self.head,270)
        self.head2=sc.transform.rotate(self.head,90)
        self.head3=sc.transform.rotate(self.head,180)
        #creating body images
        self.body=sc.image.load('body.png')
        self.body=sc.transform.scale(self.body,(20,20))
        self.body0=sc.transform.rotate(self.body,0) 
        self.body1=sc.transform.rotate(self.body,90)
        self.body2=sc.transform.rotate(self.body,180)
        self.body3=sc.transform.rotate(self.body,270)        
        #creating map
        self.map=Map()
        self.historyX=[]
        self.historyY=[]
        #self.historyX.append(25)
        #self.historyY.append(25)
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

        if(self.up):
            self.head=self.head0
        elif(self.down):
            self.head=self.head3
        elif(self.left):
            self.head=self.head2
        elif(self.right):
            self.head=self.head1 # sc.transform.rotate(self.head,90)
        
        self.draw(screen)
    def startup(self):
        return
    def draw(self,screen):
        screen.fill((0,0,0))
        #sc.draw.rect(screen,(128,128,128),sc.Rect(self.x-5,self.y-5,20,20) )  
        #DRAWING MAP
        #time.sleep(0.2)
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
                    #print(x+sumx)
                    #print(y+sumy)    
                if (x==self.x and self.y==y):
                    screen.blit(self.head,(x+sumx,y+sumy))     
                    if (len(self.historyX)>self.TailSize and self.count==10 ):
                        self.historyX.insert(0,(x+sumx))
                        self.historyY.insert(0,(y+sumy))
                        for z in self.historyX:
                            print(z,end=" ")
                        print("DONE\n") 
                        self.historyX.pop() 
                        self.historyY.pop() 
                    elif (self.count==10):
                         self.historyX.insert(0,x+sumx)
                         self.historyY.insert(0,y+sumy)
 
                sumx+=20
            sumx=0
            sumy+=20
        
        for i in range(0 ,self.TailSize):
            sc.draw.rect(screen,(128,128,128),sc.Rect(self.historyX[i],self.historyY[i],20,20) )        
             
        if (self.fruitX==self.x and self.fruitY==self.y):
            self.fruitX=random.randint(1,22)
            self.fruitY=random.randint(1,29)
            #print("****generating new rand int ******")
            #print(self.fruitY)
            #print(self.fruitX)
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
        
        return


    def cleanup(self):
        return
    
    
    
    
    
    
    
    
    
    
    
    
