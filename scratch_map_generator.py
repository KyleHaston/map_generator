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
            if random.randint(0,100) <= 10:  # change this comparison to generate more or less
                tempMap[row] += '*'
            else:
                tempMap[row] += tile
    return tempMap

def addTrees(inMap):
    print('    adding trees...')
    tempMap = [''] * len(inMap[0])
    for row in range(len(inMap[0])):
        for tile in inMap[row]:
            if random.randint(0, 100) <= 10:  # change this comparison to generate more or less
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
                if 0 < col < (len(inMap[0])-2) and tempMap[row][col-1] in '-┌└┬┴├|' and inMap[row][col+1] not in '-┘┐┬┴┤|':  # connect to something from W if possible
                    tempMap[row] += '┘'
                elif 0 < col < (len(inMap[0])-2) and tempMap[row][col-1] in '-┌└┬┴├|' and inMap[row][col+1] in '-┘┐┬┴┤|':  # connect to something from W if possible
                    tempMap[row] += '┴'
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

def addHouses(inMap):
    print('    adding abandoned houses and vehicles...')
    tempMap = [''] * len(inMap[0])
    site = '----------'  # wherever this occurs on the map, we'll add bldgs.
    for row in range(len(inMap[0])):
        if 0 < row < (len(inMap[0]) - 1) and (site in inMap[row + 1]):  # and random.randint(0, 100) <= 20:
            idx = inMap[row + 1].index(site)
            tempMap[row] += inMap[row][:idx]
            # add houses, vehicles, and empty spaces
            bldgs = '130'
            for i in range(len(site)):
                if inMap[row][idx+i] not in '┴┬├┤-|┌└┘┐':  # don't build over roads
                    tempMap[row] += bldgs[random.randint(0, len(bldgs)-1)]
                else:
                    tempMap[row] += inMap[row][idx+i]
            tempMap[row] += inMap[row][(idx+len(site)):]
        else:
            tempMap[row] += inMap[row]
    return tempMap

def addFactories(inMap):
    print('    adding abandoned factories...')
    tempMap = [''] * len(inMap[0])
    builtFactory = 0  # goes true when we place one. needed to get indexing right.
    for row in range(len(inMap[0])):
        if builtFactory == 2 or builtFactory == 1:
            builtFactory -= 1
            continue
        for col in range(len(inMap[0])):
            if row < (len(inMap[0])-6) and col > 6 and inMap[row][col] == '|' and inMap[row+1][col] == '|'and inMap[row+2][col] == '|' and random.randint(0, 100) <= 10:
                tempMap[row] = inMap[row][:col-3] + '444' + inMap[row][col:]
                tempMap[row+1] = inMap[row+1][:col - 3] + '424' + inMap[row+1][col:]
                tempMap[row+2] = inMap[row+2][:col - 3] + '444' + inMap[row+2][col:]
                builtFactory = 2
            else:
                tempMap[row] += inMap[row][col]
            if builtFactory == 2:
                break  # done with this row
    return tempMap

def addLootBoxes(inMap):
    print('    adding loot boxes...')
    tempMap = [''] * len(inMap[0])
    for row in range(len(inMap[0])):
        for tile in inMap[row]:
            # don't disrupt roads with lootboxes
            if tile in ['0','*','^'] and random.randint(0, 500) <= 1:  # change this comparison to generate more or less
                tempMap[row] += '&'
            else:
                tempMap[row] += tile
    return tempMap

def transposeMap(inMap):
    tempMap = [''] * len(inMap[0])
    for row in range(len(inMap[0])):
        for col in range(len(inMap[0])):
            tempMap[row] += inMap[col][row]
    return tempMap

def addWaterLeftRight(inMap, inWaterBorder):
    tempMap = [''] * len(inMap[0])
    leftTideLine = random.randint(0,2*inWaterBorder)
    rightTideLine = random.randint(0,2*inWaterBorder)
    for row in range(len(inMap[0])):
        # x = (a if b else 0)
        leftTideLine = (leftTideLine + random.randint(-2,2)) if leftTideLine >= inWaterBorder else inWaterBorder
        leftTideLine = leftTideLine if leftTideLine <= inWaterBorder*2 else inWaterBorder*2
        rightTideLine = (rightTideLine + random.randint(-2,2)) if rightTideLine >= inWaterBorder else inWaterBorder
        rightTideLine = rightTideLine if rightTideLine <= inWaterBorder * 2 else inWaterBorder * 2
        for col in range(len(inMap[0])):
            if col < (inWaterBorder + leftTideLine) or col > (len(inMap[0])-(inWaterBorder+1)-rightTideLine):
                tempMap[row] += '.'
            else:
                tempMap[row] += inMap[row][col]
    return tempMap

def addWater(inMap):
    print('    adding water...')
    waterBorder = 4  # change this to have more/less tiles of water around the edges
    tempMap = addWaterLeftRight(inMap, waterBorder)
    tempMap = transposeMap(tempMap)
    tempMap = addWaterLeftRight(tempMap, waterBorder)
    tempMap = transposeMap(tempMap)
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
    size = 140
    map = makeLand(size)
    map = addRocks(map)
    map = addTrees(map)
    map = addRoads(map)
    map = addLootBoxes(map)
    map = addWater(map)
    map = addHouses(map)
    map = addFactories(map)
    writeOut(map)
