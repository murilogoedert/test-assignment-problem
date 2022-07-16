## Caminhada Aleatoria ##

import random
import time
import sys

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
"""
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
"""
def reorganizarBins(solucao):
    # Percorre a solucao
    for bin in range(2, max(solucao) + 2):
        # Se o bin anterior nao estiver na solucao
        if (bin - 1) not in solucao:
            # Percorre a solucao mudando todos para o nivel que antes estava vazio
            for n in range(len(solucao)):
                if (solucao[n] == bin):
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

def heuristica2():
    # array contendo a caixa de cada item
    Bins = []
    bin = []

    for w in W:
        best_bin = 0
        
        for j in bin:
            # se nao ultrapassa o peso da caixa atual
            peso = pesoAtual(Bins, j)
            if (w + peso <= C 
            # nao tem melhor caixa ou se o peso da caixa atual vai ficar maior que a melhor caixa
                and (best_bin == 0 or peso > pesoAtual(Bins, best_bin))):
                best_bin = j

        # se nao achou nenhuma caixa para colocar
        # cria uma nova caixa
        # adiciona na solucao a ultima caixa
        if (best_bin == 0):
            bin.append(len(bin) + 1)
            Bins.append(len(bin))
        else:
            Bins.append(best_bin)

    return Bins            

""""
def pesoAtual(solucao, j):
    peso = 0
    item = 0
    for i in solucao:
        if (i == j):
            peso += W[item]
        item += 1

    return peso    
"""
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

## Busca Local Primeira Melhora ##

def buscaSolucaoInicial():
    sol = []
    for peso in W:
        if len(sol) == 0:
            sol.append(1)
        else:
            binAtual = random.randint(1, max(sol) + 1)
            # O primeiro item vai na bin 1
            if (pesoAtual(sol, binAtual) + peso <= C):
                sol.append(binAtual)
            else:
                sol.append(max(sol) + 1)        

    return sol

def pesoAtual(sol, bin):
    global W

    peso = 0
    item = 0
    for binSolucao in sol:
        if binSolucao == bin:
            peso += W[item]
        item += 1

    return peso

def conta(dic):
    total = 0
    for valor in dic.values():
        total += valor
    
    return total

def getItensBin(bin, Bins):
    itens = []
    item = 0
    for binSolucao in Bins:
        if binSolucao == bin:
            itens.append(item)
        item += 1

    return itens    

def buscaLocalPM(Bins):
    global C, W, parou 

    # tentar mover todos os itens da caixa atual para uma nova caixa
    binMaior = max(Bins)

    # percorre todas as caixas para criar a vizinhança
    for binAtual in range(1, binMaior + 1):
        if (parou):
            return Bins

        solucaoAtual = Bins.copy()

        # busca os itens das caixas
        itens = getItensBin(binAtual, solucaoAtual)

        # percorre o item tentando colocar em outra caixa
        for item in itens:
            # percorre as caixas para tentar encaixar
            for binNovo in range(1, binMaior + 1):
                # se a caixa é diferente da atual
                if (binAtual != binNovo):
                    # se o peso atual mais o peso do item serve move o item
                    if ((pesoAtual(solucaoAtual, binNovo) + W[item]) <= C):
                        solucaoAtual[item] = binNovo
                        break

        solucaoAtual = reorganizarBins(solucaoAtual)

        if (max(solucaoAtual) < binMaior):
            Bins = solucaoAtual
            Bins = buscaLocalPM(Bins)

    # Se não achou nenhum vizinho melhor então para
    parou = True
    return Bins

## Busca Local Melhor Melhora ##

def buscaLocalMM(Bins):
    global C, W, parou

    # tentar mover todos os itens da caixa atual para uma nova caixa
    binMaior = max(Bins)
    melhorSolucao = []
    melhorEspacoSobrando = {0: C}

    # percorre todas as caixas para criar a vizinhança
    for binAtual in range(1, binMaior + 1):
        if (parou):
            return Bins

        solucaoAtual = Bins.copy()

        espacoSobrandoAtual = {}

        # busca os itens das caixas
        itens = getItensBin(binAtual, solucaoAtual)

        # percorre o item tentando colocar em outra caixa
        for item in itens:
            # percorre as caixas para tentar encaixar
            for binNovo in range(1, binMaior + 1):
                # se a caixa é diferente da atual
                if (binAtual != binNovo):
                    # se o peso atual mais o peso do item serve move o item
                    if ((pesoAtual(solucaoAtual, binNovo) + W[item]) <= C):
                        solucaoAtual[item] = binNovo
                        espacoSobrandoAtual[binNovo] = C - pesoAtual(solucaoAtual, binNovo)
                        break

        solucaoAtual = reorganizarBins(solucaoAtual)

        if (max(solucaoAtual) < binMaior) and (conta(espacoSobrandoAtual) < conta(melhorEspacoSobrando)):
            melhorSolucao = solucaoAtual.copy()
            melhorEspacoSobrando = espacoSobrandoAtual.copy()
        
    if len(melhorSolucao) > 0:
        Bins = melhorSolucao
        Bins = buscaLocalMM(Bins)

    # Se não achou nenhum vizinho melhor então para
    parou = True 
    return Bins

