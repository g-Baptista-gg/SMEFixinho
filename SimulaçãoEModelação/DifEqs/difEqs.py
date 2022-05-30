%matplotlib qt
%clear
import numpy as np
import matplotlib.pyplot as plt
def orbitCalEuler(t, r, v, deltaT, nPasso):
    '''Calcula nPasso da órbita
    t: tempo inicial
    r: Vector posição
    v: vector velocidade
    deltaT: Delta t em cada passo
    nPasso: Número de passos a efectuar
    
    return: final values of t, r, v'''
    
    GM = 4. * np.pi ** 2
    
    passo = 0
    while passo < nPasso:
        #Cálculo e actualização das variáveis
        t += deltaT
        rNorm = np.sqrt((r * r).sum())
        a = -GM * r / rNorm ** 3
        r = r + v * deltaT
        v = v + a * deltaT

        passo += 1
        
    return t, r, v

def inicializa(tamanho, inicial):
    '''Inicializa os arrays das variáveis do movimento
    tamanho: O tamanho dos arrays a construir
    inicial: Tuple com os valores inicíais de r, v
    
    return: Numpy arrays inicializados a zero t, r, v'''
    
    t = np.zeros(tamanho)
    rData = np.zeros((tamanho, 2))
    rData[0] = inicial[0]
    vData = np.zeros((tamanho, 2))
    vData[0] = inicial[1]
    
    return t, rData, vData



def orbitSimul(inicial, deltaT, tmax, grafTempos = 0.005):
    '''Calcula a orbital de um dado corpo
    inicial: Tuple com valores de r, v iniciais
    deltaT: Valor de intervalo de tempo entre passos
    tmax: O tempo total a simular em unidades da simulação
    grafTempos: O intervalo de tempos par guardar os valores
    
    return: Numpy arrays com t, r, v'''
    
    #Se grafTempos < deltaT passa a ser deltaT
    grafTempos = grafTempos if grafTempos > deltaT else deltaT
    
    tamanho = int(tmax / grafTempos) + 1
    
    t, rData, vData = inicializa(tamanho, inicial)
    
    nPassos = int(grafTempos / deltaT)
    
    im = 0
    index = 1
    while index < tamanho:
        t[index], rData[index], vData[index] = orbitCalEuler(t[im],rData[im], vData[im], deltaT, nPassos)
        im = index
        index += 1
    
    return t, rData, vData


def orbitCalCromer(t, r, v, deltaT, nPasso):
    '''Calcula nPasso da órbita
    t: tempo inicial
    r: Vector posição
    v: vector velocidade
    deltaT: Delta t em cada passo
    nPasso: Número de passos a efectuar
    
    return: final values of t, r, v'''
    
    GM = 4. * np.pi ** 2
    
    passo = 0
    while passo < nPasso:
        #Cálculo e actualização das variáveis
        t += deltaT
        rNorm = np.sqrt((r * r).sum())
        a = -GM * r / rNorm ** 3
        
        v = v + a * deltaT
        r = r + v * deltaT
        passo += 1
        
    return t, r, v
def orbitSimulCromer(inicial, deltaT, tmax, grafTempos = 0.005):
    '''Calcula a orbital de um dado corpo
    inicial: Tuple com valores de x, vx, y e vy iniciais
    deltaT: Valor de intervalo de tempo entre passos
    tmax: O tempo total a simular em unidades da simulação
    grafTempos: O intervalo de tempos par guardar os valores
    
    return: Numpy arrays com t, r, v'''
    
    #Se grafTempos > deltaT passa a ser deltaT
    grafTempos = grafTempos if grafTempos > deltaT else deltaT
    
    tamanho = int(tmax / grafTempos) + 1
    
    t, rData, vData = inicializa(tamanho, inicial)
    
    nPassos = int(grafTempos / deltaT)
    
    im = 0
    index = 1
    while index < tamanho:
        t[index], rData[index], vData[index] = orbitCalCromer(t[im],rData[im], vData[im], deltaT, nPassos)
        im = index
        index += 1
    
    return t, rData, vData






r0 = np.array([1.0, 0.0])
v0 = np.array([0.0, .6 * np.pi]) 
t, r, v = orbitSimulCromer((r0, v0), .001, 30)






fig, ax = plt.subplots(figsize = (12, 12))
ax.plot(r[:, 0], r[:, 1])
#ax.set_box_aspect(1)

