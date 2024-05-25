#!/usr/bin/env python
# coding: utf-8

# ## Bibliotecas utilizadas

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# ## Extração dos dados

# In[2]:


def extrair_dados(arquivo):

    arq = open(arquivo)
    conteudo = arq.readlines()
    arq.close()
    
    index = conteudo.index('NODE_COORD_SECTION\n')
    eof = conteudo.index('EOF\n')

    dados = conteudo[index+1:eof]
    
    return dados


# ## Armazenamento das caracteristicas do ponto

# In[3]:


class Ponto:
    
    def __init__(self, id_, x_, y_):
        
        self.id = id_
        self.x = x_
        self.y = y_


# In[4]:


def gerar_pontos(dados):

    pontos = []

    for dado in dados:

        dado = dado.replace("  ", " ")
        dado = dado.strip().split(" ")
        
        id_ponto = int(dado[0]) - 1
        coord_x = float(dado[1])
        coord_y = float(dado[2].replace("\n", ""))

        pontos.append(Ponto(id_ponto, coord_x, coord_y))

    return pontos


# ## Matriz de distâncias

# In[5]:


def calcular_distancia(p1, p2):
    
    delta_x = p1.x - p2.x
    delta_y = p1.y - p2.y
    
    distancia = np.sqrt(delta_x**2 + delta_y**2)
    
    return distancia


# In[6]:


def gerar_matriz_distancias(pontos):
    
    num_pontos = len(pontos)
    
    distancias = np.zeros((num_pontos, num_pontos))
    
    
    for i in range(num_pontos):
        for k in range(1, num_pontos):
            
            p1 = pontos[i]
            p2 = pontos[k]
            
            indice_1 = p1.id
            indice_2 = p2.id
            
            distancia = calcular_distancia(p1, p2)
            
            distancias[indice_1, indice_2] = distancia
            distancias[indice_2, indice_1] = distancia
    

    return distancias


# In[20]:


def calcular_distancia_caminho(caminho, matriz_distancias):
    
    distancia_total = 0
    
    for i in range(len(matriz_distancias)-1):
        
        distancia_total += matriz_distancias[caminho[i], caminho[i+1]]
    
    return distancia_total


# ## Heurística construtiva - solução inicial

# In[21]:


def insercao_mais_proxima(distancias, pontos):
    
    num_pontos = len(pontos)
    visitados = [False]*num_pontos
    
    visitados[0] = True
    ponto_mais_proximo = np.argmin(distancias[0,1:])
    visitados[ponto_mais_proximo] = True
    
    caminho = [0, ponto_mais_proximo]
    
    while len(caminho) < len(pontos):
        
        menor_distancia = float('inf')
        ponto_minimo = -1
        ponto_de_insercao = -1
        
        for i in range(len(caminho)):
            for j in range(num_pontos):
                if i == j:
                    continue
                
                if not visitados[j]:
                    distancia_atual = distancias[caminho[i], j]
                       
                    if distancia_atual < menor_distancia:
                        menor_distancia = distancia_atual
                        ponto_minimo = j
                        ponto_de_insercao = i
                    
        caminho.insert(ponto_de_insercao+1, ponto_minimo)
        visitados[ponto_minimo] = True
    
    caminho.append(0)
    
    
    distancia_total = calcular_distancia_caminho(caminho, distancias)

    return caminho, distancia_total


# ## Heurística VND

# In[28]:


def dois_opt(caminho, matriz_distancias):
    
    n = len(caminho)
    melhor_caminho = caminho.copy()
    custo_melhor_caminho = calcular_distancia_caminho(caminho, matriz_distancias)
    melhorou = True

    while melhorou:
        melhorou = False

        for i in range(1, n - 2):
            for j in range(i + 1, n):
                novo_caminho = caminho[:i] + list(reversed(caminho[i:j])) + caminho[j:]
                custo_novo_caminho = calcular_distancia_caminho(novo_caminho, matriz_distancias)

                if custo_novo_caminho < custo_melhor_caminho:
                    melhor_caminho = novo_caminho
                    custo_melhor_caminho = custo_novo_caminho
                    melhorou = True

        caminho = melhor_caminho

    return melhor_caminho, custo_melhor_caminho


# ## Mostrar resultados

# In[29]:


def exibir_rota(pontos, caminho, distancia_total):

    plt.figure(figsize = (16,10))

    for ponto in pontos:

        plt.scatter(ponto.x, ponto.y)

    for i in range(len(caminho)-1):

        plt.plot([pontos[caminho[i]].x, pontos[caminho[i+1]].x],[pontos[caminho[i]].y, pontos[caminho[i+1]].y])


    plt.xlabel("Coordenada x", fontsize = 16)
    plt.ylabel("Coordenada y", fontsize = 16)
    plt.title("Caminho entre os pontos\nDistancia total: " + str(round(distancia_total,2)), fontsize = 22)
    plt.show()


# In[ ]:





# ## Execução

# In[39]:


def executar(nome_arquivo):
    
    dados = extrair_dados(nome_arquivo)
    pontos = gerar_pontos(dados)
    distancias = gerar_matriz_distancias(pontos)
    caminho, distancia_total = insercao_mais_proxima(distancias, pontos)
    caminho_novo, distancia_nova = dois_opt(caminho, distancias)
    
    print("Instancia: " + nome_arquivo)
    print("Custo total: " + str(distancia_nova))
    
    #exibir_rota(pontos, caminho, distancia_total)


# In[40]:


instancias = ['att48.tsp', 'berlin52.tsp', 'kroA100.tsp', 'kroA150.tsp', 'kroA200.tsp', 
              'kroB100.tsp', 'kroB150.tsp', 'kroB200.tsp', 'kroC100.tsp', 'kroD100.tsp', 
              'kroE100.tsp', 'lin105.tsp', 'pr107.tsp', 'pr124.tsp', 'pr136.tsp', 
              'pr144.tsp', 'pr152.tsp', 'pr76.tsp', 'rat195.tsp', 'rat99.tsp', 'st70.tsp']


# In[41]:


for instancia in instancias:
    
    executar(instancia)


# In[ ]:




