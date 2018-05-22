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
        self.map=Map() #I like having the back end to be 0 and 1 for the GUI as it will make it easier to analyse the data
        self.historyX=[12,12] 
        self.historyY=[11,10] 
        self.TailSize=2
        self.x=12
        self.y=12 
        self.direction=0 #0=left 1=right 2=up 3=down
        self.speed=5 #speed of game 5 for AI is good and for player 10 is good  
        self.fruit=sc.image.load('fruit.png')
        self.fruit=sc.transform.scale(self.fruit,(20,20))
        self.fruitX=random.randint(1,22)
        self.fruitY=random.randint(1,29)
        self.count=0
        #adding sound
        self.sound=sc.mixer.Sound("apple1.wav")
        #chooses between the sound and bot mode
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
                self.direction=2
            if event.key==sc.K_DOWN:
                self.direction=3
            if event.key==sc.K_LEFT:
                self.direction=0
            if event.key==sc.K_RIGHT:
                self.direction=1
            if event.key==sc.K_SPACE:
                self.done=True
            if event.key==sc.K_p:#for debugging purposes
                time.sleep(10)
        return
    def write_data(self): #this is basically the eyes of the snake and how it will view it's surrondings 
        data=[]
        #checking left side of snake 
        tail_col=self.obs_tail() #checks for tail collision and returns if it found any, very efficient 
        if(self.map.get_Value(self.x-1,self.y)==1 or tail_col[0] ):
            data.append(1) #1==yes there is a obstacle
        else:
            data.append(0)#0==no there is no obstacle
        #checking right side
        if(self.map.get_Value(self.x+1,self.y)==1 or tail_col[1] ):
            data.append(1)
        else:
            data.append(0) 
        #checking up
        if(self.map.get_Value(self.x,self.y-1)==1 or tail_col[2] ): 
            data.append(1)
        else:
            data.append(0)
        #checking down
        if(self.map.get_Value(self.x,self.y+1)==1 or tail_col[3] ):
            data.append(1)
        else:
            data.append(0)
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
        
        #direction being added 0=left 1=right 2=up 3=down
        data.append(self.direction)
#        print("[left,right,up,down]")
        print("left="+str(data[0])+" right="+str(data[1])+" up="+str(data[2])+" down="+str(data[3])+" orientation="+str(data[4])+" chosen="+str(data[5])) 
      
        if self.player:
            data1=[] #to train the snake nn
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
      
        else:
            data2={
            'left':[data[0]],
            'right':[data[1]] ,
            'up':[data[2]] ,
            'down':[data[3]],
            'distance':[data[4]],
                }
            return data2 
        return 0

    
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
            print("death bcs of wall boundary")
            self.done=True
        #head not touching body
        for i in range(1,len(self.historyX)):

           # print(self.historyX[i]," ",self.x," ",self.historyY[i]," ",self.y)
            if (self.historyX[i]==self.x and self.historyY[i]==self.y):
                print("death bcs it touch body")
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
        self.direction=val
        return 
    def not_in_snake(self):
        if (self.fruitX==self.x and self.fruitY==self.y):
            self.fruitX=random.randint(1,22)
            self.fruitY=random.randint(1,29)
            inbody=True
            print("************************")
            #making sure fruit does not land in body            
            while(inbody and self.TailSize!=0):
               # for z1 in  range(0,self.TailSize):
                    #print(self.historyX[z1]," ",self.historyY[z1]%20," ",self.fruitX," ",self.fruitY)
                    if (self.fruitX  in  self.historyX and self.fruitY in self.historyY):
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
        
        return

 
    def draw(self,screen):
        screen.fill((0,0,0))
        #sc.draw.rect(screen,(128,128,128),sc.Rect(self.x-5,self.y-5,20,20) )  
        #DRAWING MAP
        if(self.count==self.speed):
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
                if (x==self.x and self.y==y):
                    sc.draw.rect(screen,(255,255,255),sc.Rect(x+sumx,y+sumy,20,20) )
                    if (len(self.historyX)>self.TailSize and self.count==self.speed ):
                        self.historyX.insert(0,x)
                        self.historyY.insert(0,y)
                        
                        self.historyX.pop() 
                        self.historyY.pop() 
                    elif (self.count==self.speed):
                         self.historyX.insert(0,x)
                         self.historyY.insert(0,y)
                
                sumx+=20
            sumx=0
            sumy+=20
        
        for i in range(0,self.TailSize):
            sc.draw.rect(screen,(255,255,255),sc.Rect(self.historyX[i]+20*(self.historyX[i] ),self.historyY[i]+20*(self.historyY[i]),20,20))
             
        
        self.not_in_snake() 

        if (self.direction==2 and self.count==self.speed):
            self.y-=1
            self.count=0
        elif (self.direction==3 and self.count==self.speed):
            self.y+=1
            self.count=0
        elif (self.direction==0 and self.count==self.speed):
            self.x-=1
            self.count=0
        elif (self.direction==1 and self.count==self.speed):
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
        self.direction=1
        self.fruitX=random.randint(1,22)
        self.fruitY=random.randint(1,29)
        self.count=0
        self.score=0 
        return
    
    
    
    
    
    
    
    
    
    
    
    
