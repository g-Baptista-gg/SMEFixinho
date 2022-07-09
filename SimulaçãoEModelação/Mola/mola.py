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
import copy
from matplotlib.widgets import Slider, Button, RangeSlider, TextBox, CheckButtons, RadioButtons

#%%

class Body:                 #   Cada corpo possui associado a si uma mola à esquerda
    def __init__(self, mass, k, xEq, x0, v0, size):
        self.mass = mass    #   body mass
        self.k = k          #   spring constant
        self.xEq = xEq      #   Equilibrium displacement
        self.x = x0         #   instant position
        self.v = v0         #   instant velocity
        
        self.xList = np.zeros(size)
        self.xList[0] = x0 #    guarda-se a posição inicial
        
        self.vList = np.zeros(size)
        self.vList[0] = v0
        
   
#%%

def energyCalc(springs):
    """
    Função
    ---------
    Calcula a soma das energias potenciais das molas e cinéticas dos corpos

    Parameters
    ----------
    springs : Array de objetos
        Array onde tem as várias molas/corpos do sistema

    Returns
    -------
    energy : float
        Energia total do sistema.

    """
    n = springs.size
    energy = 0
    
    for i in range(n):
        if i == 0:          # Apenas necessida da posição
            energy += 0.5 * springs[i].mass * springs[i].v ** 2 + 0.5 * springs[i].k * (springs[i].x - springs[i].xEq) ** 2
        else:
            energy += 0.5 * springs[i].mass * springs[i].v ** 2 + 0.5 * springs[i].k * (springs[i].x - springs[i - 1].x - springs[i].xEq) ** 2
    
    return energy
        
#%%
        
def acceCalc(springs, sSize, sForce, sAcce): 
    """
    Função:
    ---------
    Calcula as forças e acelerações para todos os corpos do sistema.
    
    
    Parameters
    ----------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
        
    sSize : Int
        Indicador do número de molas/corpos
        
    sForce : Array de floats
        Array de Forças sentidas exercidas pelo corpo da esquerda
        
    sAcce : Array de floats
        Array com as acelerações sentidas por cada corpo. Necessário para o cálculo do próximo passo
        

    Returns
    -------
    Não retorna nada. Apenas modifica Arrays já existentes.

    """
    
    for i in range(sSize):
        if i == 0:
            sForce[i] = springs[i].k * (springs[i].x - springs[i].xEq)
        else:
            sForce[i] = springs[i].k * (springs[i].x - springs[i - 1].x - springs[i].xEq)
            
    for i in range(sSize):
        sAcce[i] = - sForce[i] / springs[i].mass + sForce[i + 1] / springs[i].mass

#%%

def springCalcCromer(springs, sForce, sAcce, saveSteps, dt):
    """
    Função:
    ---------
    Calcula as novas posições e velocidades para cada mola com base no algoritmo de Euler Cromer

    Parameters
    ----------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
        
    sForce : Array de floats
        Array de Forças sentidas exercidas pelo corpo da esquerda
        
    sAcce : Array de floats
        Array com as acelerações sentidas por cada corpo. Necessário para o cálculo do próximo passo
        
    saveSteps : Int
        Número de passos que devem ser executados até se guardar os dados para amostragem.
    dt : float
        Tempo entre passos

    Returns
    -------
    Nada. Apenas atualiza as coordenadas e velocidades instantâneas para cada corpo.

    """
    n = springs.size
    passo = 0
    
    while passo < saveSteps:
        acceCalc(springs, n, sForce, sAcce)
        for i in range(n):
            springs[i].v += sAcce[i] * dt
            springs[i].x += springs[i].v * dt
        passo += 1
        
#%%

def springCalcRK4(springs, sForce, sAcce, saveSteps, dt):
    """
    Função:
    ---------
    Calcula as novas posições e velocidades para cada mola com base no algoritmo de Runge-Kutta de Ordem 4

    Parameters
    ----------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
        
    sForce : Array de floats
        Array de Forças sentidas exercidas pelo corpo da esquerda
        
    sAcce : Array de floats
        Array com as acelerações sentidas por cada corpo. Necessário para o cálculo do próximo passo
        
    saveSteps : Int
        Número de passos que devem ser executados até se guardar os dados para amostragem.
    dt : float
        Tempo entre passos

    Returns
    -------
    Nada. Apenas atualiza as coordenadas e velocidades instantâneas para cada corpo.

    """
    n = springs.size
    passo = 0
    
    while passo < saveSteps:
        acceCalc(springs, n, sForce, sAcce)
        for i in range(n):
            v=springs[i].v

            springs[i].v += sAcce[i] * dt
            
            k2=v+ springs[i].v*dt/2 + sAcce[i] * (dt/2)
            
            k3=v+ k2 * dt/2 + sAcce[i] * (dt/2)
            
            k4=v+ k3*dt + sAcce[i] * dt
            
            springs[i].x += dt/6 * (springs[i].v+2*k2+2*k3+k4)
        passo += 1

