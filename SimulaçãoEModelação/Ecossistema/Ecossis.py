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

#%% Imports
%clear
%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
import random

#%%

'''A classe Bicho tem como objetivo conter toda a informação necessária em relação a um determinado ponto da rede, como o tipo de ser vivo e o seu respetivo nível
    changeType: muda o tipo de ser vivo do ponto da rede
    grow: faz o ser vivo aumentar de nível se este ainda não estiver no nível máximo (2)
    shrink: diminui o nível do ser vivo; se o nível deste for mínimo (0), o tipo de ser vivo passa a 0 (ou seja, passa a ser uma célula sem ser vivo)'''

class Bicho:
    def  __init__(self, sType, size):
        self.type = sType #Tipos possíveis: Vazio(0), Planta(1), Herbívoro(2), Carnívoro(3)
        self.size = size  #Níveis possíveis: Fraco(0), Médio(1), Forte(2)
    
    def __str__(self):
        return 'Hallo'
    
    def changeType(self, newType):
        self.type = newType
        self.size = 0
    
    def grow(self):
        if self.size < 2:
            self.size += 1
    
    def shrink(self):
        if self.size > 0:
            self.size -= 1
        else:
            self.type = 0
    def die(self):
        self.type = 0
        
#%%

    '''Inicia a estrutura de dados que contém a informação relacionada com a evolução da rede
    nx: número de linhas da rede
    ny: número de colunas da rede'''

def initGrid(nx, ny):
    grid = np.zeros((nx, ny), dtype = object) #Inicia a rede
    
    herbPos = [] #Cria uma lista para as posições dos herbívoros da rede
    carnPos = [] #Cria uma lista para as posições dos carnívoros da rede
    plantPos = [] #Cria uma lista para as posições das plantas da rede
    emptyPos=[]
    
    p1 = 9 #Peso relativo de plantas na inicialização da rede
    p2 = 3 #Peso relativo de herbívoros na inicialização da rede
    p3 = 1 #Peso relativo de carnívoros na inicialização da rede
    
    #Preenchimento da rede
    for i in range(nx):
        for j in range(ny):
            rd = np.random.rand()
            size = np.random.randint(2)
            if rd <= p1/(p1 + p2 + p3):
                grid[i][j] = Bicho(1, size)
                plantPos.append([i,j])
            elif rd <= (p1 + p2)/(p1 + p2 + p3):
                grid[i][j] = Bicho(2, size)
                herbPos.append([i, j])
            else:
                grid[i][j] = Bicho(3, size)
                carnPos.append([i, j])
    
    #Ordenação aleatória dos vetores posição de cada uma das listas
    #random.shuffle(herbPos)
    #random.shuffle(carnPos)
    #random.shuffle(plantPos)
    
    return grid, herbPos, carnPos, plantPos, emptyPos

#%%

    '''Esta função procura alimento para um determinado ser vivo nos primeiros vizinhos de von Neumann. Note-se que o alimento de um determinado tipo de ser vivo corresponde a (tipo - 1)
    grid: rede do ecossistema
    i: linha onde se encontra o ser vivo
    j: coluna onde se encontra o ser vivo'''

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
    '''Esta função procura espaço para expansão para um determinado ser vivo nos primeiros vizinhos de von Neumann. Note-se que o alimento de um determinado tipo de ser vivo corresponde a (tipo - 1)
    grid: rede do ecossistema
    i: linha onde se encontra o ser vivo
    j: coluna onde se encontra o ser vivo'''
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

def turn(tudo, bichoType):
    grid = tudo[0]
    herbPos = tudo[1]
    carnPos = tudo[2]
    plantPos = tudo[3]
    emptyPos = tudo[4]
    toRemove = []
    
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

        if (foodPos != -1): # caso o bicho coma
            expandFlag = (grid[iPos, jPos].size == 2) #ativa para caso ele já fosse forte antes de comer
            grid[iPos, jPos].grow()
            grid[foodPos[0]][foodPos[1]].shrink()
            if grid[foodPos[0]][foodPos[1]].type == 0:
                dietPos.remove(foodPos) # apaga a planta que morreu
                emptyPos.append(foodPos)
            if expandFlag:
                expandPos = look4space(grid, iPos, jPos)
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
                grid[expandPos[0]][expandPos[1]] = Bicho(bichoType, 0)
        else:
            grid[iPos, jPos].shrink()
            if grid[iPos, jPos].type == 0:
                emptyPos.append([iPos, jPos])
                toRemove.append([iPos, jPos])
            else:
                movePos = look4space(grid, iPos, jPos)
                if movePos != -1 :
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
                    
    for i in range(len(toRemove)): #limpar posições de antigos herbívoros
        turnPos.remove(toRemove[i])
        
    if bichoType == 2:
        
        herbPos = turnPos
        
        plantPos = dietPos
    else: 
        carnPos = turnPos
        herbPos = dietPos
        
    return grid, herbPos, carnPos, plantPos, emptyPos
    

#%%

    '''Esta função faz uma iteração da rede pela seguinte ordem: herbívoros, carnívoros, plantas. Para os herbívoros e carnívoros, procura comida e se encontrar a população cresce/fica mais saudável, caso contrário fica menos saudável ou pode até mesmo falecer. No final, as plantas crescem todas e nascem em locais de células vazias.
    gridInfo: informação relacionada com a rede (rede e matrizes com as posições de cada tipo de ser vivo)
    nx: número de linhas da rede
    ny: número de colunas da rede
    
    FUNÇÃO NÃO TERMINADA!! FALTA IR ALTERANDO AS MATRIZES COM AS POSIÇÕES DOS DIFERENTES TIPOS DE SERES VIVOS E ATUALIZAR A FUNÇÃO look4food PARA SER MAIS GERAL'''

def iteration(tudo):
    tudo = turn(tudo, 2)
    tudo = turn(tudo, 3)
    
    for i in range(len(tudo[3])):
        tudo[0][tudo[3][i][0], tudo[3][i][1]].grow()

    for i in range(len(tudo[4])):
        tudo[0][tudo[4][i][0], tudo[4][i][1]].changeType(1)
        tudo[3].append(tudo[4][i])
    tudo[4].clear()
    
#%%

def circleOfLife(nx, ny, nIterations):
    tudo = initGrid(25, 25)
    nPlant = np.zeros(nIterations + 1, dtype = int) 
    nHerb = np.zeros(nIterations + 1, dtype = int) 
    nCarn = np.zeros(nIterations + 1, dtype = int)
    
    nPlant[0] = len(tudo[3])
    nHerb[0] = len(tudo[1])
    nCarn[0] = len(tudo[2])
    
    for i in range(nIterations):
        iteration(tudo)
        nPlant[i + 1] = len(tudo[3])
        nHerb[i + 1] = len(tudo[1])
        nCarn[i + 1] = len(tudo[2])
        
    fig = plt.figure()
    axS = fig.add_subplot(1, 2, 1)
    axS.plot(nPlant, 'b-', label = "Plantas")
    axS.plot(nHerb, 'g-', label = "Herbívoros")
    axS.plot(nCarn, 'r-', label = "Carnívoros")
    plt.legend()
    fig.set_size_inches(12, 6)
        
    return tudo

#%%

tudo = circleOfLife(50, 50, 500)

