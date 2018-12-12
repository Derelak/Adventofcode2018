import os
import re
import numpy

# print('hello world')


##### Part 1 #####
                                                # Creat path to InputData
filename = os.path.abspath(os.path.join("data", "InputData"))

# print(filename)

fin = open(filename, 'r')                       # Read InputData-file

entries = []
#entries = [[1, 1], [1,6], [8,3], [3,4], [5,5], [8,9]]

for line in fin:                                # Put input data in list, remove trash
    line = re.sub(' ', '', line)
    part = line.strip().split(',')
    entries.append(part)

coordinates = numpy.zeros([len(entries), 2])    # Creating empty coordinate matrix

for i in range(0, len(entries)):                # Inserting coordinates in matrix
    coordinates[i, 0] = int(entries[i][0])
    coordinates[i, 1] = int(entries[i][1])


minX = int(min(coordinates[:, 0]))              # Finding smallest coordinate
minY = int(min(coordinates[:, 1]))


# print(minX, minY)

shiftedcoordinates = coordinates.copy()         # Shift coordinates to make lowest coordinate (0,0)
shiftedcoordinates[:, 0] = shiftedcoordinates[:, 0] - minX
shiftedcoordinates[:, 1] = shiftedcoordinates[:, 1] - minY

# print(shiftedcoordinates)


maxX = int(max(shiftedcoordinates[:, 0]))+1     # Find coordinate range
maxY = int(max(shiftedcoordinates[:, 1]))+1

# print(maxX, maxY)

area = numpy.zeros([maxY, maxX])                # Create area matrix containing zeros with the same size as coordinate range

for i in range(0, maxY):                        # Go through area matrix, for each element find closest coordinate,
    for j in range(0, maxX):                    # put the coordinate-ID (1,2,...) for the closest coordinate as matrix element
        dist=maxY+maxX                          # If same distans for multiple coordinates put zero as matrix element
        for k in range(0, len(entries)):
            tempDist = abs(i-shiftedcoordinates[k][1]) + abs(j-shiftedcoordinates[k][0])
            if tempDist < dist:
                area[i, j] = k + 1
                dist = tempDist
            elif tempDist == dist:
                area[i, j] = 0

# print(area)

edgelist = []
for i in range(0,maxY):                         # Create list with all coordinate-IDs at the edges
    if area[i,0] not in edgelist:
        edgelist.append(area[i,0])
    if area[i,maxX-1] not in edgelist:
        edgelist.append(area[i,maxX-1])
for i in range(0,maxX):
    if area[0,i] not in edgelist:
        edgelist.append(area[0,i])
    if area[maxY-1,i] not in edgelist:
        edgelist.append(area[maxY-1,i])

# print(edgelist)

for i in range(0, len(edgelist)):               # Replace all coordinate_IDs bordering an edge with zeros
    area[area == edgelist[i]] = 0

# print(area)
                                                # Count number of elements for each ID, making a list with (ID, amount)
unique = numpy.asarray((numpy.unique(area, return_counts=True))).T

# print(unique)

unique=numpy.delete(unique, 0, 0)               # Remove row with ID=0

# print(unique)

y, x = numpy.where(unique == max(unique[:,1]))  # Find ID (y) with most element (x)

print('Largest area is ', unique[y,x], 'for coordinate', coordinates[int(unique[y,0])-1])


####### Part 2 #######

area = numpy.zeros([maxY, maxX])                # Create new area matrix containing zeros with the same size as coordinate range

for i in range(0, maxY):                        # Calculate total distance to all coordinates for each area element,
    for j in range(0, maxX):                    # If below threshold set area element = 1
        distsum=0
        for k in range(0, len(entries)):
            distsum = distsum + abs(i - shiftedcoordinates[k][1]) + abs(j - shiftedcoordinates[k][0])
        if distsum < 10000:
            area[i,j] = 1

# print(area)

ones = numpy.count_nonzero(area)                # Count elements != 0

print('The area is', ones)