def grasp(heur, bl):
    timeEnd = time.time() + 30
    timeCount = 0
    timeSleep = 1

    # Comecamos com uma heuristica
    solucaoMelhor = heur()

    # Enquanto criterio de parada nao for satisfeito
    # while(cont < 1000):
    while time.time() < timeEnd:
        time.sleep(timeSleep)
        timeCount += timeSleep

        # Fazemos uma busca local na heuristica
        solucao = []
        solucao = heur()

        solucao = bl(solucao)

        # Se for melhor, atualiza
        if (max(solucao) < max(solucaoMelhor)):
            solucaoMelhor = solucao

    return solucaoMelhor

# Busca Local Multiplos Inicios
def buscaLocalMI():
    timeEnd = time.time() + 30
    timeCount = 0
    timeSleep = 1

    # Por enquanto a melhor solucao e a inicial
    solucaoMelhor = buscaSolucaoInicial()

    # Enquanto criterio de parada nao for satisfeito
    while time.time() < timeEnd:
        time.sleep(timeSleep)
        timeCount += timeSleep

        # Cria uma solucao aleatoria e executa busca local
        solucaoAtual = buscaLocalPM(buscaSolucaoInicial())

        # Se for melhor, atualiza
        if (max(solucaoAtual) < max(solucaoMelhor)):
            solucaoMelhor = solucaoAtual

    return solucaoMelhor

# Busca Local Randomizada
def buscaLocalR():
    timeEnd = time.time() + 30
    timeCount = 0
    timeSleep = 1
    probabilidadeAleatorio = 0 # [1-10] * 10 % (0 = BLSMM, 10 = CA)

    # Por enquanto a melhor solucao e a inicial
    solucaoMelhor = buscaSolucaoInicial()
    solucaoAtual = solucaoMelhor.copy()

    # Enquanto criterio de parada nao for satisfeito
    while time.time() < timeEnd:
        time.sleep(timeSleep)
        timeCount += timeSleep

        # Se caiu no aleatorio
        if random.randint(1, 10) > (10 - probabilidadeAleatorio):
            vizinhoAleatorio = buscaVizinhoAleatorio(solucaoAtual)

            # Se achou um vizinho
            if len(vizinhoAleatorio) > 0:
                solucaoAtual = vizinhoAleatorio
        else:
            # Senao busca o melhor vizinho
            melhorVizinho = buscaVizinhoMelhor(solucaoAtual)

            # Se achou um melhor vizinho
            if len(melhorVizinho) > 0:
                solucaoAtual = melhorVizinho

        # Se for melhor, atualiza
        if (max(solucaoAtual) < max(solucaoMelhor)):
            solucaoMelhor = solucaoAtual

    # Retorna a melhor solucao
    return solucaoMelhor

def buscaVizinhoAleatorio(Bins):
    global C, W

    binMaior = max(Bins)
    vizinhanca = []

    # Percorre todas as caixas para criar a vizinhança
    for binAtual in range(1, binMaior + 1):
        solucaoAtual = Bins.copy()

        # Busca os itens das caixas
        itens = getItensBin(binAtual, solucaoAtual)

        # Necessario verificar se conseguiu mover todos os itens
        totalItens = len(itens)
        itensMovidos = 0

        # Percorre o item tentando colocar em outra caixa
        for item in itens:
            # Percorre as caixas para tentar encaixar
            for binNovo in range(1, binMaior + 1):
                # Se a caixa é diferente da atual
                if (binAtual != binNovo):
                    # Se o peso atual mais o peso do item serve move o item
                    if ((pesoAtual(solucaoAtual, binNovo) + W[item]) <= C):
                        solucaoAtual[item] = binNovo
                        itensMovidos += 1
                        break
        
        # Se conseguiu mover todos os itens entao salva o vizinho
        if totalItens == itensMovidos:
            solucaoAtual = reorganizarBins(solucaoAtual)
            vizinhanca.append(solucaoAtual)

    # Retorna um vizinho aleatorio
    if len(vizinhanca) > 0:
        return vizinhanca[random.randint(0, len(vizinhanca))]
    
    return []

