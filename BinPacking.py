## Caminhada Aleatoria ##

import random
import time

## Variaveis ##
C = 6                                    # Capacidade de cada caixa
N = 10                                   # Itens a serem organizados
W = [2, 3, 5, 3, 1, 2, 5, 4, 3, 2]       # Conjunto de peso de cada item, sendo que o indice representante de cada item e o valor seu peso
Bins = []                                # Conjunto solução de itens, sendo o indice representante de cada item e o valor a sua caixa

## Auxiliares ##

# Modificacao fazendo um swap com itens distintos
def modificacao1(solucao):
    # Seleciona itens aleatorios para serem modificados
    item1 = random.randint(0, (N - 1))
    item2 = random.randint(0, (N - 1))

    # Verificar se a mudança é possível
    # Verifica o peso de cada nível
    peso1 = 0
    peso2 = 0
    for i in range(len(solucao)):
        if (solucao[i] == solucao[item1]):
            peso1 += W[i]
        if (solucao[i] == solucao[item2]):
            peso2 += W[i]

    # Verifica se os niveis poderiam abrigar os outros itens
    if (((peso1 - W[item1]) + W[item2]) <= C) and (((peso2 - W[item2]) + W[item1]) <= C):
        aux = solucao[item1]
        solucao[item1] = solucao[item2]
        solucao[item2] = aux

    return solucao

# Modificacao tentando encaixar 1 item em outro bin
def modificacao2(solucao):
    # Seleciona um item aleatorio para ser modificado
    item = random.randint(0, (N - 1))

    # Percorre os bins verificando se esse item cabe em algum outro
    for bin in range(max(solucao) + 1):
        # Verifica o peso do bin
        peso = 0
        for i in range(len(solucao)):
            if (solucao[i] == bin):
                peso += W[i]

        # Se o item couber nesse bin
        if ((peso + W[item]) <= C):
            solucao[item] = bin

            # Tenta reorganizar os bins para caso algum tenha ficado vazio
            reorganizarBins(solucao)

            break

    return solucao    

# Modificacao tentando desmontar bin e distribuir os itens em outros
def modificacao3(solucao):
    # Seleciona um bin aleatoriamente
    bin = random.randint(0, max(solucao))

    # Percorre os itens desse bin
    for item in range(len(solucao)):
        if (solucao[i] == bin):
        # Percorre os outros bins verificando se esse item cabe em algum outro
            if (bin != bin):
                for bin in range(max(solucao) + 1):
                    # Verifica o peso do bin
                    peso = 0
                    for i in range(len(solucao)):
                        if (solucao[i] == bin):
                            peso += W[i]

                    # Se o item couber nesse bin
                    if ((peso + W[item]) <= C):
                        solucao[item] = bin

                        # Tenta reorganizar os bins para caso algum tenha ficado vazio
                        reorganizarBins(solucao)

                        break

    return solucao 

# Essa funcao percorre os bins e verificar se ha algum "furo", se temos o bin 1 e 3 mas nao temos o 2, por exemplo
def reorganizarBins(solucao):
    # Percorre a solucao
    for i in range(len(solucao)):
        # Se o bin anterior nao estiver na solucao
        if (solucao[i] != 0):
            if ((solucao[i] - 1) not in solucao):
                aux = solucao[i]
                # Percorre a solucao mudando todos para o nivel que antes estava vazio
                for n in range(len(solucao)):
                    if (solucao[n] == aux):
                        solucao[n] = solucao[n] - 1

    return solucao

## Heuristicas ##

def heuristica1():
    for i in range(N):
        Bins.append(-1)

    while (-1 in Bins):
        # Gera um inteiro aleatorio (um item a ser alocado)
        item = random.randint(0, (N - 1))
        
        # Verifica se esse item ainda nao foi alocado
        if (Bins[item] == -1):
            maximo = max(Bins)
            if maximo < 1:
                maximo = 1

            for nivel in range(maximo + 1):
                # Calcula o peso do nivel
                pesoNivel = 0

                for i in range(N):
                    if (Bins[i]) == (nivel):
                        pesoNivel += W[i]

                # Se o item couber nesse nivel
                if (pesoNivel + W[item] <= C):
                    Bins[item] = nivel
                    break
                # Se não couber no ultimo nivel, cria outro nivel para esse item
                elif ((nivel) == max(Bins)):
                    Bins[item] = nivel + 1
    return Bins

## Aleatorio ##

def solucaoAleatoria():
    for i in range(N):
        Bins.append(-1)

    while (-1 in Bins):
        # Gera um inteiro aleatorio (um item a ser alocado)
        item = random.randint(0, (N - 1))
        
        # Verifica se esse item ainda nao foi alocado
        if (Bins[item] == -1):
            maximo = max(Bins)
            if maximo < 1:
                maximo = 1

            # Gera um nivel aleatorio entre os que ja existem e 1 a mais
            nivel = random.randint(0, maximo + 1)

            # Calcula o peso do nivel
            pesoNivel = 0

            for i in range(N):
                if (Bins[i]) == (nivel):
                    pesoNivel += W[i]

            # Se o item couber nesse nivel
            if (pesoNivel + W[item] <= C):
                Bins[item] = nivel
            # Se não couber no ultimo nivel, cria outro nivel para esse item
            elif ((nivel) == max(Bins)):
                Bins[item] = nivel + 1

    return Bins