#%%

def springCalcBeeman(springs, sForce, sAcce0, sAcce1, sAcce2, saveSteps, dt):
    """
    Função:
    ---------
    Calcula as novas posições e velocidades para cada mola com base no algoritmo de Beeman

    Parameters
    ----------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
        
    sForce : Array de floats
        Array de Forças sentidas exercidas pelo corpo da esquerda.
        
    sAcce0 : Array de floats
        Array com as acelerações do passo anterior
        
    sAcce1 : Array de floats
        Array com as acelerações  do passo atual
        
    sAcce2 : Array de floats
        Array com as acelerações do próximo passo
        
    saveSteps : Int
        Número de passos que devem ser executados até se guardar os dados para amostragem.
    dt : float
        Tempo entre passos

    Returns
    -------
    sAcce0 : Array de floats
        Array com as acelerações do passo anterior
        
    sAcce1 : Array de floats
        Array com as acelerações  do passo atual
        
    sAcce2 : Array de floats
        Array com as acelerações do próximo passo

    """
    n = springs.size
    passo = 0
    
    while passo < saveSteps:
        for i in range(n):
            springs[i].x += springs[i].v * dt + 2/3 * sAcce1[i] * dt ** 2 - 1/6 * sAcce0[i] * dt ** 2 
        acceCalc(springs, n, sForce, sAcce2)
        for i in range(n):
            springs[i].v += 1/3 * sAcce2[i] * dt + 5/6 * sAcce1[i] * dt - 1/6 * sAcce0[i] * dt

        sAcce0 = copy.deepcopy(sAcce1)
        sAcce1 = copy.deepcopy(sAcce2)
        
        passo += 1
    return sAcce0, sAcce1, sAcce2
        
#%%        
        
def springCalcVerlet(springs, sForce, sAcce, saveSteps, dt, xLast, xPos):
    """
    Função:
    ---------
    Calcula as novas posições e velocidades para cada mola com base no algoritmo de Verlet

    Parameters
    ----------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
        
    sForce : Array de floats
        Array de Forças sentidas exercidas pelo corpo da esquerda
        
    sAcce : Array de floats
        Array com as acelerações sentidas por cada corpo. Necessário para o cálculo do próximo passo
        
    saveSteps : Int
        Número de passos que devem ser executados até se guardar os dados para amostragem.
    dt : float
        Tempo entre passos
        
    xLast : Array de floats
        Posição do passo anterior para cada corpo.
        
    xPos : Array de floats
        Posição atual para cada corpo

    Returns
    -------
    xLast : Array de floats
        Posição do passo anterior para cada corpo.

    """
    n = springs.size
    passo = 0
    
    while passo < saveSteps:
        acceCalc(springs, n, sForce, sAcce)
        for i in range(n):
            xPos[i] = copy.deepcopy(springs[i].x)
            springs[i].x = 2 * springs[i].x - xLast[i] + sAcce[i] * dt ** 2

        xLast = copy.deepcopy(xPos)

        
        passo += 1
    return xLast

#%%

def springSimulCromer(Tmax, dt, tSample, sArray):
    """
    

    Parameters
    ----------
    Tmax : Float
        Tempo total da simulação
    dt : Float
        Tempo entre passos
    tSample : Float
        Tempo entre cada amostragem
    sArray : Array de strings
        Array com as características de inicialização de cada corpo indicadas pelo usuário na GUI.

    Returns
    -------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
    energy : Array de floats
        Array com as energias do sistema a cada amostragem
    time : Array de floats
        Array com os tempos de cada amostragem

    """
    
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
        springCalcCromer(springs, sForce, sAcce, saveSteps, dt)
        for j in range(n):
            springs[j].vList[i + 1] = springs[j].v
            springs[j].xList[i + 1] = springs[j].x
        energy[i + 1] = energyCalc(springs)
        
    return springs, energy, time

#%%

def springSimulBeeman(Tmax, dt, tSample, sArray):
    """
    

    Parameters
    ----------
    Tmax : Float
        Tempo total da simulação
    dt : Float
        Tempo entre passos
    tSample : Float
        Tempo entre cada amostragem
    sArray : Array de strings
        Array com as características de inicialização de cada corpo indicadas pelo usuário na GUI.

    Returns
    -------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
    energy : Array de floats
        Array com as energias do sistema a cada amostragem
    time : Array de floats
        Array com os tempos de cada amostragem

    """
    size = int(Tmax/tSample)
    nStep = int(Tmax/dt)
    saveSteps = int(tSample/dt)
    
    n = len(sArray)
    
    springs = np.zeros(n, dtype = object)
    
    for i in range(n):
        springs[i] = Body(sArray[i][0], sArray[i][1], sArray[i][2], sArray[i][3], sArray[i][4], size + 1)
        
    sForce = np.zeros(n + 1, dtype = float)
    sAcce0 = np.zeros(n, dtype = float)
    sAcce1 = np.zeros(n, dtype = float)
    sAcce2 = np.zeros(n, dtype = float)
    time = np.zeros(size + 1, dtype = float)
    energy = np.zeros(size + 1, dtype = float)
    
    energy[0] = energyCalc(springs)
    
    for i in range(size):
        if i == 0 :
            acceCalc(springs, n, sForce, sAcce1)
            sAcce0 = copy.deepcopy(sAcce1)
        time[i + 1] = time[i] + tSample
        sAcce0, sAcce1, sAcce2 = springCalcBeeman(springs, sForce, sAcce0, sAcce1, sAcce2, saveSteps, dt)
            
        for j in range(n):
            springs[j].vList[i + 1] = springs[j].v
            springs[j].xList[i + 1] = springs[j].x
        energy[i + 1] = energyCalc(springs)
        
    return springs, energy, time

#%%

def springSimulVerlet(Tmax, dt, tSample, sArray):
    """
    

    Parameters
    ----------
    Tmax : Float
        Tempo total da simulação
    dt : Float
        Tempo entre passos
    tSample : Float
        Tempo entre cada amostragem
    sArray : Array de strings
        Array com as características de inicialização de cada corpo indicadas pelo usuário na GUI.

    Returns
    -------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
    energy : Array de floats
        Array com as energias do sistema a cada amostragem
    time : Array de floats
        Array com os tempos de cada amostragem

    """
    size = int(Tmax/tSample)
    nStep = int(Tmax/dt)
    saveSteps = int(tSample/dt)
    
    n = len(sArray)
    
    springs = np.zeros(n, dtype = object)
    sForce = np.zeros(n + 1, dtype = float)
    sAcce = np.zeros(n, dtype = float)
    xLast = np.zeros(n, dtype = float)
    xPos = np.zeros(n, dtype = float)
    time = np.zeros(size + 1, dtype = float)
    energy = np.zeros(size + 1, dtype = float)
    
    for i in range(n):
        springs[i] = Body(sArray[i][0], sArray[i][1], sArray[i][2], sArray[i][3], sArray[i][4], size + 1)
        xLast[i] = springs[i].x-springs[i].v*dt
    
    energy[0] = energyCalc(springs)
    
    for i in range(size):
        time[i + 1] = time[i] + tSample
        xLast = springCalcVerlet(springs, sForce, sAcce, saveSteps, dt, xLast, xPos)
            
        for j in range(n):
            springs[j].vList[i + 1] = springs[j].v
            springs[j].xList[i + 1] = springs[j].x
        energy[i + 1] = energyCalc(springs)
        
    return springs, energy, time


#%%

def springSimulRK4(Tmax,dt,tSample,sArray):
    """
    

    Parameters
    ----------
    Tmax : Float
        Tempo total da simulação
    dt : Float
        Tempo entre passos
    tSample : Float
        Tempo entre cada amostragem
    sArray : Array de strings
        Array com as características de inicialização de cada corpo indicadas pelo usuário na GUI.

    Returns
    -------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema
    energy : Array de floats
        Array com as energias do sistema a cada amostragem
    time : Array de floats
        Array com os tempos de cada amostragem

    """
    
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
        springCalcRK4(springs, sForce, sAcce, saveSteps, dt)
        for j in range(n):
            springs[j].vList[i + 1] = springs[j].v
            springs[j].xList[i + 1] = springs[j].x
        energy[i + 1] = energyCalc(springs)
        
    return springs, energy, time

#%%

def initPlots(springs):
    """
    

    Parameters
    ----------
    springs : Array de objetos
        Array com as várias molas/corpos do sistema

    Returns
    -------
    plots : Array de plots
        Array com 2 plots para a animação: um para representação gráfica dos corpos, e outro das molas

    """
    size = springs.size
    plots = np.zeros((size, 2), dtype = object)
    #plotsSprings = np.zeros((size), dtype = object)
    for i in range(size):
        plots[i, 0], = plt.plot([], [], "o", color = "red", zorder = 1)     #   Bolas vermelhas, na layer superior
        plots[i, 1], = plt.plot([], [], "-", color = "black", zorder = 0)   #   Traços pretos, na layer inferior
    return plots

