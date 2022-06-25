"""
Movimento Oscilatório Composto - Gonçalo Baptista, nº 55069; José Grilo, nº 54926

Objetivo de Programação:
"""
#%%

%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as sc

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
        
def springCalc(springArray, springForce, sAcce, saveSteps, dt):
    n = springArray.size
    for i in range(n):
        if i == 0:
            springForce[i] = springArray[i].k * (springArray[i].x - springArray[i].xEq)
        else:
            springForce[i] = springArray[i].k * (springArray[i].x - springArray[i - 1].x - springArray[i].xEq)
    for i in range(n):
        sAcce[i] = - springForce[i] / springArray[i].mass + springForce[i + 1] / springArray[i].mass
        
#%%

def springSimulCromer(Tmax, dt, tSample):
    size = int(Tmax/tSample) + 1
    nStep = int(Tmax/dt)
    saveSteps = int(tSample/dt)
    
    springArray = np.zeros(2, dtype = object)
    springArray[0] = Body(1, 10, 5, 7, 0, size)
    springArray[1] = Body(1, 10, 5, 12, 0, size)
    
    sForce = np.zeros(3, dtype = float)
    sAcce = np.zeros(2, dtype = float)
    energy = np.zeros(size, dtype = float)
    
    energy[0] = 0.5 * springArray[0].mass * springArray[0].v ** 2 + 0.5 * springArray[1].mass * springArray[1].v ** 2 + 0.5 * springArray[0].k * (springArray[0].x - springArray[0].xEq) ** 2 + 0.5 * springArray[1].k * (springArray[1].x - springArray[0].x - springArray[1].xEq) ** 2
    
    index = 0
    h = 1
    for i in range(nStep):
        index += 1
        #print(index)
        springCalc(springArray, sForce, sAcce, size, dt)
        for j in range(2):
            springArray[j].v += sAcce[j] * dt
            springArray[j].x += springArray[j].v * dt
            if index == saveSteps:
                #print(i)
                springArray[j].vList[h] = springArray[j].v
                springArray[j].xList[h] = springArray[j].x
        if index == saveSteps:
            energy[h] = 0.5 * springArray[0].mass * springArray[0].v ** 2 + 0.5 * springArray[1].mass * springArray[1].v ** 2 + 0.5 * springArray[0].k * (springArray[0].x - springArray[0].xEq) ** 2 + 0.5 * springArray[1].k * (springArray[1].x - springArray[0].x - springArray[1].xEq) ** 2
            index = 0
            h += 1
        
    return springArray, energy

#%%

a, b = springSimulCromer(1000, 0.001, 0.1)
plt.plot(a[0].xList)
plt.plot(a[1].xList)

fig, ax = plt.subplots()
ax.plot(b)
