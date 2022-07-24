import sys, re, random, time
from os import walk
import matplotlib.pyplot as plt

_numDesks = 0
_numDistances = 0
_numTests = 0
_numEmptyDesks = 0
_desks = []
_tests = []
_distanceMatrix = []
_similarityMatrix = []
_instanceFile = 'instances/lab1_2x0.txt'


_maxIterations = 700
_maxTime = 40


# _stop_condition = 'iterations'
_stop_condition = 'time'


def readInstance(instance=False):
    global _numDesks, _numDistances, _numTests, _numEmptyDesks, _desks, _tests, _distanceMatrix, _similarityMatrix, _instanceFile

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
    elif (len(sys.argv) > 1):
        _instanceFile = sys.argv[1]
        file = open(sys.argv[1])
    else:
        file = open(_instanceFile)

    lines = file.readlines()
    sub = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', ' ', lines[0])))
    instanceParts = sub.split(' ')

    _numDesks = int(instanceParts[0])
    _numDistances = int(instanceParts[1])
    _numTests = int(instanceParts[2])
    _numEmptyDesks = int(instanceParts[3])

    countLines = 0
    _desks = []

    while (countLines < _numDesks):
        _desks.append(int(lines[countLines + 1]))
        countLines += 1

    _distanceMatrix = createMatrix(_numDesks, _numDesks, 0)

    countLines += 1

    while (countLines < (_numDistances + _numDesks + 1)):
        currentLine = lines[countLines]
        lineParts = re.sub('\n', '', re.sub('\t', ' ', currentLine)).split(' ')
        i = _desks.index(int(lineParts[0]))
        j = _desks.index(int(lineParts[1]))
        value = float(lineParts[2])
        _distanceMatrix[i][j] = value
        countLines += 1

    _similarityMatrix = createMatrix(_numTests, _numTests)

    while (countLines < len(lines)):
        currentLine = lines[countLines]

        lineParts = re.sub('\n', '', re.sub('\t', ' ', currentLine)).split(' ')
        if len(lineParts) > 3:
            lineParts = re.sub(
                ' +', ' ', re.sub('\n', '', re.sub('\t', ' ',
                                                   currentLine))).split(' ')
        i = int(lineParts[0])
        j = int(lineParts[1])
        value = float(lineParts[2])
        _similarityMatrix[i][j] = value
        countLines += 1


def orderFn(el):
    return float(el[1])


# def commentPlot(x, y, text):
#     ax.annotate('arc,\narms',
#             xy=(2, 30),
#             xycoords='data',
#             textcoords='offset points',
#             arrowprops=dict(arrowstyle="->"))

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

                totalCost += _similarityMatrix[indexT1][
                    indexT2] * _distanceMatrix[i][j]

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


def createMatrix(lines, columns, defValue=0):
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
        for teste in range(1, _numTests):
            newSol = solucao.copy()
            newSol[i] = teste
            if newSol != solucao:
                vizinhanca.append(newSol)
    return vizinhanca


def estrategiaMelhorVizinhoTrocaProvas(solucao, randSelection=False):
    vizinhanca = geraVizinhancaTrocaProvas(solucao)
    bestSolution = solucao

    if (randSelection == False):
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


def estrategiaMelhorVizinhoNaoTabu(solucao, tabuTable, tabuTenure, iteraction,
                                   bestValue):
    actualValue = objective(solucao)
    vizinhanca = geraVizinhancaTrocaProvas(solucao)
    scores = []
    for vizinho in vizinhanca:
        obj = objective(vizinho)
        # (solução, score, valor da função objetivo)
        scores.append((vizinho, actualValue - obj, obj))

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
            elif score[2] < bestValue:  #aspiração
                acceptedSolution = sol
                tabuTable = [0 for i in range(0, _numDesks)]
                break
        else:
            acceptedSolution = sol
            tabuTable[indexChange] = iteraction
            break

    return acceptedSolution


