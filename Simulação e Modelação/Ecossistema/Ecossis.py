import numpy as np
import matplotlib.pyplot as plt
import random
"""
*______________________________________________________________________________
|  Method [Ecossitema GG]
|
|  Purpose:  [Explain what this method does to support the correct
|      operation of its class, and how it does it.]
|
|  Pre-condition:  [Any non-obvious conditions that must exist
|      or be true before we can expect this method to function
|      correctly.]
|
|  Post-condition: [What we can expect to exist or be true after
|      this method has executed under the pre-condition(s).]
|
|  Parameters:
|      parameter_name -- [Explanation of the purpose of this
|          parameter to the method.  Write one explanation for each
|          formal parameter of this method.]
|
|  Returns:  [If this method sends back a value via the return
|      mechanism, describe the purpose of that value here, otherwise
|      state 'None.']
*______________________________________________________________________________
"""

class Bicho:
    def  __init__(self,sType,size):
        self.type=sType #Tipos possíveis:Empty(0), Planta(1), Herbívoro(2), Carnívoro(3)
        self.size=size  #Tipos possíveis: Fraco(0), Médio(1),Forte(3)
    def __str__(self):
        return 'Hallo'
    def changeTipo(self,newType):
        self.type=newType
        self.size=0
    def grow(self):
        if self.size<=2:
            self.size+=1
    def shrink(self):
        if self.size>=1:
            self.size-=1
        else:
            self.type=0
        
        
        
def initGrid(nx,ny):
    grid=np.zeros((nx,ny),dtype=object)
    herbPos=[]
    carnPos=[]
    plantPos=[]
    p1=9
    p2=3
    p3=1
    for i in range(nx):
        for j in range(ny):
            rd= np.random.rand()
            size=np.random.randint(2)
            if rd<=p1/(p1+p2+p3):
                grid[i][j]=Bicho(1,size)
                herbPos.append([i,j])
            elif rd<(p1+p2)/(p1+p2+p3):
                grid[i][j]=Bicho(2,size)
                carnPos.append([i,j])
            else:
                grid[i][j]=Bicho(3,size)
                plantPos.append([i,j])
    random.shuffle(herbPos)
    random.shuffle(carnPos)
    random.shuffle(plantPos)
    return grid,herbPos,carnPos,plantPos



def look4food(grid,i,j):
    rdPos=np.random.randint(4)
    if rdPos==0:
        if grid[i-1][j].type==(grid[i][j].type-1):
            return [i,j]
    elif rdPos==1:
        if grid[i][j-1].type==(grid[i][j].type-1):
            return [i,j]
    elif rdPos==2:
        if i+1==grid.shape[0]:
            if grid[0][j].type==(grid[i][j].type-1):
                return [0,j]
        else:
            if grid[i+1][j].type==(grid[i][j].type-1):
                return [i+1,j]
    else:
        if j+1==grid.shape[1]:
            if grid[i][0].type==(grid[i][j].type-1):
                return [i,0]
        else:
            if grid[i][j+1].type==(grid[i][j].type-1):
                return [i,j+1]
    return 'nada'
        

        
        
        

    
            
    
#FUNÇAO PRINCIPAL CHAMA-SE CIRCLE OF LIFE
tudo=initGrid(25,25)
grid=tudo[0]
print(look4food(grid,2,2))

        

