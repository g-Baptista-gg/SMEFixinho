"""
*______________________________________________________________________________
|  Method [Ecossitema GG]
|
|  Purpose:  Simula a evolução de 2 ecossistemas diferentes (ambos com plantas
|            e herbívoros, mas um com e outro sem carnívoros).
|
|  Parameters:
|      Pesos dos números de cada tipo de ser vivo no ecossistema
|      Tamanho do ecossistema (Matrix NxM)
|      Número de ciclos a executar.
|
|  Returns:  Animações das evoluções temporais para cada um dos ecossistemas e
|            gráficos com estatísticas sobre cada uma dos ecossistemas e das
|            suas populações.
*______________________________________________________________________________
"""

#%% Imports

%clear
%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy
import time
#import multiprocessing as mp

st = time.time()

#%%

'''A classe Bicho tem como objetivo conter toda a informação necessária em relação a um determinado ponto da rede, como o tipo de ser vivo e o seu respetivo nível
    changeType: muda o tipo de ser vivo do ponto da rede
    grow: faz o ser vivo aumenta de nível se este ainda não estiver no nível máximo (2)
    shrink: diminui o nível do ser vivo; se o nível deste for mínimo (0), o tipo de ser vivo passa a 0 (ou seja, passa a ser uma célula sem ser vivo)
    die: o ser vivo morre, ou seja, o tipo de ser vivo passa a 0 (ou seja, passa a ser uma célula sem ser vivo)'''

class Bicho:
    def  __init__(self, sType, size):
        self.type = sType #Tipos possíveis: Vazio(0), Planta(1), Herbívoro(2), Carnívoro(3)
        self.size = size #Níveis possíveis: Fraco(0), Médio(1), Forte(2)
    
    def __str__(self):
        return 'Hallo' #Apenas foi usado para debug
    
    def changeType(self, newType): #Muda o tipo para o novo desejado
        self.type = newType
        self.size = 0
    
    def grow(self): #Faz os bichos crescer até a um máximo de 2
        if self.size < 2:
            self.size += 1
    
    def shrink(self): #Faz os bichos ficar mais fracos e morrer caso já estiverem no estado mais fraco
        if self.size > 0:
            self.size -= 1
        else:
            self.type = 0
            
    def die(self):
        self.type = 0  #Mata o bicho
        
#%%

    '''Inicia a estrutura de dados que contém a informação relacionada com a evolução da rede
    nx: número de linhas da rede
    ny: número de colunas da rede
    p1: peso "relativo" de plantas
    p2: peso "relativo" de herbívoros
    p3: peso "relativo" de carnívoros
    Return: tuple com os diferentes arrays e listas iniciados'''

def initGrid(nx, ny, p1, p2, p3, nIterations):
    grid = np.zeros((nx, ny), dtype = object) #Inicia a rede  
    herbPos = [] #Cria uma lista para as posições dos herbívoros da rede
    carnPos = [] #Cria uma lista para as posições dos carnívoros da rede
    plantPos = [] #Cria uma lista para as posições das plantas da rede
    emptyPos=[] #Cria uma lista para as posições das células vazias da rede
    nPlant = np.zeros(nIterations + 1, dtype = float) 
    nHerb = np.zeros(nIterations + 1, dtype = float) 
    nCarn = np.zeros(nIterations + 1, dtype = float)
    hPlant = np.zeros((nIterations + 1, 3), dtype = float)
    hHerb = np.zeros((nIterations + 1, 3), dtype = float)
    hCarn = np.zeros((nIterations + 1, 3), dtype = float)
    ecossistemas = []
    
    #Preenchimento da rede de forma aleatória com os pesos atríbuidos
    for i in range(nx):
        for j in range(ny):
            rd = np.random.rand()
            size = np.random.randint(3)
            if rd <= p1/(p1 + p2 + p3):
                grid[i][j] = Bicho(1, size)
                plantPos.append([i, j])
            elif rd <= (p1 + p2)/(p1 + p2 + p3):
                grid[i][j] = Bicho(2, size)
                herbPos.append([i, j])
            else:
                grid[i][j] = Bicho(3, size)
                carnPos.append([i, j])
    
    #Ordenação aleatória dos vetores posição de cada uma das listas
    random.shuffle(herbPos)
    random.shuffle(carnPos)
    
    return grid, plantPos, herbPos, carnPos, emptyPos, nPlant, nHerb, nCarn, hPlant, hHerb, hCarn, ecossistemas

