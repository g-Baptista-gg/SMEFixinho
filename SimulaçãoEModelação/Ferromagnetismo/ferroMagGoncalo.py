%clear
%matplotlib qt
import numpy as np
import os
import matplotlib.pyplot as plt
tipo = float

class GridDot:
    def __init__(self,xcoor,ycoor,fState,energy):
        self.x = xcoor
        self.y=ycoor
        self.state=fState
        self.en=energy
    def flipState(self):
        self.state*=-1
    def newEn(self,nEn):
        self.en=nEn
#_____________________________________________________________________________#
def initGrid2 (nx,ny):
    grid = np.zeros((nx,ny),dtype=object)
    for i in range(nx):
        for j in range (ny):
            rd=np.random.randint(2)
            if rd==0:
                grid[i][j]=GridDot(i, j, -1,0)
            else:
                grid[i][j]=GridDot(i, j, 1,0)
    return grid




    
    




def getValEn (dots):
    enArray=np.zeros(dots.shape,float)
    for i in range(dots.shape[0]):
        for j in range(dots.shape[1]):
            enArray[i][j]=dots[i][j].en
    return enArray
def getValState (dots):
    stateArray=np.zeros(dots.shape,float)
    for i in range(dots.shape[0]):
        for j in range(dots.shape[1]):
            stateArray[i][j]=dots[i][j].state
    return stateArray
    
def deltaCalc (dots,i,j):
    delta=0
    delta+=dots[i-1][j].state
    delta+=dots[i][j-1].state
    if (i+1)==dots.shape[0]:
        delta+=dots[0][j].state
    else:
        delta+=dots[i+1][j].state
    if (j+1)==dots.shape[1]:
        delta+=dots[i][0].state
    else:
        delta+=dots[i][j+1].state
    return delta




def enVar (dots,delta,h,i,j):
    deltaE=(2*delta+h)*dots[i][j].state
    return deltaE
    



def flipper(dots,i,j,deltaE,delta,t,h):
    if deltaE<=0:
        dots[i][j].flipState()
    else:
        prob=np.exp(-deltaE/t)
        rd=np.random.uniform(0,1)
        #print('PROB: '+str(prob))
        #print('RAND: '+str(rd))
        if rd<prob:
            dots[i][j].flipState()
    dots[i][j].newEn(-dots[i][j].state*(delta+2*h))

def runCycle(dots,t,h):
    for i in range(dots.shape[0]):
        for j in range(dots.shape[1]):
            #print('('+str(i)+','+str(j)+')')
            delta = deltaCalc(dots, i, j)
            #print('DELTA=  '+str(delta))
            deltaE=enVar(dots, delta,h, i, j)
            flipper(dots, i, j, deltaE,delta, t,h)
            

def runCycleRnd(dots,t,h):
    k=0
    N=dots.shape[0]*dots.shape[1]
    allPos=np.zeros(N,dtype=object)
    for i in range(dots.shape[0]):
        for j in range(dots.shape[1]):
            allPos[k]=(i,j)
            k+=1
    np.random.shuffle(allPos)
    for z in range(N):
        delta=deltaCalc(dots,allPos[z][0],allPos[z][1])
        deltaE=enVar(dots,delta,h,allPos[z][0],allPos[z][1])
        flipper(dots,allPos[z][0],allPos[z][1],deltaE,delta,t,h)
            
def dataPlots(enMed,state0,state,avg,std):

    
    fig0=plt.figure()
    ax0=fig0.add_subplot(1,2,1)
    im0=ax0.imshow(state0,aspect='auto',cmap='binary',vmin=-1,vmax=1)
    print(state0)
    ax0.title.set_text('Estado Inicial')
    ax1=fig0.add_subplot(1,2,2)
    im1=ax1.imshow(state,aspect='auto',cmap='binary',vmin=-1,vmax=1)
    ax1.title.set_text(str(avg.size-1)+'ª Iteração')
    
    fig0.colorbar(im1,ax=ax1)  
    fig0.colorbar(im0,ax=ax0)    
    fig0.set_size_inches(8,4)

    fig2,axs=plt.subplots(2,2)

    
    
    
    axs[0,0].plot(avg)
    axs[0,0].set_ylabel('Momento Magnético Médio')
    axs[0,0].set_xlabel('Iteração')
    axs[0,1].plot(std)
    axs[0,1].set_ylabel('Desvio Padrão')
    axs[0,1].set_xlabel('Iteração')
    
    axs[1,0].plot(enMed)
    axs[1,0].set_ylabel('Energia Média')
    axs[1,0].set_xlabel('Iteração')
    plt.tight_layout()
def enCalc(dots,h):
    for i in range(dots.shape[0]):
        for j in range(dots.shape[1]):
            E=-dots[i][j].state*(deltaCalc(dots,i,j)+2*h)
            dots[i][j].newEn(E)
    
def ferroMag(nx,ny,N,t,h):
    dots=initGrid2(nx,ny)
    enCalc(dots,0)
    en0=getValEn(dots)
    #print(getValEn(dots))
    state0=getValState(dots)
    enMed=np.zeros(N+1)
    std=np.zeros(N+1)
    avg=np.zeros(N+1)
    enMed[0]=0.5*np.average(en0)
    avg[0]=np.average(state0)
    std[0]=np.std(state0)
    for i in range(N):
        i+=1
        runCycleRnd(dots, t,h)
        enCalc(dots,h)
        state=getValState(dots)
        enCurrent=getValEn(dots)
        enMed[i]=0.5*np.average(enCurrent)
        avg[i]=np.average(state)
        std[i]=np.std(state)
    dataPlots(enMed,state0,state,avg,std)
    #print(getValEn(dots))
        
ferroMag(200,200,100,3,1)
















