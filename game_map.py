class Map:
    def __init__(self):
        self.h=31
        self.w=24
        self.map=[]
        temp=[]
        for b in range(0,self.h):
            temp=[]
            for a in range(0,self.w):
                temp.append(0)     
            self.map.append(temp)
        for a in range(0,self.w):
            for b in range(0,self.h): 
                if(a==0 or a==(self.w-1)): 
                    self.map[b][a]=1
                if(b==0 or b==(self.h-1) ):
                    self.map[b][a]=1
        

    def __str__(self):
        temp=""
        for a in self.map:
            temp+=((str)(a))+"\n"
        return temp

    def get_H(self):
        return self.h

    def get_W(self):
        return self.w

    def get_Map(self):
        return self.map

    def get_Value(self,x,y):
        return self.map[y][x]

#if __name__=='__main__':

 #   temp=Map()
  #  print(temp)    