#%%

    '''Esta função procura alimento para um determinado ser vivo nos primeiros vizinhos de von Neumann. Note-se que o alimento de um determinado tipo de ser vivo corresponde a (tipo - 1)
    grid: rede do ecossistema
    i: linha onde se encontra o ser vivo
    j: coluna onde se encontra o ser vivo
    Return: posição onde se encontra o alimento ou, em alternativa, -1 caso não encontre alimento'''

def look4food(grid, i, j):
    #Ordena aleatoriamente as células onde se vai procurar alimento
    rdPosvec = [0, 1, 2, 3]
    random.shuffle(rdPosvec)
    
    for n in range(4):
        rdPos = rdPosvec[n]
        
        if rdPos == 0: #Procura de alimento na célula acima
            if grid[i - 1][j].type == (grid[i][j].type - 1):
                if i - 1 == -1 :
                    return [grid.shape[0] - 1, j]
                return [i - 1, j]
        elif rdPos == 1: #Procura de alimento na célula à esquerda
            if grid[i][j - 1].type == (grid[i][j].type - 1):
                if j - 1 == -1 :
                    return [i,grid.shape[1] - 1]
                return [i, j - 1]
        elif rdPos == 2: #Procura de alimento na célula abaixo
            if i + 1 == grid.shape[0]:
                if grid[0][j].type == (grid[i][j].type - 1):
                    return [0, j]
            else:
                if grid[i + 1][j].type == (grid[i][j].type - 1):
                    return [i + 1, j]
        else: #Procura de alimento na célula à direita
            if j + 1 == grid.shape[1]:
                if grid[i][0].type == (grid[i][j].type - 1):
                    return [i, 0]
            else:
                if grid[i][j + 1].type == (grid[i][j].type - 1):
                    return [i, j + 1]
    
    return -1

#%%
    '''Esta função procura espaço para expansão para um determinado ser vivo nos primeiros vizinhos de von Neumann. Note-se que um ser vivo de tipo n só se pode expandir para uma célula cujo tipo m seja tal que n > m
    grid: rede do ecossistema
    i: linha onde se encontra o ser vivo
    j: coluna onde se encontra o ser vivo
    Return: posição para onde se vai expandir ou, em alternativa, -1 caso não se possa expandir para lado nenhum'''
    
def look4space(grid, i, j):
    #ordena aleatoriamente as células onde se vai procurar espaço para expansão
    if grid[i][j].type == 2 :
        possTypes = [0, 1]
    else:
        possTypes = [0, 1, 2]
        
    rdPosvec = [0, 1, 2, 3]
    random.shuffle(rdPosvec)
    
    for n in range(4):
        rdPos = rdPosvec[n]
        
        if rdPos == 0: #Procura de espaço na célula acima
            if grid[i - 1][j].type in possTypes :
                if i - 1 == -1 :
                    return [grid.shape[0] - 1, j]
                return [i - 1, j]
        elif rdPos == 1: #Procura de espaço na célula à esquerda
            if grid[i][j - 1].type in possTypes:
                if j - 1 == -1 :
                    return [i, grid.shape[1] - 1]
                return [i, j - 1]
        elif rdPos == 2: #Procura de espaço na célula abaixo
            if i + 1 == grid.shape[0]:
                if grid[0][j].type in possTypes:
                    return [0, j]
            else:
                if grid[i + 1][j].type in possTypes:
                    return [i + 1, j]
        else: #Procura de espaço na célula à direita
            if j + 1 == grid.shape[1]:
                if grid[i][0].type in possTypes:
                    return [i, 0]
            else:
                if grid[i][j + 1].type in possTypes:
                    return [i, j + 1]
    
    return -1

#%%

    '''Esta função "joga" o turno correspondente a um determinado animal (herbívoro ou carnívoro). O turno consiste nos vários indíviduos de uma espécie, um de cada vez e de forma aleatória, procurarem comida e, se a encontrarem, alimentarem-se e subirem de nível (e possivelmente reproduzirem-se) ou, se não a encontrarem, diminuirem de nível e, caso não morram, procurarem um novo local para viver
    tudo: tuple com a rede atual e com as listas contendo as posições dos seres vivos de cada espécie
    bichoType: tipo do ser vivo (herbívoro ou carnívoro) para o qual vai ser "jogado" o turno
    Return: tuple atualizado'''