def makeAnimation(i):
    """
    

    Parameters
    ----------
    i : Objeto do array de frames
        Contém as posições de certa iteração para todos os corpos

    Returns
    -------
    Nada. Apenas trata de atualizar os dados durante a animação

    """
    s = i.size

    if s == 1:
        plotsAni[0, 0].set_data(i, 0)
        springsx = []
        springsy = []
        nsprings = 20
        for k in range(nsprings + 1):
            springsx.append(k * i/nsprings)
            springsy.append(0.2 * np.sin(k * np.pi/2))
        plotsAni[0, 1].set_data(springsx, springsy)
    else:
        for j in range(i.size):
            plotsAni[j, 0].set_data(i[j], 0)
            springsx = []
            springsy = []
            nsprings = 20
            if j == 0 :
                for k in range(nsprings + 1):
                    springsx.append(k * i[j]/nsprings)
                    springsy.append(0.2 * np.sin(k * np.pi/2))
            else:
                for k in range(nsprings + 1):
                    springsx.append(i[j - 1] + k * (i[j] - i[j - 1])/nsprings)
                    springsy.append(0.2 * np.sin(k * np.pi/2))
            plotsAni[j, 1].set_data(springsx, springsy)
    
#%%

def runGui(*args):
    """
    

    Parameters
    ----------
    *args : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    global ani
    global plotsAni
    global springTextArray
    
    alg = algcb.get_status()
    
    tmax = float(tmaxtb.text)
    dt = float(dttb.text)
    tSample = float(tsamtb.text)
    
    molas = []
    #molas.append([float(sprtb.text), float(sprtb2.text), float(sprtb3.text), float(sprtb4.text), float(sprtb5.text)])
    #molas.append([1, 10, 5, 7, 0])
    for i in range(len(springTextArray)):
        s0=float(springTextArray[i][1].text)
        s1=float(springTextArray[i][3].text)
        s2=float(springTextArray[i][5].text)
        s3=float(springTextArray[i][7].text)
        s4=float(springTextArray[i][9].text)
        S=[s0,s1,s2,s3,s4]
        molas.append(S)
    
    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    
    if alg[0] == True:
        a, b, t = springSimulCromer(tmax, dt, tSample, molas)
        for i in range(a.size):
            ax.plot(t, a[i].xList, label ='Mola ' + str(i+1)+ ' Euler-Cromer')
            fourier = sc.rfft(a[i].xList)
            fourierfreq = sc.rfftfreq(a[0].xList.size, 0.01)
            ax2.plot(fourierfreq, abs(fourier), label ='Mola ' + str(i+1)+ 'Euler-Cromer')
        
    if alg[1] == True:
        a2, b2, t2 = springSimulVerlet(tmax, dt, tSample, molas)
        for i in range(a2.size):
            ax.plot(t2, a2[i].xList, label ='Mola ' + str(i+1)+ 'Verlet')
            fourier2 = sc.rfft(a2[i].xList)
            fourierfreq = sc.rfftfreq(a2[0].xList.size, 0.01)
            ax2.plot(fourierfreq, abs(fourier2), label ='Mola ' + str(i+1)+ 'Verlet')
        
    if alg[2] == True:
        a3, b3, t3 = springSimulBeeman(tmax, dt, tSample, molas)
        for i in range(a3.size):
            ax.plot(t3, a3[i].xList, label ='Mola ' + str(i+1)+ 'Beeman')
            fourier3 = sc.rfft(a3[i].xList)
            fourierfreq = sc.rfftfreq(a3[0].xList.size, 0.01)
            ax2.plot(fourierfreq, abs(fourier3), label ='Mola ' + str(i+1)+ 'Beeman')
            
    if alg[3] == True:
        a4, b4, t4 = springSimulRK4(tmax, dt, tSample, molas)
        for i in range(a4.size):
            ax.plot(t4, a4[i].xList, label ='Mola ' + str(i+1)+ 'RK4')
            fourier4 = sc.rfft(a4[i].xList)
            fourierfreq = sc.rfftfreq(a4[0].xList.size, 0.01)
            ax2.plot(fourierfreq, abs(fourier4), label ='Mola ' + str(i+1)+ 'RK4')
            
    ax.legend()
    ax2.legend()
    ax2.set_xlim([0.1,1])
    ax2.set_ylim([0,10000])
    
    if a.size == 1:
        r = a[0].xList
    else:
        for i in range(a.size-1):
            if i == 0:
                r=np.column_stack((a[0].xList,a[1].xList))
            else:
                r=np.column_stack((r,a[i+1].xList))
            
        #r = np.column_stack((a[0].xList))

    figAni, axAni = plt.subplots()
    axAni.set_xlim(0, 20)
    axAni.set_ylim(-5, 5)
    plotsAni = initPlots(a)
    ani = animation.FuncAnimation(figAni, makeAnimation, frames = r, interval = .1)

#%%

def addSpring(*args):
    """
    

    Parameters
    ----------
    *args : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    global pos
    global springTextArray
    
    global molaName
    molaName+=1
    
    global xIn
    xIn+=3
    
    
    pos-=0.05
    s0 = plt.axes([0.15, pos, 0.05, 0.03])
    s1 = TextBox(s0,'Mola '+str(molaName)+  ': Massa(kg)', initial = '1')

    s2 = plt.axes([0.25, pos, 0.05, 0.03])
    s3 = TextBox(s2, '$k$(N/m)', initial = '10')

    s4 = plt.axes([0.35, pos, 0.05, 0.03])
    s5 = TextBox(s4, '$d_{Eq}$(m)', initial = '5')

    s6 = plt.axes([0.45, pos, 0.05, 0.03])
    s7 = TextBox(s6, '$x_0$(m)', initial = str(xIn))

    s8 = plt.axes([0.55, pos, 0.05, 0.03])
    s9 = TextBox(s8, '$v_0$(m/s)', initial = '0')
    sA0=[s0,s1,s2,s3,s4,s5,s6,s7,s8,s9]
    
    springTextArray.append(sA0)
    
    global butPos
    global plusax
    global minax
    
    butPos-=0.05
    plusax.set_position([0.35, butPos, 0.03, 0.03], which='both')
    minax.set_position([0.25, butPos, 0.03, 0.03], which='both')
    
