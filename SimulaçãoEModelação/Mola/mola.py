import numpy as np
import matplotlib.pyplot as plt



class Body:
    def __init__(self, mass, k,xEq, x0, v0, size):
        self.mass = mass #  body mass
        self.k = k  #   spring constant
        self.xEq=xEq
        self.x = x0 #   instant pos
        self.v = v0 #   instant velocity
        
        self.xList = np.zeros(size)
        self.xList[0]=x0
        
        self.vList = np.zeros(size)
        self.vList[0]=v0
   
        
def initialize(Tmax,dt,tSample):
    size= int(Tmax/tSample)+1
    nStep=int(Tmax/dt)
    saveSteps= int (tSample/dt)
    
    springArray=np.zeros(2,dtype=object)
    springArray[0]=Body(7,7,7,0,0,0)
    springArray[1]=Body(1,1,0.5,1,0,size)
    springArray[2]=Body(1,1,0.5,2,0,size)
    
    
    springCalc(molinha,size,dt)
    
    return molinha


def springCalc(springArray,saveSteps,dt):
    n=springArray.size
    for i in range(n):
        j=i+1
        if j != n-1:
            a=-springArray[j].k*(springArray[j].x-(springArray[j-1].x+springArray[j].xEq))+
            
    
    
# =============================================================================
#     for i in range (saveSteps):
#         a=-springs.k * (springs.x-springs.xEq)
#         springs.v += a*dt
#         springs.x += springs.v*dt
#         springs.xList[i]=springs.x
#         
# =============================================================================



a=initialize(1000,0.01,0.1)
plt.plot(a.xList)