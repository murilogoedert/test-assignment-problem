from calendar import TUESDAY
import sys, re, random, time
from os import walk
import matplotlib.pyplot as plot


_numDesks = 0
_numDistances = 0
_numTests = 0
_numEmptyDesks = 0
_desks = []
_tests = []
_distanceMatrix = []
_similarityMatrix = []


_maxIterations = 200

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

    if instance:
        file = open(instance)
    elif(len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        file = open('instances/lab3_2x0.txt')
        #file = open('instances/lab1_2x10.txt')
        
    
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

    while(countLines < len(lines)):
        currentLine = lines[countLines]

        lineParts = re.sub('\n', '', re.sub('\t', ' ', currentLine)).split(' ');
        if len(lineParts) > 3:
            lineParts = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', ' ', currentLine))).split(' ');
        i = int(lineParts[0])
        j = int(lineParts[1])
        value = float(lineParts[2])
        _similarityMatrix[i][j] = value
        countLines += 1

def objective(sol):
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

def createMatrix(lines, columns, defValue = 0):
    matrix = []
    for i in range(lines):
        line = []
        for j in range(columns):
            line.append(defValue)
        matrix.append(line)
    return matrix

def geraVizinhancaTrocaIndices(solucao):
    vizinhanca = []
    for i in range(len(solucao)):
        for j in range(i, len(solucao)):
            newSol = solucao.copy()
            valI = solucao[i]
            valJ = solucao[j]
            newSol[i] = valJ
            newSol[j] = valI
            vizinhanca.append(newSol)

    return vizinhanca

def geraVizinhancaTrocaProvas(solucao):
    vizinhanca = []
    for i in range(len(solucao)):
        if solucao[i] > 0:
            for teste in range(1, _numTests - 1):
                newSol = solucao.copy()
                newSol[i] = teste
                vizinhanca.append(newSol)
    
    return vizinhanca


def estrategiaMelhorVizinhoTrocaProvas(solucao, randSelection = False):
    vizinhanca = geraVizinhancaTrocaProvas(solucao)
    bestSolution = solucao

    if(randSelection == False):
        bestValue = objective(solucao)

        for vizinho in vizinhanca:
            obj = objective(vizinho)
            if obj < bestValue:
                bestSolution = vizinho
                bestValue = obj
    else:
        list = []
        for vizinho in vizinhanca:
            obj = objective(vizinho)
            if list.count((vizinhanca.index(vizinho), obj)) == 0:
                list.append((vizinhanca.index(vizinho), obj))
        
        def orderList(o):
            return o[1]

        list.sort(key=orderList)
        bestSolution = vizinhanca[random.choice(list[0:randSelection])[0]]

    return bestSolution

def estrategiaMelhorVizinhoTrocaIndices(solucao):
    vizinhanca = geraVizinhancaTrocaIndices(solucao)
    bestValue = objective(solucao)
    bestSolution = solucao

    for vizinho in vizinhanca:
        obj = objective(vizinho)
        if obj < bestValue:
            bestSolution = vizinho
            bestValue = obj

    return bestSolution

def perturbaSolucaoSwapIndices(solucao):
    sol = solucao.copy()
    i = 0
    j = 0
    while(i == j):
        i = random.randint(0, len(sol) - 1)
        j = random.randint(0, len(sol) - 1)

    aux = sol[i]
    sol[i] = sol[j]
    sol[j] = aux

    return sol

def perturbaSolucaoSwapTest(solucao):
    sol = solucao.copy()
    index = random.randint(0, len(sol) - 1)
    while sol[index] == 0:
        index = random.randint(0, len(sol) - 1)

    test = sol[index]
    newTest = random.randint(1, _numTests - 1)
    while(newTest == test):
         newTest = random.randint(1, _numTests - 1)

    sol[index] = newTest

    return sol

def getIndexOfChangeProva(solucao1, solucao2):
    for index, (first, second) in enumerate(zip(solucao1, solucao2)):
        if first != second:
            return index
    return -1
    

#################################
####Heurísticas Construtivas#####
#################################


#Totalmente randomica
def heuristicaConstrutiva_1(full=False):
    readInstance()
    solution = [0 for i in range(_numDesks)]
    rang = len(solution) - _numEmptyDesks if not full else len(solution)
    for i in range(rang):
        solution[i] = random.randint(1, _numTests - 1)

    return solution

#Utiliza a primeira heurística para criar uma solução inicial aleatória sem nenhuma carteira vazia
#Após isso vai removendo da solução as N provas que mais diminuiem o valor da função objetivo
def heuristicaConstrutiva_2():
    solution = heuristicaConstrutiva_1(True)
    initialValue = objective(solution)
    if _numEmptyDesks > 0:
        scores = []
        for i in range(len(solution)):
            newSolution = solution.copy()
            newSolution[i] = 0
            newValue = objective(newSolution)
            scores.append((i, initialValue - newValue))

        def orderFn(el):
            return el[1]

        scores.sort(key=orderFn,  reverse=True)
        for i in range(_numEmptyDesks):
            solution[scores[i][0]] = 0

    return solution

#################################
########## Comparações ##########
#################################

def buscaLocalSimplesPM(solucao=False):
    if not solucao:
        solucao = heuristicaConstrutiva_2()

    value = objective(solucao)
    bestSolution = solucao

    for i in range(_maxIterations):
        melhorou = False
        vizinhos = geraVizinhancaTrocaProvas(solucao)
        for vizinho in vizinhos:
            obj = objective(vizinho)
            if(obj < value):
                value = obj
                melhorou = True
                bestSolution = vizinho
        
        if melhorou:
            break

    return bestSolution

def buscaLocalSimplesMM(solucao=False):
    if not solucao:
        sol = heuristicaConstrutiva_2()
    else:
        sol = solucao.copy()
    
    bestValue = objective(sol)
    
    stop = False
    iter = 0;
    while(not stop):
        iter += 1
        vizinhos = geraVizinhancaTrocaProvas(sol)
        melhorou = False
        for vizinho in vizinhos:
            obj = objective(vizinho)
            if(obj < bestValue):
                bestValue = obj
                melhorou = True
                sol = vizinho


        if not melhorou:
            stop = True

    return sol

def caminhadaAleatoria(solucao=False):
    if not solucao:
        sol = heuristicaConstrutiva_2()
    else:
        sol = solucao.copy()
    
    bestValue = objective(sol)

    for i in range(_maxIterations):
        if random.randint(0, 1) == 1:
            newSol = perturbaSolucaoSwapIndices(sol)
        else:
            newSol = perturbaSolucaoSwapTest(sol)

        obj = objective(newSol)

        if(obj < bestValue):
            sol = newSol
            bestValue = obj

    return sol

def buscaLocalRandomizada(p = 0, solucao=False):
    if not solucao:
        solucao = heuristicaConstrutiva_2()
    
    bestValue = objective(solucao)
    bestSolution = solucao
    concumbente = solucao
    
    for i in range(_maxIterations):      
        r = random.randint(0, 1)
        if r <= p:
            concumbente = perturbaSolucaoSwapIndices(concumbente)
        else:
            concumbente = estrategiaMelhorVizinhoTrocaIndices(concumbente)

        if(objective(concumbente) < bestValue):
            bestSolution = concumbente

    return bestSolution

def buscaTabu(solucao=False, tabuTenure = 4):
    if not solucao:
        sol = heuristicaConstrutiva_2()
    else:
        sol = solucao.copy()
    
    bestSolution = sol
    bestValue = objective(sol)
    tabuTable = [0 for i in range(_numDesks)]

    for i in range(_maxIterations):
        solucaoAtual = estrategiaMelhorVizinhoTrocaProvas(sol)
        indexTabu = getIndexOfChangeProva(solucaoAtual, sol)
        if tabuTable[indexTabu] > 0:
            if i - tabuTenure > tabuTable[indexTabu]:
                sol = solucaoAtual
                tabuTable[indexTabu] = i
            #aspiração
            elif objective(solucaoAtual) < bestValue:
                sol = solucaoAtual
                tabuTable[indexTabu] = i
        else:
            sol = solucaoAtual
            tabuTable[indexTabu] = i

        obj = objective(sol)  
        if obj < bestValue:
            bestValue = obj
            bestSolution = sol

    return bestSolution

def construcaoRepetida(numer: int ,repeat = 20):
    # bestSolution = heuristicaConstrutiva_2()
    # bestValue = objective(bestSolution)
    # for i in range(repeat):
    #     sol = heuristicaConstrutiva_2()
    #     newSol = buscaLocalRandomizada(solucao=sol)
    #     obj = objective(newSol)
    #     if obj < bestValue:
    #         bestSolution = newSol
    #         bestValue = obj
    
    # return bestSolution
    return True
    
# print(objective(heuristicaConstrutiva_1()))
# print(objective(heuristicaConstrutiva_2()))
# print(objective(caminhadaAleatoria()))
# print(objective(buscaLocalSimplesPM()))
# print(objective(buscaTabu()))
readInstance()
sol = buscaLocalRandomizada()
print(sol)
print(objective(sol))

# print(objective(buscaLocalRandomizada(p = 0)))
# print(construcaoRepetida())
# print(objective(buscaTabu()))

print('Best Known: ' + str(23.18))