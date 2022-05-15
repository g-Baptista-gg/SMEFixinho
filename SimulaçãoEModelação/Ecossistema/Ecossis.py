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

#%matplotlib qt
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
        
#%%

    '''Inicia a estrutura de dados que contém a informação relacionada com a evolução da rede
    nx: número de linhas da rede
    ny: número de colunas da rede'''

def initGrid(nx, ny):
    grid = np.zeros((nx, ny), dtype = object) #Inicia a rede
    
    herbPos = [] #Cria uma lista para as posições dos herbívoros da rede
    carnPos = [] #Cria uma lista para as posições dos carnívoros da rede
    plantPos = [] #Cria uma lista para as posições das plantas da rede
    
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
            elif rd < (p1 + p2)/(p1 + p2 + p3):
                grid[i][j] = Bicho(2, size)
                herbPos.append([i, j])
            else:
                grid[i][j] = Bicho(3, size)
                carnPos.append([i, j])
    
    #Ordenação aleatória dos vetores posição de cada uma das listas
    random.shuffle(herbPos)
    random.shuffle(carnPos)
    random.shuffle(plantPos)
    
    return grid, herbPos, carnPos, plantPos

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
        rdPos=rdPosvec[n]
        
        if rdPos == 0: #Procura de alimento na célula acima
            if grid[i - 1][j].type == (grid[i][j].type - 1):
                return [i - 1, j]
        elif rdPos == 1: #Procura de alimento na célula à esquerda
            if grid[i][j - 1].type == (grid[i][j].type - 1):
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
def look4space(grid,i,j):
    #ordena aleatoriamente as células onde se vai procurar espaço para expansão
    rdPosvec = [0, 1, 2, 3]
    random.shuffle(rdPosvec)
    
    for n in range(4):
        rdPos=rdPosvec[n]
        
        if rdPos == 0: #Procura de espaço na célula acima
            if (grid[i - 1][j].type == (grid[i][j].type - 1)) or grid[i - 1][j].type==0 :
                return [i - 1, j]
        elif rdPos == 1: #Procura de espaço na célula à esquerda
            if (grid[i][j - 1].type == (grid[i][j].type - 1)) or grid[i][j - 1].type==0:
                return [i, j - 1]
        elif rdPos == 2: #Procura de espaço na célula abaixo
            if i + 1 == grid.shape[0]:
                if (grid[0][j].type == (grid[i][j].type - 1)) or grid[0][j].type==0:
                    return [0, j]
            else:
                if (grid[i + 1][j].type == (grid[i][j].type - 1)) or grid[i+1][j].type==0:
                    return [i + 1, j]
        else: #Procura de espaço na célula à direita
            if j + 1 == grid.shape[1]:
                if (grid[i][0].type == (grid[i][j].type - 1)) or grid[i][0].type==0:
                    return [i, 0]
            else:
                if (grid[i][j + 1].type == (grid[i][j].type - 1)) or grid[i][j+1].type==0:
                    return [i, j + 1]
    
    return -1

#%%
    '''Esta função procura espaço vazio para mudança de posição para um determinado ser vivo nos primeiros vizinhos de von Neumann. Note-se que o alimento de um determinado tipo de ser vivo corresponde a (tipo - 1)
    grid: rede do ecossistema
    i: linha onde se encontra o ser vivo
    j: coluna onde se encontra o ser vivo'''
def look4empty(grid,i,j):
    #ordena aleatoriamente as células onde se vai procurar espaço para expansão
    rdPosvec = [0, 1, 2, 3]
    random.shuffle(rdPosvec)
    
    for n in range(4):
        rdPos=rdPosvec[n]
        
        if rdPos == 0: #Procura de espaço na célula acima
            if grid[i - 1][j].type==0 :
                return [i - 1, j]
        elif rdPos == 1: #Procura de espaço na célula à esquerda
            if grid[i][j - 1].type==0:
                return [i, j - 1]
        elif rdPos == 2: #Procura de espaço na célula abaixo
            if i + 1 == grid.shape[0]:
                if grid[0][j].type==0:
                    return [0, j]
            else:
                if grid[i+1][j].type==0:
                    return [i + 1, j]
        else: #Procura de espaço na célula à direita
            if j + 1 == grid.shape[1]:
                if grid[i][0].type==0:
                    return [i, 0]
            else:
                if grid[i][j+1].type==0:
                    return [i, j + 1]
    
    return -1

