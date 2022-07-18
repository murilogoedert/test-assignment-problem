
import sys, re, random, time
from os import walk
import matplotlib.pyplot as plot


from numpy import array

_numDesks = 0
_numDistances = 0
_numTests = 0
_numEmptyDesks = 0
_desks = []
_tests = []
_distanceMatrix = []
_similarityMatrix = []
_solution = []

_iterations = 100


def readInstance(instance = False):
    global _numDesks, _numDistances, _numTests, _numEmptyDesks, _desks, _tests, _distanceMatrix, _similarityMatrix

    _numDesks = 0
    _numDistances = 0
    _numTests = 0
    _numEmptyDesks = 0
    _desks = []
    _tests = []
    _distanceMatrix = []
    _similarityMatrix = []
    _solution = []

    if instance:
        file = open(instance)
    elif(len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        # file = open('instances/lab3_2x0.txt')
        file = open('instances/lab6b_2x20.txt')
        
    lines = file.readlines()
    sub = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', ' ', lines[0])));
    instanceParts = sub.split(' ')

    _numDesks = int(instanceParts[0])
    _numDistances = int(instanceParts[1])
    _numTests = int(instanceParts[2])
    _numEmptyDesks = int(instanceParts[3])

    countLines = 0
    _desks = []

    while(countLines < _numDesks):
        _desks.append(int(lines[countLines + 1]))
        countLines += 1

    _distanceMatrix = createMatrix(_numDesks, _numDesks, 0)

    countLines += 1

    while(countLines < (_numDistances + _numDesks + 1)):
        currentLine = lines[countLines]
        lineParts = re.sub('\n', '', re.sub('\t', ' ', currentLine)).split(' ');
        i = _desks.index(int(lineParts[0]))
        j = _desks.index(int(lineParts[1]))
        value = float(lineParts[2])
        _distanceMatrix[i][j] = value
        countLines += 1

    _similarityMatrix = createMatrix(_numTests, _numTests)

    while(countLines < _numDistances + _numDesks + 1 + (_numTests * 2)):
        currentLine = lines[countLines]

        lineParts = re.sub('\n', '', re.sub('\t', ' ', currentLine)).split(' ');
        if len(lineParts) > 3:
            lineParts = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', ' ', currentLine))).split(' ');
        i = int(lineParts[0])
        j = int(lineParts[1])
        value = float(lineParts[2])
        _similarityMatrix[i][j] = value
        countLines += 1

def createMatrix(lines, columns, defValue = 0):
    matrix = []
    for i in range(lines):
        line = []
        for j in range(columns):
            line.append(defValue)
        matrix.append(line)
    return matrix

def closestDesk(desk):
    distance = 0
    closest = 1

    for i in range(len(_distanceMatrix)):
        for j in range(i, len(_distanceMatrix)):
            if _distanceMatrix[i][j] != 0 and _distanceMatrix[i][j] > distance and  (i == desk or j == desk):
                distance = _distanceMatrix[i][j]
                if i == desk:
                    closest = j
                else:
                    closest = i
                
            if distance == 1:
                break
            
        if distance == 1:
            break

    return closest


def lessSimilarTest(test):
    similarity = 1
    bestTest = 1
    for i in range(len(_similarityMatrix)):
        for j in range(len(_similarityMatrix)):
            if _similarityMatrix[i][j] != 0 and _similarityMatrix[i][j] < similarity and (i == test or j == test):
                similarity = _similarityMatrix[i][j]
                if i == test:
                    bestTest = j
                else:
                    bestTest = i


    return bestTest

def chooseTest(test):
    testToChoose = test
    while testToChoose == test:
        testToChoose = random.randint(1, _numTests - 1)
    
    return testToChoose

def avaliaSolucao(sol):
    totalCost = 0
    for i in range(len(_distanceMatrix)):
        #Considera apenas os elementos acima da diagonal principal
        for j in range(i, len(_distanceMatrix)):
            if _distanceMatrix[i][j] > 0:
                indexT1 = sol[i]
                indexT2 = sol[j]
                #Inverte os indices das similaridades quando necessário, já que a matriz de similaridades Sij i <= j
                if indexT2 < indexT1:
                    indexT1 = indexT1 + indexT2
                    indexT2 = indexT1 - indexT2
                    indexT1 = indexT1 - indexT2

                totalCost += _similarityMatrix[indexT1][indexT2] * _distanceMatrix[i][j]

    return totalCost

def heuristicaConstrutiva1(allowEmpty = True):
    global _solution
    _solution = []
    if allowEmpty:
        for i in range(len(_desks)):
            _solution.append(0)

        for i in range(len(_desks) - _numEmptyDesks):
            _solution[i] = random.randint(1, _numTests - 1)  
    else:
        for i in range(len(_desks)):
            _solution.append(random.randint(1, _numTests - 1))

def heuristicaConstrutiva2(): 
    global _solution  
    _solution = []
    #inicia com tudo vazio
    for i in range(len(_desks)):
        _solution.append(0)

    #Para cada indice da solução
    for i in range(len(_solution)):
        if(_solution.count(0) > _numEmptyDesks):
            #O primeiro sempre atribui o teste 1
            if i == 0:
                _solution[i] = 1
            else:
                #Nos próximos, busca o indice da carteira mais proxima
                closest = closestDesk(i) 

                closestTest = _solution[closest]

                #Atribui no indice atual o teste que tem menos similaridade com a carteira mais proxima
                _solution[i] = lessSimilarTest(closestTest)


def modificaSolucaoSwapAleatorio(solucao):
    index1 = 0
    index2 = 0
    while index1 == index2:
        index1 = random.randint(0, len(solucao) - 1)
        index2 = random.randint(0, len(solucao) - 1)
    aux = solucao[index1];
    solucao[index1] = solucao[index2]
    solucao[index2] = aux

    return solucao

def modificaSolucaoSwapIndices(solucao, a, b):
    aux = solucao[a]
    solucao[a] = solucao[b]
    solucao[b] = aux
    return solucao

def modificaSolucaoSwapVantajoso(solucao):
    trocou = False
    initialValue = avaliaSolucao(solucao)
    solucaoConcumbente = solucao
    for i in range(10):
        solucaoConcumbente = modificaSolucaoSwapAleatorio(solucaoConcumbente)
        value = avaliaSolucao(solucaoConcumbente)
        if value < initialValue:
            return solucaoConcumbente

    return solucaoConcumbente

def modificaSolucaoTrocaTeste(solucao, index):
    test = solucao[index]
    while(test == solucao[index]):
        test = random.randint(1, _numTests - 1)

    solucao[index] = test

    return solucao, test

    

def criaSolucaoInicial():
    heuristicaConstrutiva1()


def doHeuristica1():
    readInstance()
    heuristicaConstrutiva1()
    print('\nHeurística Construtiva I')
    print('value ' + str("%0.2f" % avaliaSolucao(_solution)))
    print('-----------------------')

def doHeuristica2():
    readInstance()
    heuristicaConstrutiva2()
    print('\nHeurística Construtiva II')
    print('value ' + str("%0.2f" % avaliaSolucao(_solution)))
    print('-----------------------')


def caminhadaAleatoria():
    readInstance()
    criaSolucaoInicial()
    bestValue = 0
    solucaoConcumbente = _solution
    valueConcumbente = avaliaSolucao(_solution)

    for i in range(_iterations):
        newSolution = modificaSolucaoSwapAleatorio(solucaoConcumbente)
        value = avaliaSolucao(newSolution)
        if value < valueConcumbente:
            bestValue = value
            solucaoConcumbente = newSolution

    print('\nCaminhada aleatória')
    print('initial - ' + str("%0.2f" % valueConcumbente))
    print('value - ' + str("%0.2f" % bestValue))
    print('-----------------------')



def buscaLocalPrimeiraMelhora():
    readInstance()
    criaSolucaoInicial()
    valueConcumbente = avaliaSolucao(_solution)
    solucao = _solution
    bestValue = 0
    stop = False
    for i in range(len(_solution)):
        for j in range(i + 1, len(_solution)):
            newSol = modificaSolucaoSwapIndices(solucao, i, j,)
            value = avaliaSolucao(newSol)
            if value < valueConcumbente:
                stop = True
                solucao = newSol
                bestValue = value
                break
        if stop:
            break

    print('\nBusca Local - Primeira melhora')
    print('initial - ' + str("%0.2f" % valueConcumbente))
    print('value - ' + str("%0.2f" % bestValue))
    print('-----------------------')

def buscaLocalMelhorMelhora():
    readInstance()
    criaSolucaoInicial()
    valueConcumbente = avaliaSolucao(_solution)
    bestValue = valueConcumbente
    solucaoConcumbente = _solution
    stop = False
    cont = 0
    for i in range(len(_solution)):
        for j in range(i + 1, len(_solution)):
            newSol = modificaSolucaoSwapIndices(solucaoConcumbente, i, j,)
            value = avaliaSolucao(newSol)
            cont += 1
            if value < bestValue:
                solucaoConcumbente = newSol
                bestValue = value

    print('\nBusca Local - Melhor melhora')
    print('initial - ' + str("%0.2f" % valueConcumbente))
    print('value - ' + str("%0.2f" % bestValue))
    print('-----------------------')

def buscaLocalRandomizada():
    readInstance()
    criaSolucaoInicial()
    valueConcumbente = avaliaSolucao(_solution)
    initialValue = valueConcumbente
    solutionConcumbente = _solution
    for i in range(_iterations):
        if random.randint(0,1) == 0:
            solution = modificaSolucaoSwapAleatorio(solutionConcumbente)
        else:
            solution = modificaSolucaoSwapVantajoso(solutionConcumbente)
        
        value = avaliaSolucao(solution)
        if value < valueConcumbente:
            valueConcumbente = value
            solutionConcumbente = solution

    print('\nBusca Local Randomizada')
    print('initial - ' + str("%0.2f" % initialValue))
    print('value - ' + str("%0.2f" % valueConcumbente))
    print('-----------------------')

def orderList(el):
    return el[1]

def getScores(solution, reversed = False):
    scores = []
    for i in range(len(solution)):
        if solution[i] != 0:
            evalSol = solution.copy()
            evalSol[i] = 0
            scores.append((i, avaliaSolucao(evalSol)))

    scores.sort(key=orderList, reverse=reversed)
    return scores

def clearDesksByScore(solution, numEmptyDesks = 0):
    newSol = solution.copy()
    cont = 0
    for i in range(len(newSol)):
        if cont < numEmptyDesks:
            scores = getScores(newSol, reversed=False)
            newSol[scores[0][0]] = 0
        else:
            break 
        cont += 1

    return newSol



def buscaTabu():

    def buscaMelhorSolucaoNaoTabu(solucao:list, tabuList:list):
        list = []
        for i in range(len(solucao)):
            if tabuList.count(i) == 0:
                solTest = solucao.copy()
                solTest[i] = 0
                list.append((i, avaliaSolucao(solTest)))
        
        list.sort(key=orderList, reverse=True)
        indiceEscolhido = list[random.randint(0, randSelectionSize - 1)][0]

        bestValue = 9999999
        bestSolution = False


        for i in range(1, _numTests):
            solucaoAvaliar = solucao.copy()
            solucaoAvaliar[indiceEscolhido] = i
            value = avaliaSolucao(solucaoAvaliar)
            if value < bestValue:
                bestValue = value
                bestSolution = solucaoAvaliar

        return indiceEscolhido, bestSolution

    def removeDesks(solucao, qtd):
        for i in range(len(solucao)):
            if(solucao.count(0) < qtd):
                solucao[i] = 0


    def updateTabu(tabuCont:list, tabuList:list):
        for i in range(len(tabuCont)):
            if tabuCont[i] > 0:
                tabuCont[i] -= 1

            if tabuCont[i] == 0 and tabuList.count(i) > 0:
                tabuList.remove(i)

        return tabuCont, tabuList
        

    readInstance()
    heuristicaConstrutiva1(allowEmpty=False)
    solI = _solution.copy() 
    removeDesks(solI, _numEmptyDesks)
    initialValue = avaliaSolucao(solI)
    bestValue = initialValue
    bestSolution = _solution
    solucaoAtual = _solution
    tabuIteractions = 35
    randSelectionSize = 6
    totalIteracoes = 200
    tabuList = []
    tabuCont = [0 for i in range(_numDesks)]


    cont = 0

    pltX = []
    pltY = []

    while cont < totalIteracoes:
        tabuIndex, solucaoAtual = buscaMelhorSolucaoNaoTabu(solucaoAtual, tabuList)
        tabuList.append(tabuIndex)
        tabuCont[tabuIndex] = tabuIteractions

        cleanSolution = clearDesksByScore(solucaoAtual, _numEmptyDesks)
        currentValue = avaliaSolucao(cleanSolution)
        if currentValue < avaliaSolucao(bestSolution):
            bestSolution = cleanSolution
            bestValue = currentValue
            pltX.append(cont * 2)
            pltY.append(bestValue)

        updateTabu(tabuCont, tabuList)
        cont += 1

    print('\nBusca Tabu')
    print('initial - ' + str("%0.2f" % initialValue))
    print('value - ' + str("%0.2f" % bestValue))
    print('solution - ' + str(bestSolution))
    print('-----------------------')

    plot.plot(pltX, pltY)
    plot.show()
        
def construcaoRepedida():
    readInstance()
    criaSolucaoInicial()

def gulosoK():
    return

def reinicioAleatorio():
    return

# # Etapa II
# doHeuristica1()
# doHeuristica2()
# caminhadaAleatoria()
# buscaLocalPrimeiraMelhora()
# buscaLocalMelhorMelhora()

# Etapa III

# Modificação de Soluções
# buscaLocalRandomizada()
buscaTabu()
# reinicioAleatorio()

# #Construção de Soluções
# construcaoRepedida()
# gulosoK()


#WHAAAAT???
# .\instances\lab2_3x10.txt
# sol = [2, 0, 1, 2, 3, 0, 0, 2, 3, 3, 0, 3, 0, 3, 2, 3, 3, 2, 1, 0, 1, 3, 3, 3, 2, 0, 2, 3, 3, 2, 3, 3, 3, 3, 0, 3, 3, 3, 3, 2, 0, 0, 2, 3, 3, 2, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3]
# # sool = [1, 1, 0, 1, 0, 0, 1, 1, 0, 2, 0, 1, 1, 2, 1, 0, 2, 0, 1, 1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 1, 1, 1, 0, 2, 0, 0, 1, 1, 1, 2, 1, 1, 0]
# #sol = [1, 1, 0, 1, 0, 0, 2, 1, 0, 2, 0, 1, 1, 2, 1, 0, 2, 0, 1, 1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 1, 1, 1, 0, 2, 0, 0, 1, 1, 1, 2, 1, 1, 0]
# readInstance()
# print(avaliaSolucao(sol))





