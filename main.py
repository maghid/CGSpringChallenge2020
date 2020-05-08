import sys
import math
import random
import itertools
import copy

# Grab the pellets as fast as you can!

# Classes

def printError(errorString):
    print(errorString, file=sys.stderr)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y  
    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y)
    def __str__(self):
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = []

class Pac:
    def __init__(self, id, mine, x, y, type_id, speed_turns_left, ability_cooldown):
        self.id = id
        self.mine = mine
        self.lastPos = Position(-1,-1)
        self.currentPos = Position(x,y)
        self.typeId = type_id
        self.speedTurnsLeft = speed_turns_left
        self.abilityCooldown = ability_cooldown
        self.visible = True

class Pellet:
    def __init__(self, x, y, value):
        self.pos = Position(x,y)
        self.value = value

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
printError("width: " + str(width) + " ,height: " + str(height))
gameGrid = Grid(width, height)
for i in range(height):
    #row = input()  # one line of the grid: space " " is floor, pound "#" is wall
    gameGrid.rows.append(input())

def getManhattanDistance(x1,x2,y1,y2):
    return abs(x1-x2) + abs(y1-y2)

def findClosestPellet(pacX,pacY,pellets,superpellets):
    destination = (-1,-1)
    shortestDistance = None
    if (not superpellets):
        for p in pellets:
            distance = getManhattanDistance(pacX,pacY,p.pos.x,p.pos.y)
            if (shortestDistance is None or distance < shortestDistance):
                shortestDistance = distance
                destination = (p.pos.x, p.pos.y)
                pellets.remove(p)
    else:
         for p in superpellets:
            distance = getManhattanDistance(pacX,pacY,p.pos.x,p.pos.y)
            if (shortestDistance is None or distance < shortestDistance):
                shortestDistance = distance
                destination = (p.pos.x, p.pos.y)     
                superpellets.remove(p)
    return destination

def detectCollisions(visiblePacs):
    pacsInCollision = set()
    for pac in visiblePacs:
        if (pac.mine): printError("pac id: " + str(pac.id) + ", current pos: " + str(pac.currentPos) + ", lastPos: " + str(pac.lastPos))
        if (pac.currentPos == pac.lastPos):
            if (pac.mine): pacsInCollision.add(pac.id)
    return pacsInCollision

def chooseRandomDirection(x,y):
    possibleMoves = []
    #UP
    if (gameGrid.rows[(y+1)%(height-1)][x] != '#'):
        possibleMoves.append((x,(y+1)%(height-1)))
    #DOWN
    if (gameGrid.rows[(y-1)%(height-1)][x] != '#') :
        possibleMoves.append((x,(y-1)%(height-1))) 
    #LEFT
    if (gameGrid.rows[y][(x-1)%(width-1)] != '#') :
        possibleMoves.append(((x-1)%(width-1),y)) 
    #RIGHT
    if (gameGrid.rows[y][(x+1)%(width-1)] != '#') :
        possibleMoves.append(((x+1)%(width-1),y))
    return random.choice(possibleMoves)

visiblePacs = []
# game loop
while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
        found = False
        for p in visiblePacs:
            if (pac_id == p.id and mine == p.mine):
                p.lastPos = copy.deepcopy(p.currentPos)
                p.currentPos.x = x
                p.currentPos.y = y
                p.speedTurnsLeft = speed_turns_left
                p.abilityCooldown = ability_cooldown
                found = True
                break
        if (not found):
            pac = Pac(pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown)
            visiblePacs.append(pac)

    visible_pellet_count = int(input())  # all pellets in sight
    visiblePellets = []
    visibleSuperPellets = []
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        pellet = Pellet(x, y, value)
        if (value == 10):
            visibleSuperPellets.append(pellet)
        else:
            visiblePellets.append(pellet)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    allMovesString = None
    pacsInCollision = detectCollisions(visiblePacs)
    printError("Pacs in collision: " + str(pacsInCollision))
    for pac in visiblePacs:
        if (pac.mine):
            if (pac.id in pacsInCollision):
                nextPos = chooseRandomDirection(pac.currentPos.x, pac.currentPos.y)
                singleMoveString = 'MOVE ' + str(pac.id) + ' ' + str(nextPos[0]) + " " + str(nextPos[1])
                if (allMovesString is not None):
                    allMovesString += ' | ' + singleMoveString
                else:
                    allMovesString = singleMoveString
            else:
                # Find closest pellet and move to it
                nextPos = findClosestPellet(pac.currentPos.x, pac.currentPos.y, visiblePellets, visibleSuperPellets)
                singleMoveString = 'MOVE ' + str(pac.id) + ' ' + str(nextPos[0]) + " " + str(nextPos[1])
                if (allMovesString is not None):
                    allMovesString += ' | ' + singleMoveString
                else:
                    allMovesString = singleMoveString
    
    print(allMovesString)

    # MOVE <pacId> <x> <y>  
    #print("MOVE 0 15 10")