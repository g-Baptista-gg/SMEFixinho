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
    def  __init__(self,name, mass, radius,period,color,size):
        self.name=name
        self.m = mass 
        self.color=color
        tudo=randVals(radius, period)
        self.coor=tudo[0]
        self.v = tudo[1]
        self.rList=np.zeros((size,2))
        self.rList[0]=self.coor
        self.vList=np.zeros((size,2))
        self.vList[0]=self.v
        self.energy=0
        self.eList=np.zeros(size)
    def __str__(self):
        return 'Planeta: '+str(self.name) + '       Coordenadas: ' + str(self.coor)

def initialize(size):
    t=np.zeros(size)
    planets=np.zeros(0)
    '''Aqui devem ser inseridos os planetas do sistema Solar'''
    planets=np.append(planets,Planet('Terra', 1/332946, 1,1,"blue", size))
    
    planets=np.append(planets,Planet('Júpiter', 1/1047.35, 5.2,11.9,"orange", size))
    
    planets=np.append(planets,Planet('Marte', 1/332946*0.107, 1.5,1.9,"red", size))
    
    planets=np.append(planets,Planet('Mercury', 0.055*1/332946, 0.4,88/365,"grey", size))
    
    planets=np.append(planets,Planet('Sun', 1, 0,0,"yellow", size))
    
    planets=np.append(planets,Planet('Venus',0.815*1/332946 , 0.7,225/365,"green", size))
    #planets=np.append(planets,Planet('Black Hole',1,5,0,"white", size))

    
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
    return pos,vel
def orbitCalc(deltaT,Tmax,interaction,tStep=0.01):
    
    size=int(Tmax/tStep)+1
    nStep=int(tStep/deltaT)
    
    planets,t=initialize(size)
    eInit(planets)
    for i in range(size-1):
        step=0
        while step<nStep:
            for p in range(planets.shape[0]):
                if interaction == 1 :
                    a=aCalc(planets[p],planets,p)
                else:
                    a=aCalcBasic(planets[p])
                planets[p].v+=a*deltaT
                planets[p].coor=planets[p].coor+planets[p].v*deltaT
                planets[p].energy+=0.5*planets[p].m* (planets[p].v*planets[p].v).sum()
            step+=1
        loadVnC(planets, i)
        t[i+1]+=deltaT*nStep+t[i]
    return planets,t
            
def eInit(pArray):
    GM=4.*np.pi**2
    for p in range(pArray.shape[0]):
        for i in range(pArray.shape[0]-1):
            r=pArray[p].coor-pArray[p-(i+1)].coor
            rNorm=np.sqrt((r*r).sum())
            energy=-GM*pArray[p].m*pArray[p-(i+1)].m/rNorm
            energy+=0.5*pArray[p].m*(pArray[p].v*pArray[p].v).sum()
            pArray[p].eList[0]=energy

def aCalc(planet,pArray,p):
    GM=4.*np.pi**2

    a=0
    for i in range(pArray.shape[0]-1):
        r=planet.coor-pArray[p-(i+1)].coor
        rNorm=np.sqrt((r*r).sum())
        a += -GM* pArray[p-(i+1)].m * r / rNorm ** 3
        planet.energy=-GM*planet.m*pArray[p-(i+1)].m/rNorm
    return a

def aCalcBasic(planet):
    GM=4.*np.pi**2
    r=planet.coor
    rNorm=np.sqrt((r*r).sum())
    a = -GM*r/rNorm**3
    return a

def loadVnC(pArray,i):
    for p in range(pArray.shape[0]):
        pArray[p].rList[i+1]=pArray[p].coor
        pArray[p].vList[i+1]=pArray[p].v
        pArray[p].eList[i+1]=pArray[p].energy
    
def initPlots(planets,ax):
    size=planets.shape[0]
    plots=np.zeros((size,4),dtype=object)
    for i in range(size):
        a, =ax.plot([],[],'o',color=planets[i].color,label=planets[i].name)
        b, =ax.plot([],[],'-',color=planets[i].color)
        datax=[]
        datay=[]
        plots[i]=np.array([a,b,datax,datay],dtype=object)
        
    return plots
def makeAnimation2(i):
    for j in range(p.shape[0]):
        if i == 0 :
            plots[j][2].clear
            plots[j][3].clear
        pos=p[j].rList
        plots[j][2].append(pos[i,0])
        plots[j][3].append(pos[i,1])
        plots[j][1].set_data(plots[j][2],plots[j][3])
        plots[j][0].set_data(pos[i,0],pos[i,1])
        time_text.set_text(time_template % (t[i]))

def makeFreqPlots(p,p0):
    figfreq=plt.figure()
    figfreq.suptitle('Frequências')
    figen=plt.figure()
    figen.suptitle('Energias')
    freqplots=np.zeros(p.shape[0],dtype=object)
    enplots=np.zeros(p.shape[0],dtype=object)
    for i in range(p.shape[0]):
        freqplots[i]=figfreq.add_subplot(4,2,i+1)
        x=np.fft.rfftfreq(p[i].rList[:,0].shape[0],0.01)
        y=abs(np.fft.rfft(p[i].rList[:,0]))
        freqplots[i].plot(x,y)
        x0=np.fft.rfftfreq(p0[i].rList[:,0].shape[0],0.01)
        y0=abs(np.fft.rfft(p0[i].rList[:,0]))
        freqplots[i].plot(x0,y0)
        freqplots[i].set_yscale('log')
        freqplots[i].set_xlim(0,20)
        freqplots[i].set_title(p[i].name)
        
        enplots[i]=figen.add_subplot(4,2,i+1)
        enplots[i].plot(p[i].eList)
        enplots[i].set_title(p[i].name)

    figfreq.tight_layout()
    figen.tight_layout()
            

            
            
fig, ax =plt.subplots()
ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect('equal')
    

    
    
p,t=orbitCalc(0.001, 50,1)
p0,tlixo=orbitCalc(0.001,50,0)
time_template = '%.2f years'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
plots=initPlots(p,ax)

plt.legend()
rt=p[0].rList

makeFreqPlots(p, p0)

t0=t/t[1]
t0=t0.astype(int)
ani=animation.FuncAnimation(fig, makeAnimation2,frames=t0, interval=.1)







