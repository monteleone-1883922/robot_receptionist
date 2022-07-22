
import math
#from marrtino_apps.program.robot_receptionist.free_movement import mapLookup

from robot_cmd_ros import *

from free_movement import mapCreate

from classi import Position as Pos
from classi import Map
from classi import Directions as Dir

# mapping sistematico con ostacoli-------------------------------------------------------------------------------------------------
def obstacleSistematicMapping(bBox,dim,err):
    map=Map(bBox,dim)
    #mapDim = getMapDim(map)
    #numCelle = mapDim[0] * mapDim[1]

    pos = Pos(0,0,0)
    map.updateCell(pos,-1)
    backward = False
    mapping = True
    count = 0
    while mapping:
        if count == map.numCelle:
            mapping=False
        elif tryRight(err,map,pos.tryUpdate(Dir.right)):
            count += 1
            pos.update()
            map.updateCell(pos,-1)
            forward(dim)
            if map.lookup(pos) >= 0 :
                backward = False




        elif tryForward(err,map,pos.tryUpdate(Dir.forward),backward):
            pos.update()
            if map.lookup(pos) == -1:
                map.updateCell(pos,-2)
            else:
                count += 1
                if map.lookup(pos) >= 0 :
                    backward = False
                map.updateCell(pos,-1)
            forward(dim)


        elif tryLeft(err,map,pos.tryUpdate(Dir.left)):
            count += 1
            pos.update()
            map.updateCell(pos,-1)
            forward(dim)
            if map.lookup(pos) >= 0 :
                backward = False



        elif tryBackward(err,map,pos.tryUpdate(Dir.backward)):
            backward = True
            map.updateCell(pos,-2)
            pos.update()
            map.updateCell(pos,-2)
            forward(dim)
        else:
            mapping = False
    return map,pos






def tryRight(err,map,pos):
    right(1)
    if map.validCell(pos) and obstacle_distance() > map.dim + err and map.lookup(pos) >= 0 :
        return True
    if map.validCell(pos) and obstacle_distance() <= map.dim + err:
        map.updateCell(pos,-3)
    left(1)

def tryForward(err,map,pos,backward):
    if map.validCell(pos) and obstacle_distance() > map.dim + err and (map.lookup(pos) >= 0 or  (map.lookup(pos)==-1 and backward)):
        return True
    if map.validCell(pos) and obstacle_distance() <= map.dim + err:
        map.updateCell(pos,-3)

def tryLeft(err,map,pos):
    
    left(1)
    if map.validCell(pos) and obstacle_distance() > map.dim + err and map.lookup(pos) >= 0 :
        return True
    if map.validCell(pos) and obstacle_distance() <= map.dim + err:
        map.updateCell(pos,-3)
    left(1)

def tryBackward(err,map,pos):
    return map.validCell(pos) and obstacle_distance() > map.dim + err and map.lookup(pos) >= -1


#movimento con ostacoli-------------------------------------------------------------------------------------------------------------

def obstacleMoveTo(map,src,trg):
    map.updateCell(trg,0)
    cell= trg.copy()
    visitati = {trg}
    i=0
    val=0
    visitare=[]
    #addneighbours deve arrivare a src partendo da trg
    while addNeighbours(cell,src,map,visitati,visitare,val):
        cell=visitare[i]
        val = map.lookup(cell)
        i+=1
    obstacleMoveRobot(map,src)


def obstacleMoveRobot(map,pos): 
    p = map.numCelle
    s=0
    while p != 0:
        p = findDirection(map,pos)
        turn(pos.th,ref = "ABS")
        if pos.th%90 == 0:
            s=map.dim
        else:
            s=map.dim*math.sqrt(2)
        forward(s)
        



def findDirection(map,pos):
    m=map.numCelle+1
    for i in range(-1,2):
        for j in range(-1,2):
            cella = pos.tryUpdate(Pos(i,j))
            val = map.lookup(cella)
            if val >=0 and val < m and i*i + j*j != 2:
                m=val
                pos.update()
                pos.th = getDir(i,j)
                
    return m 


def getDir(a,b):
    #sinistra
    if a ==0   and b  ==1    :
        return 90
    #destra
    elif a ==0   and b  ==-1    :
        return -90   
    #avanti
    elif a ==1   and b  ==0    :
        return 0
    #indietro
    elif a ==-1   and b  ==0    :
        return 180
    #alto sinistra
    elif a ==1   and b  ==1    :
        return 45
    #alto destra
    elif a ==1   and b  ==-1    :
        return -45
    #basso sinistra
    elif a ==-1   and b  ==1    :
        return 135
    #basso destra
    elif a ==-1   and b  ==-1    :
        return -135






def obstacleMapLookup(map,pos):
    return map[pos[0]][pos[1]]


def addNeighbours(cell,pos,map,visitati,visitare,val):
    
    for i in range(-1,2):
        for j in range(-1,2):
            cella = cell.tryUpdate(Pos(i,j))
            if validCell(cella,visitati) and i*i + j*j != 2:
                
                if cella == pos :
                    return False
                map.updateCell(cella,val+1)
                c = cella.copy()
                visitare.append(c)
                visitati.add(c)
                
    return True

def mapUpdate(map,cella,val):
    map[cella[0]][cella[1]] = val


def compareCell(a,b):
    return a[0] == b[0] and a[1] == b[1]



def validCell(cell,visitati):
    return (cell not in visitati) and map.validCell(cell) and map.lookup(cell) != -3

def getMapDim(map):
   return len(map), len(map[0])