def perturbaSolucaoSwapIndices(solucao, qtd=1):
    sol = solucao.copy()
    cont = 0
    while cont < qtd:
        i = 0
        j = 0
        while (i == j):
            i = random.randint(0, len(sol) - 1)
            j = random.randint(0, len(sol) - 1)

        aux = sol[i]
        sol[i] = sol[j]
        sol[j] = aux
        cont += 1

    return sol


def perturbaSolucaoSwapTest(solucao):
    sol = solucao.copy()
    index = random.randint(0, len(sol) - 1)
    while sol[index] == 0:
        index = random.randint(0, len(sol) - 1)

    test = sol[index]
    newTest = random.randint(1, _numTests - 1)
    while (newTest == test):
        newTest = random.randint(1, _numTests - 1)

    sol[index] = newTest

    return sol


def getIndexOfChangeProva(solucao1, solucao2):
    for index, (first, second) in enumerate(zip(solucao1, solucao2)):
        if first != second:
            return index
    return -1


def bestTestForIndex(solucao, indice, k=0):
    scores = []
    for i in range(1, _numTests):
        sol = solucao.copy()
        sol[indice] = i
        obj = objective(sol)
        scores.append((i, obj))

    scores.sort(key=orderFn)

    if k == 0:
        return scores[0][0]

    if k > len(scores):
        k = len(scores)

    return scores[random.randint(0, k - 1)][0]


def testAllInstances():
    f = []
    for (dirpath, dirnames, filenames) in walk('instances/'):
        f.extend(filenames)
        break

    for fileName in f:
        testInstance(fileName)

def testInstance(filename = False):
    global _instanceFile

    if filename:
        _instanceFile = 'instances/' + filename

    readInstance()

    print('############################# instance: ' + _instanceFile + ' ##################################')

    #5 primeiros
    print('\n##### Heuristicas Construtivas #####')
    print('Heurística I : ' + str("%0.2f" % objective(heuristicaConstrutiva_1(False))))
    print('Heurística II : ' + str("%0.2f" % objective(heuristicaConstrutiva_2())))
    print('\n##### Comparações #####')
    print('Caminhada Aleatória : ' + str("%0.2f" % objective(caminhadaAleatoria())))
    print('Busca Local Simples PM : ' + str("%0.2f" % objective(buscaLocalSimplesPM())))
    print('Busca Local Simples MM : ' + str("%0.2f" % objective(buscaLocalSimplesMM())))

    #5 implementações
    print('\n##### 5 implementações #####')
    print('Busca Tabu : ' + str("%0.2f" % objective(buscaTabu(tabuTenure=10, doPlot=False))))
    print('Busca Local Randomizada : ' + str("%0.2f" % objective(buscaLocalRandomizada(p=0))))
    print('Construção Repetida : ' + str("%0.2f" % objective(construcaoRepetida())))
    print('Guloso-K : ' + str("%0.2f" % objective(gulosoK(k=1))))
    print('Random Reestart : ' + str("%0.2f" % objective(randomReestart())))

    #6 extras
    print('\n##### 6 algoritmos hibridos #####')
    print('"Auto-Tabu" : ' + str("%0.2f" % objective(tabuAutoTenure(cycleRange=12, initialTenure=1, tenureIncrement=2, cutRange=25, doPlot=False))))
    print('Tabu + Guloso-K : ' + str("%0.2f" % objective(tabuComGulosoK())))
    print('Tabu + Construcao Repetida : ' + str("%0.2f" % objective(tabuComConstrucaoRepetida())))
    print('Random Reestart + Guloso-K : ' + str("%0.2f" % objective(randomRestartComGulosoK())))
    print('Construção Repetida + Guloso-K : ' + str("%0.2f" % objective(construcaoRepetidaComGulosoK())))
    print('Construção Repetida + Perturbação : ' + str("%0.2f" % objective(construcaoRepetidaComPerturbacao())))

    print('\n##################################################################################################')


#################################
####Heurísticas Construtivas#####
#################################


#Totalmente randomica
def heuristicaConstrutiva_1(full=False):
    readInstance()
    solution = [0 for i in range(_numDesks)]

    for i in range(len(solution)):
        solution[i] = bestTestForIndex(solution, i)

    if full:
        return solution

    return removeEmptyDesks(solution)