#%%

    '''Esta função faz uma iteração da rede pela seguinte ordem: herbívoros, carnívoros, plantas. Para os herbívoros e carnívoros, procura comida e se encontrar a população cresce/fica mais saudável, caso contrário fica menos saudável ou pode até mesmo falecer. No final, as plantas crescem todas e nascem em locais de células vazias.
    gridInfo: informação relacionada com a rede (rede e matrizes com as posições de cada tipo de ser vivo)
    nx: número de linhas da rede
    ny: número de colunas da rede
    
    FUNÇÃO NÃO TERMINADA!! FALTA IR ALTERANDO AS MATRIZES COM AS POSIÇÕES DOS DIFERENTES TIPOS DE SERES VIVOS E ATUALIZAR A FUNÇÃO look4food PARA SER MAIS GERAL'''

# =============================================================================
# def iteration(gridInfo, nx, ny):
#     
#     for i in range(len(gridInfo[1])):
#         foodPos = look4food(gridInfo[0], gridInfo[1][i, 0], gridInfo[1][i, 1])
#         if foodPos != 'No Food':
#             gridInfo[0][foodPos[0], foodPos[1]].shrink()
#             if gridInfo[0][gridInfo[1][i, 0], gridInfo[1][i, 1]].size < 2:
#                 gridInfo[0][gridInfo[1][i, 0], gridInfo[1][i, 1]].grow()
#             else:
#                 newHerb = look4food(gridInfo[0], gridInfo[1][i, 0], gridInfo[1][i, 1])
#                 gridInfo[0][newHerb[0], newHerb[1]].changeType(2)
#         else:
#             gridInfo[0][gridInfo[1][i, 0], gridInfo[1][i, 1]].shrink()
#             if gridInfo[0][gridInfo[1][i, 0], gridInfo[1][i, 1]].type == 0:
#                 newPos = look4food(gridInfo[0], gridInfo[1][i, 0], gridInfo[1][i, 1])
#                 if newPos != 'No Food':
#                     gridInfo[0][gridInfo[1][i, 0], gridInfo[1][i, 1]].changeType(0)
#                     gridInfo[0][newPos[0], newPos[1]].changeType(2)
#                     
#     for i in range(len(gridInfo[2])):
#         foodPos = look4food(gridInfo[0], gridInfo[2][i, 0], gridInfo[2][i, 1])
#         if foodPos != 'No Food':
#             gridInfo[0][foodPos[0], foodPos[1]].shrink()
#             if gridInfo[0][gridInfo[2][i, 0], gridInfo[2][i, 1]].size < 2:
#                 gridInfo[0][gridInfo[2][i, 0], gridInfo[2][i, 1]].grow()
#             else:
#                 newCarn = look4food(gridInfo[0], gridInfo[2][i, 0], gridInfo[2][i, 1])
#                 gridInfo[0][newCarn[0], newCarn[1]].changeType(3)
#         else:
#             gridInfo[0][gridInfo[2][i, 0], gridInfo[2][i, 1]].shrink()
#             if gridInfo[0][gridInfo[2][i, 0], gridInfo[2][i, 1]].type == 0:
#                 newPos = look4food(gridInfo[0], gridInfo[2][i, 0], gridInfo[2][i, 1])
#                 if newPos != 'No Food':
#                     gridInfo[0][gridInfo[2][i, 0], gridInfo[2][i, 1]].changeType(0)
#                     gridInfo[0][newPos[0], newPos[1]].changeType(3)
#                     
#     for i in range(len(gridInfo[3])):
#         gridInfo[0][gridInfo[3][i, 0], gridInfo[3][i, 1]].grow()
#         
#     for i in range(nx):
#         for j in range(ny):
#             if gridInfo[0][i, j].type == 0:
#                 gridInfo[0][i, j].changeType(1)
# 
# =============================================================================
#%%

#FUNÇAO PRINCIPAL CHAMA-SE CIRCLE OF LIFE
tudo=initGrid(25,25)
grid=tudo[0]
plantPos=tudo[3]
herbPos=tudo[1]
carnPos=tudo[2]
print(look4food(grid,0,0))


