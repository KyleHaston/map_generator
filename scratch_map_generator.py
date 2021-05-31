# map generator
# may 31, 2021

# ----- charset -----
# . water
# 0 land
# * rock
# ^ tree
# 1 abandoned house
# 2 abandoned factory
# 3 abandoned vehicle
# & lootbox
# | road
# - road
# └ road
# ┘ road
# ┌ road
# ┐ road
# ┴ road
# ┬ road
# ├ road
# ┤ road

import random

def makeLand(inSize):
    print('    making land...')
    return ['0'*inSize]*inSize

def addRocks(inMap):
    print('    adding rocks...')
    tempMap = ['']*len(inMap[0])
    for row in range(len(inMap[0])):
        for tile in inMap[row]:
            if random.randint(0,100) <= 30:  # change this comparison to generate more or less
                tempMap[row] += '*'
            else:
                tempMap[row] += tile
    return tempMap

def addTrees(inMap):
    print('    adding trees...')
    tempMap = [''] * len(inMap[0])
    for row in range(len(inMap[0])):
        for tile in inMap[row]:
            if random.randint(0, 100) <= 40:  # change this comparison to generate more or less
                tempMap[row] += '^'
            else:
                tempMap[row] += tile
    return tempMap

def addIntersections(inMap):
    print('        adding intersections...')
    intersections = '┴┬├┤'
    tempMap = ['' * len(inMap[0])] * len(inMap[0])
    for row in range(len(inMap[0])):
        for col in range(len(inMap[0])):
            if random.randint(0, 100) <= 2:  # change this comparison to generate more or less
                # don't put intersections right next to each other
                nearbyTiles = ''
                if 0 < row:
                    for x in range(row):
                        nearbyTiles += tempMap[x][col]
                if 0 < col:
                        nearbyTiles += tempMap[row][:]
                intersectionNearby = False
                for c in nearbyTiles:
                    if c in intersections:
                        intersectionNearby = True
                        break
                if intersectionNearby:
                    tempMap[row] += inMap[row][col]
                else:
                    tempMap[row] += intersections[random.randint(0, len(intersections)-1)]
            else:
                tempMap[row] += inMap[row][col]
    return tempMap

def growE(inMap):
    growToE = '-┘┐'
    tempMap = [''] * len(inMap[0])
    for row in range(len(inMap[0])):
        for col in range(len(inMap[0])):
            if 0 < col and tempMap[row][col-1] in '┬┴├-┌└' and random.randint(0, 100) <= 95:  # can grow to E
                if (0 < row) and (tempMap[row-1][col] in '-┬┤├|┌┐'):  # if we can connect N, do it.
                    tempMap[row] += '┘'
                else:
                    if random.randint(0, 100) <= 90:  # generate more straight roads than not
                        tempMap[row] += '-'
                    else:
                        tempMap[row] += growToE[random.randint(0, len(growToE)-1)]
            else:
                tempMap[row] += inMap[row][col]
    return tempMap

def growS(inMap):
    growToS = '|└┘'
    tempMap = [''] * len(inMap[0])
    for row in range(len(inMap[0])):
        for col in range(len(inMap[0])):
            if 0 < row and tempMap[row-1][col] in '|┬┤├┐┌' and \
               5 < col and '|' not in tempMap[row][col-5:col]:  # and random.randint(0, 100) <= 98:
                if 0 < col and tempMap[row][col-1] in '-┌└┬┴├|':  # connect to something from W if possible
                    tempMap[row] += '┘'
                elif col < (len(inMap[0])-1) and inMap[row][col+1] in '-┘┐┬┴┤':  # turn road toward E if something is there
                    tempMap[row] += '└'
                else:
                    if random.randint(0, 100) <= 90:  # generate more straight roads than not
                        tempMap[row] += '|'
                    else:
                        tempMap[row] += growToS[random.randint(0, len(growToS)-1)]
            else:
                tempMap[row] += inMap[row][col]
    return tempMap


def growFromIntersections(inMap):
    print('        pathing away from intersections...')
    growToN = '|┌┐'
    growToE = '-┘┐'
    growToS = '|└┘'
    growToW = '-└┌'
    tempMap = growE(inMap)
    tempMap = growS(tempMap)

    return tempMap

def addRoads(inMap):
    print('    adding roads...')
    tempMap = addIntersections(inMap)
    tempMap = growFromIntersections(tempMap)
    return tempMap

def addAbandonedBuildings(inMap):
    print('    adding abandoned bldgs...')
    tempMap = [''] * len(inMap[0])
    site = '-------'  # wherever this occurs on the map, we'll add bldgs.
    for row in range(len(inMap[0])):
        if 0 < row < (len(inMap[0]) - 1) and (site in inMap[row + 1]):  # and random.randint(0, 100) <= 20:
            idx = inMap[row + 1].index(site)
            tempMap[row] += inMap[row][:idx]

            # pick we're adding factories or houses (assuming they wouldn't be next to each other)
            if random.randint(0, 100) < 50:  # add factories & vehicles
                bldgs = '23'
            else:  # add houses & vehicles
                bldgs = '13'
            for i in range(len(site)):
                if inMap[row][idx+i] not in '┴┬├┤-|┌└┘┐':  # don't build over roads
                    tempMap[row] += bldgs[random.randint(0, len(bldgs)-1)]
                else:
                    tempMap[row] += inMap[row][idx+i]
            tempMap[row] += inMap[row][(idx+len(site)):]
        else:
            tempMap[row] += inMap[row]
    return tempMap

def addAbandonedVehicles(inMap):
    print('    adding abandoned vehicles...')
    return inMap

def addLootBoxes(inMap):
    print('    adding loot boxes...')
    tempMap = ['' * len(inMap[0])] * len(inMap[0])
    for row in range(len(inMap[0])):
        for tile in inMap[row]:
            # don't disrupt roads with lootboxes
            if tile in ['0','*','^'] and random.randint(0, 500) <= 1:  # change this comparison to generate more or less
                tempMap[row] += '&'
            else:
                tempMap[row] += tile
    return tempMap

def writeOut(inMap):
    print('    writing to output file...')
    filename = 'output.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        # f.writelines(inMap)
        for line in inMap:
            print(line)
            f.write(line + '\n')
        print('        finished writing: ' + filename)

if __name__ == "__main__":
    size = 512
    map = makeLand(size)
    map = addRocks(map)
    map = addTrees(map)
    map = addRoads(map)
    map = addAbandonedBuildings(map)
    map = addAbandonedVehicles(map)
    map = addLootBoxes(map)
    writeOut(map)