def turn(tudo, bichoType):
    grid = tudo[0]
    plantPos = tudo[1]
    herbPos = tudo[2]
    carnPos = tudo[3]
    emptyPos = tudo[4]
    toRemove = []
    # Dá as configurações à função com base no tipo de Bicho
    if bichoType == 2:
        n = len(herbPos)
        turnPos = herbPos
        dietPos = plantPos
    else: 
        n = len(carnPos)
        turnPos = carnPos
        dietPos = herbPos
    
    for i in range(n):

        iPos = turnPos[i][0]
        jPos = turnPos[i][1]

        foodPos = look4food(grid, iPos, jPos)

        if (foodPos != -1): # caso encontre comida 
            expandFlag = (grid[iPos, jPos].size == 2) #ativa para caso ele já fosse forte antes de comer
            grid[iPos, jPos].grow() 
            grid[foodPos[0]][foodPos[1]].shrink()
            if grid[foodPos[0]][foodPos[1]].type == 0:
                dietPos.remove(foodPos) # apaga a planta que morreu
                emptyPos.append(foodPos)# adiciona ao array de espaços vazios
            if expandFlag:  #caso expanda
                expandPos = look4space(grid, iPos, jPos) #verifica se há sítio para expansão
                if grid[expandPos[0]][expandPos[1]].type == 0:
                    emptyPos.remove(expandPos)
                elif grid[expandPos[0]][expandPos[1]].type == 1:
                    if bichoType == 2:
                        dietPos.remove(expandPos)
                    else:
                        plantPos.remove(expandPos)   
                elif grid[expandPos[0]][expandPos[1]].type == 2:
                    dietPos.remove(expandPos)
                turnPos.append(expandPos)
                grid[expandPos[0]][expandPos[1]] = Bicho(bichoType, 0)  #Cria um novo Bicho do mesmo tipo na nova posição
        else:
            grid[iPos, jPos].shrink()   #Enfraquece por não ter comido
            if grid[iPos, jPos].type == 0:  #Verifica se o Bicho morreu ao enfraquecer
                emptyPos.append([iPos, jPos])
                toRemove.append([iPos, jPos])
            else:
                movePos = look4space(grid, iPos, jPos)  #Procura um espaço válido para mover
                if movePos != -1 :          #Vai mover o Bicho para um espaço válido
                    if grid[movePos[0]][movePos[1]].type == 0:
                        emptyPos.remove(movePos)
                    elif grid[movePos[0]][movePos[1]].type == 1:
                        if bichoType == 2:
                            dietPos.remove(movePos)
                        else:
                            plantPos.remove(movePos)   
                    elif grid[movePos[0]][movePos[1]].type == 2:
                        dietPos.remove(movePos)
                    turnPos.append(movePos)
                    emptyPos.append([iPos, jPos])
                    toRemove.append([iPos, jPos])
                    grid[movePos[0]][movePos[1]] = Bicho(grid[iPos, jPos].type,grid[iPos, jPos].size)
                    grid[iPos, jPos].die()
                    
    for i in range(len(toRemove)): #limpar posições de Bichos que morreram/ moveram
        turnPos.remove(toRemove[i])
        
    return grid, plantPos, herbPos, carnPos, emptyPos   #Retorna a grid e arrays atualizados
    

#%%

    '''Esta função faz uma iteração da rede pela seguinte ordem: herbívoros, carnívoros, plantas. Para os herbívoros e carnívoros, procura comida e se encontrar a população cresce/fica mais saudável, caso contrário fica menos saudável ou pode até mesmo falecer. No final, as plantas crescem todas e nascem em locais de células vazias.
    tudo: tuple com a rede atual e com as listas contendo as posições dos seres vivos de cada espécie'''

def iteration(tudo):
    tudo = turn(tudo, 2)
    tudo = turn(tudo, 3)
    random.shuffle(tudo[2])
    random.shuffle(tudo[3])
    
    for i in range(len(tudo[1])):
        tudo[0][tudo[1][i][0], tudo[1][i][1]].grow()

    for i in range(len(tudo[4])):
        tudo[0][tudo[4][i][0], tudo[4][i][1]].changeType(1)
        tudo[1].append(tudo[4][i])
    tudo[4].clear()

#%%

    '''Esta função conta, para um determinado ser vivo, o número de indivíduos de cada nível.
    tudo: tuple com a rede atual e com as listas contendo as posições dos seres vivos de cada espécie
    bichoType: tipo do ser vivo (herbívoro ou carnívoro) para o qual vai ser "jogado" o turno
    Return: array com o número de indivíduos de cada nível para uma determinada espécie'''