def gulosoK(k=3, full=False):
    readInstance()
    solution = [0 for i in range(_numDesks)]

    for i in range(len(solution)):
        solution[i] = bestTestForIndex(solution, i, k)

    if full:
        return solution

    return removeEmptyDesks(solution)


#Utiliza a primeira heurística para criar uma solução inicial aleatória sem nenhuma carteira vazia
#Após isso vai removendo da solução as N provas que mais diminuiem o valor da função objetivo
def heuristicaConstrutiva_2(full=False):
    readInstance()
    sol = [random.randint(1, _numTests - 1) for i in range(0, _numDesks)]
    if full:
        return sol

    return removeEmptyDesks(sol)


#################################
########## Comparações ##########
#################################


def buscaLocalSimplesPM(solucao=False):
    if not solucao:
        solucao = heuristicaConstrutiva_1(True)

    value = objective(solucao)
    bestSolution = solucao
    melhorou = False
    if _stop_condition == 'iterations':
        for i in range(_maxIterations):
            vizinhos = geraVizinhancaTrocaProvas(solucao)
            for vizinho in vizinhos:
                obj = objective(vizinho)
                if (obj < value):
                    value = obj
                    melhorou = True
                    bestSolution = vizinho

            if melhorou:
                break
    else:
        firstTime = time.time()
        while time.time() - firstTime < _maxTime:
            vizinhos = geraVizinhancaTrocaProvas(solucao)
            for vizinho in vizinhos:
                obj = objective(vizinho)
                if (obj < value):
                    value = obj
                    bestSolution = vizinho
                    break

    return removeEmptyDesks(bestSolution)


def buscaLocalSimplesMM(solucao=False):
    if not solucao:
        sol = heuristicaConstrutiva_1(True)
    else:
        sol = solucao.copy()

    bestValue = objective(sol)

    stop = False
    iter = 0
    while (not stop):
        iter += 1
        vizinhos = geraVizinhancaTrocaProvas(sol)
        melhorou = False
        for vizinho in vizinhos:
            obj = objective(vizinho)
            if (obj < bestValue):
                bestValue = obj
                melhorou = True
                sol = vizinho

        if not melhorou:
            stop = True

    return removeEmptyDesks(sol)


def randomReestart(solucao=False, reestarts=15, doPlot=False):
    if not solucao:
        sol = heuristicaConstrutiva_2(full=True)
    else:
        sol = solucao.copy()

    bestSolution = sol
    bestValue = objective(sol)

    reestartCount = 0

    pX = []
    pY = []

    cont = 0
    while reestartCount < reestarts:
        newSol = buscaLocalSimplesMM(sol)
        obj = objective(newSol)
        if doPlot:
            pX.append(cont)
            pY.append(obj)
        if obj < bestValue:
            bestValue = obj
            sol = newSol
            bestSolution = sol
        else:
            sol = heuristicaConstrutiva_2(full=True)
            reestartCount += 1

        cont += 1
    if doPlot:
        plt.plot(pX, pY)
        plt.show()

    return removeEmptyDesks(bestSolution)


def caminhadaAleatoria(solucao=False):
    if not solucao:
        sol = heuristicaConstrutiva_1(True)
    else:
        sol = solucao.copy()

    bestValue = objective(sol)

    if _stop_condition == 'iterations':
        for i in range(_maxIterations):
            if random.randint(0, 1) == 1:
                newSol = perturbaSolucaoSwapIndices(sol)
            else:
                newSol = perturbaSolucaoSwapTest(sol)

            obj = objective(newSol)

            if (obj < bestValue):
                sol = newSol
                bestValue = obj
    else:
        firstTime = time.time()
        while time.time() - firstTime < _maxTime:
            if random.randint(0, 1) == 1:
                newSol = perturbaSolucaoSwapIndices(sol)
            else:
                newSol = perturbaSolucaoSwapTest(sol)

            obj = objective(newSol)

            if (obj < bestValue):
                sol = newSol
                bestValue = obj

    return removeEmptyDesks(sol)


