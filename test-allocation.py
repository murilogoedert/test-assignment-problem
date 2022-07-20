from hashlib import md5
import sys, re, random, time
from os import walk
# import matplotlib.pyplot as plot


_numDesks = 0
_numDistances = 0
_numTests = 0
_numEmptyDesks = 0
_desks = []
_tests = []
_distanceMatrix = []
_similarityMatrix = []


_maxIterations = 100

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
       # file = open('instances/lab3_4x10.txt')
        file = open('instances/lab1_2x0.txt')
        
    
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

def orderFn(el):
    return float(el[1])

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

def removeEmptyDesks(solution):
    sol = solution.copy()
    if _numEmptyDesks > 0 and sol.count(0) == 0:
        count = 0
        while count < _numEmptyDesks:
            scores = []
            best = objective(sol)
            for i in range(len(sol)):
                if sol[i] != 0:
                    newSol = sol.copy()
                    newSol[i] = 0
                    scores.append((i, best - objective(newSol)))
            
            scores.sort(key=orderFn, reverse=True)
            sol[scores[0][0]] = 0
            count += 1
            
    return sol
 

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
            for teste in range(1, _numTests):
                newSol = solucao.copy()
                newSol[i] = teste
                if newSol != solucao:
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
        

        list.sort(key=orderFn)
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

def estrategiaMelhorVizinhoNaoTabu(solucao, tabuTable, tabuTenure, iteraction):
    actualValue = objective(solucao)
    vizinhanca = geraVizinhancaTrocaProvas(solucao)
    scores = []
    for vizinho in vizinhanca:
        scores.append((vizinho, actualValue - objective(vizinho)))
    
    scores.sort(key=orderFn, reverse=True)
    acceptedSolution = solucao

    for score in scores:
        sol = score[0]
        indexChange = getIndexOfChangeProva(solucao, sol)

        if tabuTable[indexChange] > 0:
            if iteraction - tabuTenure > tabuTable[indexChange]:
                acceptedSolution = sol
                tabuTable[indexChange] = iteraction
                break
        else:
            acceptedSolution = sol
            tabuTable[indexChange] = iteraction
            break

    return acceptedSolution

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
    
def bestTestForIndex(solucao, indice):
    scores = []
    for i in range(1, _numTests):
        sol = solucao.copy()
        sol[indice] = i
        obj = objective(sol)
        scores.append((i, obj))

    scores.sort(key=orderFn)

    return scores[0][0]

#################################
####Heurísticas Construtivas#####
#################################

#Totalmente randomica
def heuristicaConstrutiva_1(full = False):
    readInstance()
    solution = [0 for i in range(_numDesks)]

    for i in range(len(solution)):
        solution[i] = bestTestForIndex(solution, i)

    if full:
        return solution

    return removeEmptyDesks(solution)

#Utiliza a primeira heurística para criar uma solução inicial aleatória sem nenhuma carteira vazia
#Após isso vai removendo da solução as N provas que mais diminuiem o valor da função objetivo
def heuristicaConstrutiva_2():
    solution = heuristicaConstrutiva_1()
    initialValue = objective(solution)
    if _numEmptyDesks > 0:
        scores = []
        for i in range(len(solution)):
            newSolution = solution.copy()
            newSolution[i] = 0
            newValue = objective(newSolution)
            scores.append((i, initialValue - newValue))

        scores.sort(key=orderFn,  reverse=True)
        for i in range(_numEmptyDesks):
            solution[scores[i][0]] = 0

    return solution

def heuristicaConstrutivaAleatoria():
    return [random.randint(1, _numTests) for i in range(0, _numDesks)]



#################################
########## Comparações ##########
#################################

def buscaLocalSimplesPM(solucao=False):
    if not solucao:
        solucao = heuristicaConstrutiva_1(True)

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

    return removeEmptyDesks(bestSolution)

def buscaLocalSimplesMM(solucao=False):
    if not solucao:
        sol = heuristicaConstrutiva_1(True)
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

    return removeEmptyDesks(sol)

def caminhadaAleatoria(solucao=False):
    if not solucao:
        sol = heuristicaConstrutiva_1(True)
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

    return removeEmptyDesks(sol)

def buscaLocalRandomizada(p = 0, solucao=False):
    if not solucao:
        solucao = heuristicaConstrutiva_1(True)
    
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

    return removeEmptyDesks(bestSolution)

def buscaTabu(solucao=False, tabuTenure = 2):
    if not solucao:
        sol = heuristicaConstrutiva_1(True)
    else:
        sol = solucao.copy()
    
    bestSolution = sol
    bestValue = objective(sol)
    tabuTable = [0 for i in range(_numDesks)]

    for i in range(_maxIterations):
        sol = estrategiaMelhorVizinhoNaoTabu(sol, tabuTable, tabuTenure, i)
        obj = objective(sol)
  
        if obj < bestValue:
            bestValue = obj
            bestSolution = sol

    return removeEmptyDesks(bestSolution)

def construcaoRepetida(repeat = 4):
    bestSolution = heuristicaConstrutiva_1(True)
    bestValue = objective(bestSolution)
    sol = bestSolution
    for i in range(repeat):
        newSol = buscaLocalSimplesMM(solucao=sol)
        obj = objective(newSol)
        if obj < bestValue or bestSolution == False: 
            bestSolution = newSol
            bestValue = obj
        sol = heuristicaConstrutiva_1(True)
        sol = perturbaSolucaoSwapIndices(sol)
    
    return removeEmptyDesks(bestSolution)
    
# print('Heurística I : ' + str("%0.2f" % objective(heuristicaConstrutiva_1(False))))
# print('Heurística II : ' + str("%0.2f" % objective(heuristicaConstrutiva_2()))) Precisa melhorar esta
# print('Caminhada Aleatória : ' + str("%0.2f" % objective(caminhadaAleatoria())))
# print('Busca Local Simples PM : ' + str("%0.2f" % objective(buscaLocalSimplesPM())))
# print('Busca Local Simples MM : ' + str("%0.2f" % objective(buscaLocalSimplesMM())))

print('Busca Tabu : ' + str("%0.2f" % objective(buscaTabu(tabuTenure=3))))
# print('Busca Local Randomizada : ' + str("%0.2f" % objective(buscaLocalRandomizada(p=0))))
# print('Construção Repetida : ' + str("%0.2f" % objective(construcaoRepetida())))
