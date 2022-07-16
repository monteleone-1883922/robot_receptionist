
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







def tryRight(err,map,pos):
    right(1)
    if map.validCell(pos) and obstacle_distance() > map.dim + err and map.lookup(pos) >= 0 :
        return True
    if map.validCell(pos) and obstacle_distance() <= map.dim + err:
        map.updateCell(pos,-3)
    left(1)

def tryForward(err,map,pos,backward):
    val= map.lookup(pos)
    if map.validCell(pos) and obstacle_distance() > map.dim + err and (val >= 0 or  (val==-1 and backward)):
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

def obstacleMoveTo(map,dim,src,trg):
    mapUpdate(map,trg,0)
    cell=trg
    visitati = {trg}
    i=0
    val=0
    visitare=[]
    while addNeighbours(cell,src,map,visitati,visitare,val):
        cell=visitare[i]
        val = obstacleMapLookup(map,cell)
        i+=1
    obstacleMoveRobot(map,src,dim)


def obstacleMoveRobot(map,pos,dim):
    n,m = getMapDim(map)
    numCelle=n*m 
    p = numCelle
    s=0
    while p != 0:
        dir, p, pos = findDirection(map,pos,numCelle)
        turn(dir,ref = "ABS")
        if dir%90 == 0:
            s=dim
        else:
            s=dim*math.sqrt(2)
        forward(s)
        



def findDirection(map,pos,numCelle):
    m=numCelle+1
    dir=0
    newpos = pos
    for i in range(-1,2):
        for j in range(-1,2):
            cella = (pos[0]+i,pos[1]+j)
            val = obstacleMapLookup(map,cella)
            if val >=0 and val < m and i*i + j*j != 2:
                m=val
                dir = getDir(i,j)
                newpos = (pos[0]+i,pos[1]+j)
    return dir,m ,newpos


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
    mapDim=getMapDim(map)
    for i in range(-1,2):
        for j in range(-1,2):
            cella = (cell[0]+i,cell[1]+j)
            if validCell(cella,mapDim,visitati) and i*i + j*j != 2:
                
                if compareCell(cella,pos):
                    return False
                mapUpdate(map,cella,val+1)
                visitare.append(cella)
                visitati.add(cella)
                
    return True

def mapUpdate(map,cella,val):
    map[cella[0]][cella[1]] = val


def compareCell(a,b):
    return a[0] == b[0] and a[1] == b[1]

#eliminare spostamenti diagonali
def validCell(cell,mapDim,visitati):
    return (cell not in visitati) and cell[0]>=0 and cell[1]>=0 and cell[0] < mapDim[0] and cell[1] < mapDim[1] and map[cell[0]][cell[1]] != -3

def getMapDim(map):
   return len(map), len(map[0])

