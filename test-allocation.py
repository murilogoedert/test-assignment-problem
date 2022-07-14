
import sys, re, random

def readInstance():
    if(len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        file = open('instances/lab6b_2x20.txt')
        
    lines = file.readlines()
    sub = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', ' ', lines[0])));
    instanceParts = sub.split(' ')

    numDesks = int(instanceParts[0])
    numDistances = int(instanceParts[1])
    numTests = int(instanceParts[2])
    numEmptyDesks = int(instanceParts[3])

    countLines = 0
    desks = []

    while(countLines < numDesks):
        desks.append(int(lines[countLines + 1]))
        countLines += 1

    distanceMatrix = createMatrix(numDesks, numDesks, None)

    countLines += 1

    while(countLines < (numDistances + numDesks + 1)):
        currentLine = lines[countLines]
        lineParts = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', '', currentLine))).split(' ');
        i = desks.index(int(lineParts[0]))
        j = desks.index(int(lineParts[1]))
        value = float(lineParts[2])
        distanceMatrix[i][j] = value
        countLines += 1

    similarityMatrix = createMatrix(numTests, numTests)

    while(countLines < numDistances + numDesks + 1 + (numTests * 2)):
        currentLine = lines[countLines]
        lineParts = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', '', currentLine))).split(' ');
        i = int(lineParts[0])
        j = int(lineParts[1])
        value = float(lineParts[2])
        similarityMatrix[i][j] = value
        countLines += 1

    return desks, numDistances, numTests, numEmptyDesks, distanceMatrix, similarityMatrix

def createMatrix(lines, columns, defValue = 0):
    matrix = []
    for i in range(lines):
        line = []
        for j in range(columns):
            line.append(0)
        matrix.append(line)
    return matrix

def solucaoInicial(desks, numTests, numEmptyDesks):
    solution = []
    for i in range(len(desks)):
        solution.append(0)

    while solution.count(0) > numEmptyDesks:
        solution[random.randint(0, len(desks) - 1)] = random.randint(1, numTests)

    return solution
            
        
def avaliaSolucao(distanceMatrix, similarityMatrix, solution):
    totalCost = 0
    for i in range(len(solution) - 1):
        for j in range(i + 1, len(solution)):
            if(solution[i] != 0 and solution[j] != 0):
                totalCost += similarityMatrix[solution[i] - 1][solution[j] - 1] * distanceMatrix[i][j]

    
    return totalCost


def buscaLocal():
    desks, numDistances, numTests, numEmptyDesks, distanceMatrix, similarityMatrix = readInstance()
    solucaoAtual = solucaoInicial(desks, numTests, numEmptyDesks)
    print(avaliaSolucao(distanceMatrix, similarityMatrix, solucaoAtual))



buscaLocal()





#  python .\test-allocation.py instances/lab1_2x10.txt 


    