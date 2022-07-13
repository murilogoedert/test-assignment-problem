
import sys, re, numpy

def readInstance():
    file = open(sys.argv[1])
    lines = file.readlines()
    sub = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', ' ', lines[0])));
    instanceParts = sub.split(' ')

    numNodes = int(instanceParts[0])
    numEdges = int(instanceParts[1])
    numTests = int(instanceParts[2])
    numEmptyDesks = int(instanceParts[3])

    countLines = 0
    desks = []

    while(countLines < numNodes):
        desks.append(int(lines[countLines + 1]))
        countLines += 1

    distanceMatrix = numpy.full((numNodes, numNodes), 0, dtype=float)

    countLines += 1

    while(countLines < (numEdges + numNodes + 1)):
        currentLine = lines[countLines]
        lineParts = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', '', currentLine))).split(' ');
        i = desks.index(int(lineParts[0]))
        j = desks.index(int(lineParts[1]))
        value = float(lineParts[2])
        distanceMatrix[i][j] = value
        countLines += 1

    similarityMatrix = numpy.full((numTests, numTests), 0, dtype=float)

    while(countLines < numEdges + numNodes + 1 + (numTests * 2)):
        currentLine = lines[countLines]
        lineParts = re.sub(' +', ' ', re.sub('\n', '', re.sub('\t', '', currentLine))).split(' ');
        i = int(lineParts[0])
        j = int(lineParts[1])
        value = float(lineParts[2])
        similarityMatrix[i][j] = value
        countLines += 1

    return numNodes, numEdges, numTests, numEmptyDesks, distanceMatrix, similarityMatrix;

    

print(readInstance())

#  python .\test-allocation.py instances/lab1_2x10.txt 


    