def getLevel(tudo, bichoType):
    nLevel = np.zeros(3, dtype = float)
    
    for j in range(len(tudo[bichoType])):
        if tudo[0][tudo[bichoType][j][0], tudo[bichoType][j][1]].size == 0:
            nLevel[0] += 1
        elif tudo[0][tudo[bichoType][j][0], tudo[bichoType][j][1]].size == 1:
            nLevel[1] += 1
        else:
            nLevel[2] += 1
    nLevel = nLevel/len(tudo[bichoType]) * 100
    
    return nLevel
    
#%%

    '''Desenha os gráficos relativos à evolução das simulações.
    nPlant: array com o número de plantas ao longo da simulação com carnívoros
    nHerb: array com o número de herbívoros ao longo da simulação com carnívoros
    nCarn: array com o número de carnívoros ao longo da simulação
    nPlant2: array com o número de plantas ao longo da simulação sem carnívoros
    nHerb2: array com o número de herbívoros ao longo da simulação sem carnívoros
    hPlant: array com a distribuição dos níveis de plantas ao longo da simulação com carnívoros
    hHerb: array com a distribuição dos níveis de herbívoros ao longo da simulação com carnívoros
    hCarn: array com a distribuição dos níveis de carnívoros ao longo da simulação
    hPlant2: array com a distribuição dos níveis de plantas ao longo da simulação sem carnívoros
    hHerb2: array com a distribuição dos níveis de herbívoros ao longo da simulação sem carnívoros'''

def drawGraphs(sim1, sim2):
    plt.style.use('dark_background')
    fig = plt.figure()
    axS = fig.add_subplot(4, 2, 1)
    axS.plot(sim1[5], 'b-', label = "Plantas")
    axS.plot(sim1[6], 'g-', label = "Herbívoros")
    axS.plot(sim1[7], 'r-', label = "Carnívoros")
    axS.set_title('Simulação c/ Carnívoros')
    axS.set_ylabel('%')
    axS.set_xlabel('Número da Iteração')
    plt.legend()
    axS2 = fig.add_subplot(4, 2, 2)
    axS2.plot(sim2[5], 'b-', label = "Plantas")
    axS2.plot(sim2[6], 'g-', label = "Herbívoros")
    axS2.set_title('Simulação s/ Carnívoros')
    axS2.set_ylabel('%')
    axS2.set_xlabel('Número da Iteração')
    plt.legend()
    axS3 = fig.add_subplot(4, 2, 3)
    axS3.plot(sim1[8][:, 0], 'b-', label = "Fraco")
    axS3.plot(sim1[8][:, 1], 'g-', label = "Médio")
    axS3.plot(sim1[8][:, 2], 'r-', label = "Forte")
    axS3.set_title('População de Plantas por Nível')
    axS3.set_ylabel('%')
    axS3.set_xlabel('Número da Iteração')
    plt.legend()
    axS4 = fig.add_subplot(4, 2, 4)
    axS4.plot(sim2[8][:, 0], 'b-', label = "Fraco")
    axS4.plot(sim2[8][:, 1], 'g-', label = "Médio")
    axS4.plot(sim2[8][:, 2], 'r-', label = "Forte")
    axS4.set_title('População de Plantas por Nível')
    axS4.set_ylabel('%')
    axS4.set_xlabel('Número da Iteração')
    plt.legend()
    axS5 = fig.add_subplot(4, 2, 5)
    axS5.plot(sim1[9][:, 0], 'b-', label = "Fraco")
    axS5.plot(sim1[9][:, 1], 'g-', label = "Médio")
    axS5.plot(sim1[9][:, 2], 'r-', label = "Forte")
    axS5.set_title('População de Herbívoros por Nível')
    axS5.set_ylabel('%')
    axS5.set_xlabel('Número da Iteração')
    plt.legend()
    axS6 = fig.add_subplot(4, 2, 6)
    axS6.plot(sim2[9][:, 0], 'b-', label = "Fraco")
    axS6.plot(sim2[9][:, 1], 'g-', label = "Médio")
    axS6.plot(sim2[9][:, 2], 'r-', label = "Forte")
    axS6.set_title('População de Herbívoros por Nível')
    axS6.set_ylabel('%')
    axS6.set_xlabel('Número da Iteração')
    plt.legend()
    axS7 = fig.add_subplot(4, 2, 7)
    axS7.plot(sim1[10][:, 0], 'b-', label = "Fraco")
    axS7.plot(sim1[10][:, 1], 'g-', label = "Médio")
    axS7.plot(sim1[10][:, 2], 'r-', label = "Forte")
    axS7.set_title('População de Carnívoros por Nível')
    axS7.set_ylabel('%')
    axS7.set_xlabel('Número da Iteração')
    plt.legend()
    fig.set_size_inches(12, 6)
    