def buscaLocalRandomizada(p=0, solucao=False):
    if not solucao:
        solucao = heuristicaConstrutiva_2(True)

    bestValue = objective(solucao)
    bestSolution = solucao
    concumbente = solucao

    if _stop_condition == 'iterations':
        for i in range(_maxIterations):
            r = random.randint(0, 1)
            if r <= p:
                concumbente = perturbaSolucaoSwapIndices(concumbente)
            else:
                concumbente = estrategiaMelhorVizinhoTrocaIndices(concumbente)

            if (objective(concumbente) < bestValue):
                bestSolution = concumbente
    else:
        firstTime = time.time()
        while time.time() - firstTime < _maxTime:
            r = random.randint(0, 1)
            if r <= p:
                concumbente = perturbaSolucaoSwapIndices(concumbente)
            else:
                concumbente = estrategiaMelhorVizinhoTrocaIndices(concumbente)

            if (objective(concumbente) < bestValue):
                bestSolution = concumbente

    return removeEmptyDesks(bestSolution)


def buscaTabu(solucao=False, tabuTenure=5, doPlot=False):
    if not solucao:
        sol = heuristicaConstrutiva_2(True)
    else:
        sol = solucao.copy()

    dataX = []
    dataY = []

    bestSolution = sol
    bestValue = objective(sol)
    tabuTable = [0 for i in range(_numDesks)]

    if _stop_condition == 'iterations':
        for i in range(_maxIterations):
            sol = estrategiaMelhorVizinhoNaoTabu(sol, tabuTable, tabuTenure, i, bestValue)
            obj = objective(sol)

            if doPlot:
                dataY.append(objective(removeEmptyDesks((sol))))
                dataX.append(i)

            if obj < bestValue:
                bestValue = obj
                bestSolution = sol
    else:
        firstTime = time.time()
        iterCount = 0
        while time.time() - firstTime < _maxTime:
            sol = estrategiaMelhorVizinhoNaoTabu(sol, tabuTable, tabuTenure, iterCount, bestValue)
            obj = objective(sol)

            if doPlot:
                dataY.append(objective(removeEmptyDesks((sol))))
                dataX.append(iterCount)

            if obj < bestValue:
                bestValue = obj
                bestSolution = sol

            iterCount += 1

    if doPlot:
        plt.plot(dataX, dataY)
        plt.show()

    return removeEmptyDesks(bestSolution)


def construcaoRepetida(repeat=10):
    bestSolution = heuristicaConstrutiva_2(full=True)
    bestValue = objective(bestSolution)
    sol = bestSolution
    for i in range(repeat):
        newSol = buscaLocalSimplesMM(solucao=sol)
        obj = objective(newSol)
        if obj < bestValue or bestSolution == False:
            bestSolution = newSol
            bestValue = obj
        sol = heuristicaConstrutiva_2(full=True)

    return removeEmptyDesks(bestSolution)

def construcaoRepetidaComGulosoK(repeat=10):
    bestSolution = gulosoK(k=2, full=True)
    bestValue = objective(bestSolution)
    sol = bestSolution
    for i in range(repeat):
        newSol = buscaLocalSimplesMM(solucao=sol)
        obj = objective(newSol)
        if obj < bestValue or bestSolution == False:
            bestSolution = newSol
            bestValue = obj
        sol = gulosoK(k=2, full=True)

    return removeEmptyDesks(bestSolution)

def construcaoRepetidaComPerturbacao(repeat=15):
    bestSolution = heuristicaConstrutiva_2(full=True)
    bestValue = objective(bestSolution)
    sol = bestSolution
    for i in range(repeat):
        sol = perturbaSolucaoSwapTest(sol)
        newSol = buscaLocalSimplesMM(solucao=sol)
        obj = objective(newSol)
        if obj < bestValue or bestSolution == False:
            bestSolution = newSol
            bestValue = obj
        sol = heuristicaConstrutiva_2(full=True)

    return removeEmptyDesks(bestSolution)