def caminhadaAleatoria():
    # Gera uma solucao
    solucao = solucaoAleatoria()
    solucaoMelhor = []
    comparativo = []

    for i in range(len(solucao)):      
        solucaoMelhor.append(solucao[i])
        comparativo.append(solucao[i])

    cont = 0

    timeEnd = time.time() + 30
    timeCount = 0
    timeSleep = 1

    # Enquanto criterio de parada nao for satisfeito
    # while(cont < 1000):
    while time.time() < timeEnd:
        time.sleep(timeSleep)
        timeCount += timeSleep

        #Gera uma modificacao na solucao
        solucao = modificacao2(solucao)

        # Verifica se a qualidade da solucao nova é melhor que a melhor solucao que temos
        # O número de bins se mantem igual, entao medimos o espaco livre de cada solucao
        if max(solucao) < max(solucaoMelhor):
            solucaoMelhor = solucao
        elif max(solucao) == max(solucaoMelhor):            
            pesoLivreSol1 = 0
            pesoLivreSol2 = 0
            for nivel in range(max(solucao) + 1):
                # Calcula o peso do nivel
                pesoNivelSol1 = 0
                pesoNivelSol2 = 0

                for item in range(len(solucao)):
                    if (solucao[item]) == (nivel):
                        pesoNivelSol1 += W[item]

                    if (solucaoMelhor[item]) == (nivel):
                        pesoNivelSol2 += W[item]

                # Adiciona o espaco que sobra para nossa variavel de comparacao
                pesoLivreSol1 += (C - pesoNivelSol1)
                pesoLivreSol2 += (C - pesoNivelSol2)
            # Se a solucao atual tem um peso livre maior que a melhor solucao, ela se torna a nova melhor solucao
            if (pesoLivreSol1 < pesoLivreSol2):
                solucaoMelhor = solucao                   

        cont += 1

    return comparativo, solucao, solucaoMelhor

## Instancias ##

# Percorrendo nossas 20 instancias
for i in range(1, 21):
    # Abre a instancia
    file = open("instances/instancia" + str(i) + ".txt")

    # Percorrendo o arquivo, ignoramos as linhas que começam com //
    linhas = file.readlines()

    N = int(linhas[1].split("\n")[0])             # Itens a serem organizados
    C = int(linhas[3].split("\n")[0])             # Capacidade de cada caixa
    W = []                                        # Conjunto de pesos de cada item
    Bins = []                                     # Conjunto solucao

    # Pesos dos itens
    for ls in range(len(linhas)):
        if (ls > 6):
            W.append(int(linhas[ls].split("\n")[0]))

    file.close()

    # solucao = heuristica1()
    # solucao = solucaoAleatoria()
    comparativo, solucao, melhorDeTodas = caminhadaAleatoria()

    print("Instancia " + str(i) + ": " + str(max(solucao)))

## Resultados ##

# solucao = heuristica1()
# solucao = solucaoAleatoria()

# for i in range(len(solucao)):
#     print("Item " + str(i) + ": " + str(solucao[i]))

# for nivel in range(max(solucao) + 1):
#     pesoNivel = 0

#     for i in range(N):
#         if (solucao[i]) == (nivel):
#             pesoNivel += W[i]

#     print("Peso do nivel " + str(nivel) + ": " + str(pesoNivel))

# comparativo, solucao, melhorDeTodas = caminhadaAleatoria()
# print("----------------- Inicial -----------------")

# for i in range(len(comparativo)):
#     print("Item " + str(i) + ": " + str(comparativo[i]))

# for nivel in range(max(comparativo) + 1):
#     pesoNivel = 0

#     for i in range(N):
#         if (comparativo[i]) == (nivel):
#             pesoNivel += W[i]

#     print("Peso do nivel " + str(nivel) + ": " + str(pesoNivel))

# print("----------------- Ultima Modificacao -----------------")

# for i in range(len(solucao)):
#     print("Item " + str(i) + ": " + str(solucao[i]))

# for nivel in range(max(solucao) + 1):
#     pesoNivel = 0

#     for i in range(N):
#         if (solucao[i]) == (nivel):
#             pesoNivel += W[i]

#     print("Peso do nivel " + str(nivel) + ": " + str(pesoNivel))

# print("----------------- Melhor de Todas -----------------")

# for i in range(len(melhorDeTodas)):
#     print("Item " + str(i) + ": " + str(melhorDeTodas[i]))

# for nivel in range(max(melhorDeTodas) + 1):
#     pesoNivel = 0

#     for i in range(N):
#         if (melhorDeTodas[i]) == (nivel):
#             pesoNivel += W[i]

#     print("Peso do nivel " + str(nivel) + ": " + str(pesoNivel))