def buscaVizinhoMelhor(Bins):
    global C, W

    # Tenta mover todos os itens da caixa atual para uma nova caixa
    binMaior = max(Bins)
    melhorSolucao = []
    melhorEspacoSobrando = {0: C}

    # Percorre todas as caixas para criar a vizinhança
    for binAtual in range(1, binMaior + 1):
        solucaoAtual = Bins.copy()
        espacoSobrandoAtual = {}

        # Busca os itens das caixas
        itens = getItensBin(binAtual, solucaoAtual)

        # Percorre o item tentando colocar em outra caixa
        for item in itens:
            # Percorre as caixas para tentar encaixar
            for binNovo in range(1, binMaior + 1):
                # Se a caixa é diferente da atual
                if (binAtual != binNovo):
                    # Se o peso atual mais o peso do item serve move o item
                    if ((pesoAtual(solucaoAtual, binNovo) + W[item]) <= C):
                        solucaoAtual[item] = binNovo
                        espacoSobrandoAtual[binNovo] = C - pesoAtual(solucaoAtual, binNovo)
                        break

        solucaoAtual = reorganizarBins(solucaoAtual)

        if (max(solucaoAtual) < binMaior) and (conta(espacoSobrandoAtual) < conta(melhorEspacoSobrando)):
            melhorSolucao = solucaoAtual.copy()
            melhorEspacoSobrando = espacoSobrandoAtual.copy()
        
    # Retorna o melhor vizinho
    return melhorSolucao

# Construcao Repetida (com Guloso K)
# hmmm guloso

## Etapa 2 ##

# Percorrendo nossas 20 instancias
def percorreInstancias():
    global N, C, W, Bins, parou

    for i in range(1, 21):
        # Abre a instancia
        file = open("instances-bin/instancia" + str(i) + ".txt")

        # Percorrendo o arquivo, ignoramos as linhas que começam com //
        linhas = file.readlines()

        N = int(linhas[1].split("\n")[0])             # Itens a serem organizados
        C = int(linhas[3].split("\n")[0])             # Capacidade de cada caixa
        W = []                                        # Conjunto de pesos de cada item
        Bins = []                                     # Conjunto solucao
        parou = False                                 # Usado para as buscas locais

        # Pesos dos itens
        for ls in range(len(linhas)):
            if (ls > 6):
                W.append(int(linhas[ls].split("\n")[0]))

        file.close()

        ## Descomente a funcao a ser executada ##

        # Heurísticas #
        #solucao = heuristica1()
        #solucao = heuristica2()

        # Caminhada Aleatoria #
        #solucao = solucaoAleatoria()
        #comparativo, solucao, melhorDeTodas = caminhadaAleatoria()
        
        # Buscas Locais #
        solucao = buscaLocalPM(buscaSolucaoInicial())
        #solucao = buscaLocalMM(buscaSolucaoInicial())

        ## Etapa 2 ##
        #solucao = grasp(heuristica2, buscaLocalPM)
        #solucao = buscaLocalMI()
        # solucao = buscaLocalR()

        print("Instancia " + str(i) + ": " + str(max(solucao)))

percorreInstancias()
""""
## Etapa 3 ##

if (len(sys.argv) == 4):
    inst = sys.argv[1]      # Instancia escolhida
    alg = sys.argv[2]       # Algoritmo escolhida
    heur = sys.argv[3]      # Heuristica escolhida
    bl = sys.argv[4]        # Busca Local escolhida
else:    
    inst = "instancia1.txt"      # Instancia padrao
    alg = grasp       # Algoritmo padrao
    heur = heuristica2      # Heuristica padrao
    bl = buscaLocalPM        # Busca Local padrao

# Abre a instancia
file = open("instances/" + inst)

# Percorrendo o arquivo, ignoramos as linhas que começam com //
linhas = file.readlines()

N = int(linhas[1].split("\n")[0])             # Itens a serem organizados
C = int(linhas[3].split("\n")[0])             # Capacidade de cada caixa
W = []                                        # Conjunto de pesos de cada item
Bins = []                                     # Conjunto solucao
parou = False                                 # Usado para as buscas locais

# Pesos dos itens
for ls in range(len(linhas)):
    if (ls > 6):
        W.append(int(linhas[ls].split("\n")[0]))

file.close()    

solucao = alg(heur, bl)

print("Instancia " + inst + ": " + str(max(solucao)) + " bins")
"""