''' 
    Podem adicionar-se quantos planetas se quiser
    Também dá para adicionar buracos negros (fica interessante)
    Tentei meter a lua a orbitar, mas acaba por se perder da Terra
    O Sol não se encontra fixo (perde-se tempo, mas fica mais correto)
    A Testar: sistema binário
'''



%matplotlib qt
%clear

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
plt.style.use('dark_background')
class Planet:
    def  __init__(self,name, mass, radius,period,size):
        self.name=name
        self.m = mass 
        
        tudo=randVals(radius, period)
        self.coor=tudo[0]
        self.v = tudo[1]
        self.rList=np.zeros((size,2))
        self.rList[0]=self.coor
        self.vList=np.zeros((size,2))
        self.vList[0]=self.v
    def __str__(self):
        return 'Planeta: '+str(self.name) + '       Coordenadas: ' + str(self.coor)

def initialize(size):
    t=np.zeros(size)
    planets=np.zeros(0)
    '''Aqui devem ser inseridos os planetas do sistema Solar'''
    planets=np.append(planets,Planet('Terra', 1/332946, 1,1, size))
    
    planets=np.append(planets,Planet('Júpiter', 1/1047.35, 5.2,11.9, size))
    
    planets=np.append(planets,Planet('Marte', 1/332946*0.107, 1.5,1.9, size))
    
    planets=np.append(planets,Planet('Mercury', 0.055*1/332946, 0.4,88/365, size))
    
    planets=np.append(planets,Planet('Sun', 1, 0,0, size))
    
    planets=np.append(planets,Planet('Venus',0.815*1/332946 , 0.7,225/365, size))
    #planets=np.append(planets,Planet('Black Hole',1, 5,0, size))

    
    
    return planets,t

def randVals(radius,period):
    if period==0 :
        v=0
    else:
        v=2*np.pi*radius/period
    theta=np.random.rand()*2*np.pi
    x=radius*np.cos(theta)
    y=radius*np.sin(theta)
    vx=-v*np.sin(theta)
    vy=v*np.cos(theta)
    pos=np.array([x,y])
    vel=np.array([vx,vy])
    print(pos)
    print(vel)
    return pos,vel
def orbitCalc(deltaT,Tmax,tStep=0.01):
    
    size=int(Tmax/tStep)+1
    print(size)
    nStep=int(tStep/deltaT)
    
    planets,t=initialize(size)
    for i in range(size-1):
        step=0
        while step<nStep:
            for p in range(planets.shape[0]):
                a=aCalc(planets[p],planets,p)
                planets[p].v+=a*deltaT
                planets[p].coor=planets[p].coor+planets[p].v*deltaT
            step+=1
        loadVnC(planets, i)
        t[i+1]+=deltaT*nStep+t[i]
    return planets,t
            
        
    
def aCalc(planet,pArray,p):
    GM=4.*np.pi**2

    a=0
    for i in range(pArray.shape[0]-1):
        r=planet.coor-pArray[p-(i+1)].coor
        rNorm=np.sqrt((r*r).sum())
        a += -GM* pArray[p-(i+1)].m * r / rNorm ** 3
    return a

def loadVnC(pArray,i):
    for p in range(pArray.shape[0]):
        pArray[p].rList[i+1]=pArray[p].coor
        pArray[p].vList[i+1]=pArray[p].v
    

    
fig, ax =plt.subplots()
ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect('equal')

time_template = '%.2f years'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

oT, =ax.plot([],[],'bo', label = 'Earth')
lT, =ax.plot([],[],'b-')

oJ, =ax.plot([],[],'o',color='orange', label = 'Jupiter')
lJ, =ax.plot([],[],'-',color='orange')

oM, =ax.plot([],[],'ro', label = 'Mars')
lM, =ax.plot([],[],'r-')

oMerc, =ax.plot([],[],'o',color='grey',label='Mercury')
lMerc, =ax.plot([],[],'-',color='grey')

oVenus, =ax.plot([],[],'o',color='green',label='Venus')
lVenus, =ax.plot([],[],'-',color='green')

oS, =ax.plot(0,0,'o',color='yellow',label='SOL')



oHole, =ax.plot([],[],'o',color='white',label='Black Hole')



    
Tdatax,Tdatay,Jdatax,Jdatay,Mdatax,Mdatay,Mercdatax,Mercdatay,Venusdatax,Venusdatay=[],[],[],[],[],[],[],[],[],[]
plt.legend()
def make_animation(i):
    if i==0 :
        Tdatax.clear()
        Tdatay.clear()
        Jdatax.clear()
        Jdatay.clear()
        Mdatax.clear()
        Mdatay.clear()
        Mercdatax.clear()
        Mercdatay.clear()
        Venusdatax.clear()
        Venusdatay.clear()

        
        
    Tdatax.append(rt[i,0])
    Tdatay.append(rt[i,1])
    Jdatax.append(rj[i,0])
    Jdatay.append(rj[i,1])
    Mdatax.append(rm[i,0])
    Mdatay.append(rm[i,1])
    Mercdatax.append(rmerc[i,0])
    Mercdatay.append(rmerc[i,1])
    Venusdatax.append(rvenus[i,0])
    Venusdatay.append(rvenus[i,1])
    
    
    
    lT.set_data(Tdatax,Tdatay)
    lJ.set_data(Jdatax,Jdatay)
    lM.set_data(Mdatax,Mdatay)
    lMerc.set_data(Mercdatax,Mercdatay)
    lVenus.set_data(Venusdatax,Venusdatay)
    
    oT.set_data(rt[i,0],rt[i,1])
    oJ.set_data(rj[i,0],rj[i,1])
    oM.set_data(rm[i,0],rm[i,1])
    oMerc.set_data(rmerc[i,0],rmerc[i,1])
    oS.set_data(rsun[i,0],rsun[i,1])
    oVenus.set_data(rvenus[i,0],rvenus[i,1])
    #oHole.set_data(rhole[i,0],rhole[i,1])
    
    
    time_text.set_text(time_template % (t[i]))
    

    
    
p,t=orbitCalc(0.001, 12)

rt=p[0].rList
rj=p[1].rList
rm=p[2].rList
rmerc=p[3].rList
rsun=p[4].rList
rvenus=p[5].rList
#rhole=p[6].rList



t0=t/t[1]
t0=t0.astype(int)
ani=animation.FuncAnimation(fig, make_animation,frames=t0, interval=0.1)