#initialTenure - Valor inicial da tabu tenure
#tenureIncrement - A cada ciclo, caso não haja melhora, incrementa este valor na tenure
#cycleRange - Quantidade permitida de iterações sem melhora
#cutRange - percentual de piora tolerado, quando atingilo, volta a tenure para o valor inicial
def tabuAutoTenure(solucao=False,
                   initialTenure=5,
                   tenureIncrement=2,
                   cycleRange=60,
                   cutRange=20,
                   doPlot = True):
    if not solucao:
        sol = heuristicaConstrutiva_1(True)
    else:
        sol = solucao.copy()

    dataX = []
    dataY = []

    bestSolution = sol
    initialSolution = sol
    bestValue = objective(sol)

    tabuTable = [0 for i in range(_numDesks)]
    tabuTenure = initialTenure

    min = bestValue
    solMin = initialSolution
    cycleCount = 0

    if _stop_condition == 'iterations':
        for i in range(_maxIterations):
            cycleCount += 1
            sol = estrategiaMelhorVizinhoNaoTabu(sol, tabuTable, tabuTenure, i,
                                             bestValue)
            obj = objective(sol)

            #atualiza os minimos, quando atualiza, zera o contador
            #de ciclos, permitindo mais rodadas sem atualizar a tenure
            if obj < min:
                min = obj
                solMin = sol
                cycleCount = 0

            if doPlot:
                realSol = obj#objective(removeEmptyDesks(sol))
                dataY.append(realSol)
                dataX.append(i)

            if obj < bestValue:
                bestValue = obj
                bestSolution = sol
            else:
                if cycleCount >= cycleRange:
                    tabuTenure += tenureIncrement
                    cycleCount = 0

            if obj > min and ((100 * obj) / min) - 100 >= cutRange:
                tabuTenure = initialTenure
                cycleCount = 0
                sol = perturbaSolucaoSwapIndices(solMin, qtd=2)

    else:
        firstTime = time.time()
        iterCount = 0
        while time.time() - firstTime  < _maxTime:
            cycleCount += 1
            sol = estrategiaMelhorVizinhoNaoTabu(sol, tabuTable, tabuTenure, iterCount,
                                             bestValue)
            obj = objective(sol)

            #atualiza os minimos, quando atualiza, zera o contador
            #de ciclos, permitindo mais rodadas sem atualizar a tenure
            if obj < min:
                min = obj
                solMin = sol
                cycleCount = 0

            if doPlot:
                realSol = objective(removeEmptyDesks(sol))
                dataY.append(realSol)
                dataX.append(iterCount)

            if obj < bestValue:
                bestValue = obj
                bestSolution = sol
            else:
                if cycleCount >= cycleRange:
                    tabuTenure += tenureIncrement
                    cycleCount = 0

            if obj > min and ((100 * obj) / min) - 100 >= cutRange:
                tabuTenure = initialTenure
                cycleCount = 0
                sol = perturbaSolucaoSwapIndices(solMin, qtd=2)
            
            iterCount += 1

    if doPlot:
        plt.plot(dataX, dataY)
        plt.show()

    return removeEmptyDesks(bestSolution)

def tabuComGulosoK():
    solucao = gulosoK(k = 3)
    return buscaTabu(solucao, tabuTenure=4)

def tabuComConstrucaoRepetida():
    solucao = construcaoRepetida(repeat=6)
    return buscaTabu(solucao)

def randomRestartComGulosoK(solucao = False, reestarts=10, doPlot = False):
    if not solucao:
        sol = gulosoK(full=True, k=2)
    else:
        sol = solucao.copy()

    bestSolution = sol
    bestValue = objective(sol)

    reestartCount = 0

    pX = []
    pY = []

    cont = 0
    while reestartCount < reestarts:
        newSol = buscaLocalSimplesMM(sol)
        obj = objective(newSol)
        if doPlot:
            pX.append(cont)
            pY.append(obj)
        if obj < bestValue:
            bestValue = obj
            sol = newSol
            bestSolution = sol
        else:
            sol = gulosoK(full=True, k=2)
            reestartCount += 1

        cont += 1
    if doPlot:
        plt.plot(pX, pY)
        plt.show()

    return removeEmptyDesks(bestSolution)


testInstance()
