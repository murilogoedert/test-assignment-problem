
from ast import walk
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
        file = open('instances/lab3_2x0.txt')
        # file = open('instances/lab6b_2x20.txt')
        
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
    index1 = 0;
    index2 = 0;
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
    heuristicaConstrutiva1()
    bestValue = 0
    solucaoConcumbente = _solution
    valueConcumbente = avaliaSolucao(_solution)

    for i in range(10000):
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
    heuristicaConstrutiva1()
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
    heuristicaConstrutiva1()
    valueConcumbente = avaliaSolucao(_solution)
    bestValue = valueConcumbente
    solucaoConcumbente = _solution
    stop = False
    cont =0
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
    

doHeuristica1()
doHeuristica2()
caminhadaAleatoria()
buscaLocalPrimeiraMelhora()
buscaLocalMelhorMelhora()

#teste




# f = []
# for (dirpath, dirnames, filenames) in walk('instances/'):
#     f.extend(filenames)
#     break

# for ff in f:
#     readInstance('instances/' + ff)
#     solucaoInicial()
#     print(_solution)
#     caminhadaAleatoria()



# heuristicaConstrutiva2()
# print(_solution)

# _desks, _numDistances, _numTests, _numEmptyDesks, _distanceMatrix, _similarityMatrix = readInstance()
# print(closestDesk(_distanceMatrix, 22))
# print(_distanceMatrix[2][3])
# print(_similarityMatrix)




#  python .\test-allocation.py instances/lab1_2x10.txt 


    