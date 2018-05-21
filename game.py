import pygame as sc
import tensorflow as tf
import time
import random
import math
import pandas as pd
import numpy as np
from pathlib import Path
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
        self.historyX=[12,12]
        self.historyY=[11,10]
        self.TailSize=2
        self.x=12
        self.y=12 
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
        self.player=False
        
        if self.player is False:
            self.model=self.load_model()

    def load_model(self):
        #initlizing model and expected input
        features1=['left','right','up','down','distance']
        features=[]
        for key in features1:
           # print(key)
            features.append(tf.feature_column.numeric_column(key=key))
       # print(features) 
        model=tf.estimator.DNNClassifier(feature_columns=features,model_dir="tensor/snake_nn",hidden_units=[25],n_classes=4)

        return model;
        
    def get_event(self,event):
        if event.type==sc.KEYDOWN and self.player:
            if event.key==sc.K_UP:
                self.up=True
                self.down=False
                self.left=False
                self.right=False
            if event.key==sc.K_DOWN:
                self.up=False
                self.down=True
                self.left=False
                self.right=False
            if event.key==sc.K_LEFT:
                self.up=False
                self.down=False
                self.left=True
                self.right=False
            if event.key==sc.K_RIGHT:
                self.up=False
                self.down=False
                self.left=False
                self.right=True
            if event.key==sc.K_SPACE:
                self.done=True
            if event.key==sc.K_p:
                time.sleep(10)
        return
    def write_data(self):
        data=[]
        #checking left side of snake
        tail_col=self.obs_tail() #checks for tail collision
        if(self.map.get_Value(self.x-1,self.y)==1 or tail_col[0] ):#  self.historyX[1]==self.x-1):
            data.append(1) #1==yes there is a obstacle
        else:
            data.append(0)#0==no there is no obstacle
        #checking right side
        if(self.map.get_Value(self.x+1,self.y)==1 or tail_col[1] ): # self.historyX[1]==self.x+1):
            data.append(1)
        else:
            data.append(0) 
        #checking up
        if(self.map.get_Value(self.x,self.y-1)==1 or tail_col[2] ):  # self.historyY[1]==self.y-1):
            data.append(1)
        else:
            data.append(0)
        #checking down
        if(self.map.get_Value(self.x,self.y+1)==1 or tail_col[3] ):    # self.historyY[1]==self.y+1):
            data.append(1)
        else:
            data.append(0)
        #distance between head and apple
       # data.append(round(math.sqrt( math.pow(self.fruitX-self.x,2)  + math.pow((self.fruitY-self.y),2)),3) )  
        #orientation of apple to head, since using distance did not work so well
        #e.g 
        #       |    a
        #       |  /
        #       |/
        #       O   --head
        #       o   --body
        #       o
        #       o
        #a is apple
        data.append(round(math.atan2(self.fruitY-self.y,self.fruitX-self.x),3) )
        
        #direction pick 0=left 1=right 2=up 3=down
        if self.left:
            data.append(0)
        elif self.right:
            data.append(1)
        elif self.up:
            data.append(2)
        elif self.down:
            data.append(3)
#        print("[left,right,up,down]")
        print("left="+str(data[0])+" right="+str(data[1])+" up="+str(data[2])+" down="+str(data[3])+" orientation="+str(data[4])+" chosen="+str(data[5])) 
        data1=[]
        if self.player:
            data1.append(data)
            file_path=Path("train_data/test0.csv")
            if file_path.exists():
                df=pd.DataFrame(data1,columns=None)
                #print(df)
                df.to_csv('train_data/test0.csv',mode='a' ,index=False,header=False)
            else:
                df=pd.DataFrame(data1,columns=['left','right','up','down','distance','chosen'])
                #print(df)
                df.to_csv('train_data/test0.csv',mode='w' ,index=False)
        ax=[]
        ax.append(data[0])
        a2=[]
        a2.append(data[1])
        a3=[]
        a3.append(data[2])
        a4=[]
        a4.append(data[3])
        a5=[]
        a5.append(data[4])
         
        data2={
            'left':ax,
            'right':a2,
            'up':a3,
            'down':a4,
            'distance':a5,
            }
        return data2 

    
    def obs_tail(self):
        ans=[False,False,False,False]
        for a in range(0,len(self.historyX)):
            if self.x-1==self.historyX[a]and self.y==self.historyY[a]:
                ans[0]=True
            if self.x+1==self.historyX[a] and self.y==self.historyY[a]:
                ans[1]=True
            if self.x==self.historyX[a] and self.y-1==self.historyY[a]:
                ans[2]=True
            if self.x==self.historyX[a] and self.y+1==self.historyY[a]:
                ans[3]=True
        return ans  


    def update(self,screen,dt):
        #wall boundaries
        if(self.x>22 or self.y>29 or self.x==0 or self.y==0):
            self.done=True
        #head not touching body
        for i in range(0,self.TailSize):
           # print(self.historyX[i]," ",self.x," ",self.historyY[i]," ",self.y)
            if (self.historyX[i]==self.x and self.historyY[i]==self.y):
                self.done=True
        
        self.draw(screen)
    def startup(self):
        self.historyX=[12,12]
        self.historyY=[11,10]
        self.TailSize=2
        self.x=12
        self.y=12 
        return
    def eval_input(self,features,labels,batch_size):
        features=dict(features)
        if labels is None:
            inputs=features
        else:
            inputs=(features,labels)

        dataset=tf.data.Dataset.from_tensor_slices(inputs)

        assert batch_size is not None, "wrong, batch must be none"
        dataset=dataset.batch(batch_size)
    
        return dataset
    
    
    def nn_mode(self,inputs):
        predictions=self.model.predict(input_fn=lambda:self.eval_input(inputs,labels=None,batch_size=100))         
        val=-1
        for pred in predictions:
            class_id=pred['class_ids'][0]
            print(class_id)
            val=int(class_id)
            print(pred['probabilities'][class_id])
        if val==2:
            self.up=True
            self.down=False
            self.left=False
            self.right=False
        if val==3:
            self.up=False
            self.down=True
            self.left=False
            self.right=False
        if val==0:
            self.up=False
            self.down=False
            self.left=True
            self.right=False
        if val==1:
                self.up=False
                self.down=False
                self.left=False
                self.right=True
        return 
    
    def draw(self,screen):
        screen.fill((0,0,0))
        #sc.draw.rect(screen,(128,128,128),sc.Rect(self.x-5,self.y-5,20,20) )  
        #DRAWING MAP
        if(self.count==10):
            if self.player:
                self.write_data()
            else:
                self.nn_mode(self.write_data())        
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
#            print("************************")
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
        self.score=0 
        return
    
    
    
    
    
    
    
    
    
    
    
    
