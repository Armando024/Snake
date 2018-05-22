import numpy as np

class Map:
    def __init__(self):
        self.h=31
        self.w=24
        self.map=np.zeros(shape=(31,24))
        self.map[:,0]=1
        self.map[:,23]=1
        self.map[0,:]=1
        self.map[30,:]=1 
        print(self.map)
        
    def get_H(self):
        return self.h

    def get_W(self):
        return self.w

    def get_Map(self):
        return self.map

    def get_Value(self,x,y):
        return self.map[y][x]

if __name__=='__main__':
    temp=Map()

    print(temp.get_Value(1,1))
   # print(temp)    