def takeSpring(*args):
    """
    

    Parameters
    ----------
    *args : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    global pos
    global xIn
    global butPos
    
    pos+=0.05
    butPos+=0.05
    
    global springTextArray
    
    global molaName
    
    
    if molaName>1 :
        for i in range(5):
            springTextArray[-1][i*2].remove()
            
        springTextArray.pop()
    molaName-=1
    xIn-=3
    plusax.set_position([0.35, butPos, 0.03, 0.03], which='both')
    minax.set_position([0.25, butPos, 0.03, 0.03], which='both')
    
    


gui = plt.figure(figsize = (12, 7))

algax = plt.axes([0.65, 0.65, 0.12, 0.2])
algcb = CheckButtons(algax, ['Euler-Cromer', 'Verlet', 'Beeman','RK4'])

runax = plt.axes([0.675, 0.2, 0.2, 0.2])
runbut = Button(runax, 'Run')
runbut.on_clicked(runGui)

butPos=0.7

minax = plt.axes([0.25, butPos, 0.03, 0.03])
minbut = Button(minax, '-')
minbut.on_clicked(takeSpring)


plusax = plt.axes([0.35, butPos, 0.03, 0.03])
plusbut = Button(plusax, '+')

pos=0.8
springTextArray=[]
plusbut.on_clicked(addSpring)

molaName=1
xIn=7

s0 = plt.axes([0.15, 0.8, 0.05, 0.03])
s1 = TextBox(s0,'Mola '+str(molaName)+  ': Massa(kg)', initial = '1')

s2 = plt.axes([0.25, 0.8, 0.05, 0.03])
s3 = TextBox(s2, '$k$(N/m)', initial = '10')

s4 = plt.axes([0.35, 0.8, 0.05, 0.03])
s5 = TextBox(s4, '$d_{Eq}$(m)', initial = '5')

s6 = plt.axes([0.45, 0.8, 0.05, 0.03])
s7 = TextBox(s6, '$x_0$(m)', initial = str(xIn))

s8 = plt.axes([0.55, 0.8, 0.05, 0.03])
s9 = TextBox(s8, '$v_0$(m/s)', initial = '0')
sA0=[s0,s1,s2,s3,s4,s5,s6,s7,s8,s9]

springTextArray.append(sA0)


dtax = plt.axes([0.85, 0.8, 0.05, 0.03])
dttb = TextBox(dtax, '$dt$(s)', initial = '0.001')



tmaxax = plt.axes([0.85, 0.7, 0.05, 0.03])
tmaxtb = TextBox(tmaxax, '$t_{Max}$(s)', initial = '100')

tsamax = plt.axes([0.85, 0.6, 0.05, 0.03])
tsamtb = TextBox(tsamax, '$t_{Sample}$(s)', initial = '0.01')


