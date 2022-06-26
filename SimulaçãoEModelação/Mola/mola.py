"""
Movimento Oscilatório Composto - Gonçalo Baptista, nº 55069; José Grilo, nº 54926

Objetivo de Programação:
"""
#%%

%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as sc
import matplotlib.animation as animation

#%%

class Body:
    def __init__(self, mass, k, xEq, x0, v0, size):
        self.mass = mass #  body mass
        self.k = k  #   spring constant
        self.xEq = xEq
        self.x = x0 #   instant pos
        self.v = v0 #   instant velocity
        
        self.xList = np.zeros(size)
        self.xList[0] = x0
        
        self.vList = np.zeros(size)
        self.vList[0] = v0
   
#%%

def energyCalc(springs):
    n = springs.size
    energy = 0
    
    for i in range(n):
        if i == 0:
            energy += 0.5 * springs[i].mass * springs[i].v ** 2 + 0.5 * springs[i].k * (springs[i].x - springs[i].xEq) ** 2
        else:
            energy += 0.5 * springs[i].mass * springs[i].v ** 2 + 0.5 * springs[i].k * (springs[i].x - springs[i - 1].x - springs[i].xEq) ** 2
    
    return energy
        
#%%
        
def springCalc(springArray, springForce, sAcce, saveSteps, dt):
    n = springArray.size
    
    passo = 0
    while passo < saveSteps:
        for i in range(n):
            if i == 0:
                springForce[i] = springArray[i].k * (springArray[i].x - springArray[i].xEq)
            else:
                springForce[i] = springArray[i].k * (springArray[i].x - springArray[i - 1].x - springArray[i].xEq)
        
        for i in range(n):
            sAcce[i] = - springForce[i] / springArray[i].mass + springForce[i + 1] / springArray[i].mass
            springArray[i].v += sAcce[i] * dt
            springArray[i].x += springArray[i].v * dt
        passo += 1
        
#%%

def springSimulCromer(Tmax, dt, tSample, sArray):
    
    size = int(Tmax/tSample)
    nStep = int(Tmax/dt)
    saveSteps = int(tSample/dt)
    
    n = len(sArray)
    
    springs = np.zeros(n, dtype = object)
    
    for i in range(n):
        springs[i] = Body(sArray[i][0], sArray[i][1], sArray[i][2], sArray[i][3], sArray[i][4], size + 1)
    
    sForce = np.zeros(n + 1, dtype = float)
    sAcce = np.zeros(n, dtype = float)
    time = np.zeros(size + 1, dtype = float)
    energy = np.zeros(size + 1, dtype = float)
    
    energy[0] = energyCalc(springs)
    
    for i in range(size):
        time[i + 1] = time[i] + tSample
        springCalc(springs, sForce, sAcce, saveSteps, dt)
        for j in range(n):
            springs[j].vList[i + 1] = springs[j].v
            springs[j].xList[i + 1] = springs[j].x
        energy[i + 1] = energyCalc(springs)
        
    return springs, energy, time


#%%

def initPlots(springs):
    size = springs.size
    plots = np.zeros((size,2), dtype = object)
    #plotsSprings=np.zeros((size),dtype = object)
    for i in range(size):
        plots[i,0], = plt.plot([], [], "o", color = "red")
        plots[i,1],=plt.plot([],[],"-", color='black')
    return plots

def makeAnimation(i):
    #print(i.size)
    for j in range(i.size):
        plotsAni[j,0].set_data(i[j], 0)
        springsx=[]
        springsy=[]
        nsprings=20
        if j == 0 :
            for k in range(nsprings+1):
                springsx.append(k*i[j]/nsprings)
                springsy.append(0.2*np.sin(k*np.pi/2))
        else:
            for k in range(nsprings+1):
                springsx.append(i[j-1]+k*(i[j]-i[j-1])/nsprings)
                print(springsx)
                springsy.append(0.2*np.sin(k*np.pi/2))
        plotsAni[j,1].set_data(springsx,springsy)
        

#%%

mola1 = (1, 10, 5, 7, 0)
mola2 = (1, 10, 5, 12, 0)
mola3 = (1, 10, 5, 13, 0)

molas = [mola1, mola2, mola3]

a, b, t = springSimulCromer(100, 0.001, 0.01, molas)

for i in range(a.size):
    plt.plot(t, a[i].xList)

fig, ax = plt.subplots()
ax.plot(t, b)

fourier1 = sc.rfft(a[0].xList)
fourier2 = sc.rfft(a[1].xList)
fourier3 = sc.rfft(a[2].xList)
fourierfreq = sc.rfftfreq(a[0].xList.size, 0.01)

fig2, ax2 = plt.subplots()
ax2.plot(fourierfreq, abs(fourier1))
ax2.plot(fourierfreq, abs(fourier2))
ax2.plot(fourierfreq, abs(fourier3))
#ax2.set_yscale('log')
ax2.set_ylim(-100, 20000)

r = np.column_stack((a[0].xList, a[1].xList, a[2].xList))

figAni, axAni = plt.subplots()
axAni.set_xlim(0, 20)
axAni.set_ylim(-2, 2)
plotsAni = initPlots(a)
ani = animation.FuncAnimation(figAni, makeAnimation, frames = r, interval = .1)