#%%

def stats(tudo, iteration, nx, ny):
    tudo[11].append(copy.deepcopy(tudo[0]))
    tudo[5][iteration] = len(tudo[1])/(nx * ny) * 100
    tudo[6][iteration] = len(tudo[2])/(nx * ny) * 100
    tudo[7][iteration] = len(tudo[3])/(nx * ny) * 100
    tudo[8][iteration] = getLevel(tudo, 1)
    tudo[9][iteration] = getLevel(tudo, 2)
    tudo[10][iteration] = getLevel(tudo, 3)
    
#%%

def ecosystems(tudo, nx, ny, nIterations):
    gridInt = np.zeros((nx, ny), dtype = float)
    
    for i in range(len(tudo[11])):
        for j in range(nx):
            for k in range(ny):
                gridInt[j, k] = tudo[11][i][j, k].type
        tudo[11].append(copy.deepcopy(gridInt))
    del tudo[11][0:nIterations + 1]

#%%

    '''É a função principal. Esta função inicia as estruturas de dados necessárias à execução das simulações (com e sem carnívoros) e chama as funções que atualizam os estados das mesmas, criando cópias das redes após cada iteração. Para além disso, calcula o necessário para posteriormente apresentar nos respetivos gráficos dados relacionados com a evolução das redes de forma a poder comparar as duas simulações.
    nx: número de linhas da rede
    ny: número de colunas da rede
    nIterations: número de iterações a ser executadas por simulação
    Return: tuples com as informações relativas às duas simulações e listas com cópias da rede após cada iteração'''

def circleOfLife(nx, ny, nIterations, p1, p2, p3):
    #Simulação com carnívoros
    tudo = initGrid(nx, ny, p1, p2, p3, nIterations)
    stats(tudo, 0, nx, ny)
            
    for i in range(nIterations):
        iteration(tudo)
        stats(tudo, i + 1, nx, ny)
    
    ecosystems(tudo, nx, ny, nIterations)        
    
    return tudo

#%%


def simulations(nx, ny, nIterations):
    
    tudo = circleOfLife(nx, ny, nIterations, 9, 3, 1)
    tudo2 = circleOfLife(nx, ny, nIterations, 9, 3, 0)
    
    drawGraphs(tudo, tudo2)
    
    return tudo, tudo2

#%%

tudo, tudo2 = simulations(50, 50, 500)

#%%

'''Esta parte do código é a responsável pela animação do estado dos ecossistemas ao longo das simulações.'''

fig1 = plt.figure()
fig1.suptitle('1-Planta         2-Herbívoro         3-Carnívoro',fontsize='25')
ax1 = fig1.add_subplot(1, 2, 1)
ims = []
for i in range(len(tudo[11])):
    im = ax1.imshow(tudo[11][i],cmap='summer', animated = True, aspect = 'auto', vmin = 1, vmax = 3)
    if i == 0:
        ax1.imshow(tudo[11][i],cmap='summer', aspect = 'auto', vmin = 1, vmax = 3)
    ims.append([im])
ani = animation.ArtistAnimation(fig1, ims, interval = 100, blit = True, repeat_delay = 1000)
plt.colorbar(im)

ax2 = fig1.add_subplot(1, 2, 2)
ims2 = []
for i in range(len(tudo2[11])):
    im2 = ax2.imshow(tudo2[11][i],cmap='summer', animated = True, aspect = 'auto', vmin = 1, vmax = 3)
    if i == 0:
        ax2.imshow(tudo2[11][i],cmap='summer', aspect = 'auto', vmin = 1, vmax = 3)
    ims2.append([im2])
ani2 = animation.ArtistAnimation(fig1, ims2, interval = 100, blit = True, repeat_delay = 1000)
plt.colorbar(im2)

fig1.set_size_inches(12, 6)
plt.show()

et = time.time()

print(et - st)