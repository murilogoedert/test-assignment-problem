
from ast import walk
from operator import index
import sys, re, random, time
from os import walk

_numDesks = 0
_numDistances = 0
_numTests = 0
_numEmptyDesks = 0
_desks = []
_tests = []
_distanceMatrix = []
_similarityMatrix = []
_solution = []

_iterations = 70


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

def heuristicaConstrutiva1():
    global _solution
    _solution = []
    for i in range(len(_desks)):
        _solution.append(0)

    for i in range(len(_desks) - _numEmptyDesks):
        _solution[i] = random.randint(1, _numTests - 1)  

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
    for i in range(_iterations):
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

def atualizaTabu(tabuTable):
    for i in range(len(tabuTable)):
        for j in range(len(tabuTable)):
            if tabuTable[i][j] > 0:
                tabuTable[i][j] = tabuTable[i][j] - 1
    
    return tabuTable


def buscaTabu():
    readInstance()
    criaSolucaoInicial()
    tabuTable = createMatrix(_numDesks, _numDesks)
    initialValue = avaliaSolucao(_solution)
    bestValue = initialValue
    tabuIterations = 5
    solucaoConcumbente = _solution

    for iter in range(_iterations):
        for i in range(len(_solution)):
            for j in range(len(_solution)):
                solucao = modificaSolucaoSwapIndices(solucaoConcumbente, i, j)
                tabu = False
                if tabuTable[i][j] == 0:
                    solucaoConcumbente = solucao
                else:
                    print('tabu!')
                    tabu = True
            
                tabuTable = atualizaTabu(tabuTable)
                value = avaliaSolucao(solucao)
                if value < bestValue and not tabu:
                    bestValue = value
                    tabuTable[i][j] = tabuIterations

    print('\nBusca Tabu')
    print('initial - ' + str("%0.2f" % initialValue))
    print('value - ' + str("%0.2f" % bestValue))
    print('-----------------------')
        
    

#Etapa II
doHeuristica1()
doHeuristica2()
caminhadaAleatoria()
buscaLocalPrimeiraMelhora()
buscaLocalMelhorMelhora()

#Etapa III

#Modificação de Soluções
buscaLocalRandomizada()
buscaTabu()

#Construção de Soluções
