import sys
import math
import random

# Grab the pellets as fast as you can!

# Classes
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = []

class Pac:
    def __init__(self, id, mine, x, y, type_id, speed_turns_left, ability_cooldown):
        self.id = id
        self.mine = mine
        self.x = x
        self.y = y
        self.typeId = type_id
        self.speedTurnsLeft = speed_turns_left
        self.abilityCooldown = ability_cooldown

class Pellet:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
gameGrid = Grid(width, height)
for i in range(height):
    #row = input()  # one line of the grid: space " " is floor, pound "#" is wall
    gameGrid.rows.append(input())

def getEuclideanDistance(x1,x2,y1,y2):
    return math.sqrt(((x1-x2)**2)+((y1-y2)**2))

def getManhattanDistance(x1,x2,y1,y2):
    return abs(x1-x2) + abs(y1-y2)

def findClosestPellet(pacX,pacY,pellets,superpellets):
    destination = (-1,-1)
    shortestDistance = None
    if (not superpellets):
        for p in pellets:
            distance = getManhattanDistance(pacX,pacY,p.x,p.y)
            if (shortestDistance is None or distance < shortestDistance):
                shortestDistance = distance
                destination = (p.x, p.y)
    else:
         for p in superpellets:
            distance = getManhattanDistance(pacX,pacY,p.x,p.y)
            if (shortestDistance is None or distance < shortestDistance):
                shortestDistance = distance
                destination = (p.x, p.y)     
    return destination

# game loop
while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    visiblePacs = []
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
    for pac in visiblePacs:
        if (pac.mine):
            # Find closest pellet and move to it
            nextPos = findClosestPellet(pac.x, visiblePacs[0].y, visiblePellets, visibleSuperPellets)
            # x and y are inverted
            print('MOVE 0 ' + str(nextPos[0]) + " " + str(nextPos[1]))


    # MOVE <pacId> <x> <y>  
    #print("MOVE 0 15 10")
