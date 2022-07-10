
import math

from robot_cmd_ros import *

from free_movement import mapCreate

# mapping sistematico con ostacoli-------------------------------------------------------------------------------------------------
def obstacleSistematicMapping(bBox,dim):
    map=mapCreate(bBox,dim)
    mapping = True
    while mapping:







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
            if val >=0 and val < m:
                m=val
                dir = getDir(i,j)
                newpos = (pos[0]+i,pos[1]+j)
    return dir,m ,newpos


def getDir(a,b):
    if a ==0   and b  ==1    :
        return 90
    elif a ==0   and b  ==-1    :
        return -90   
    elif a ==1   and b  ==0    :
        return 0
    elif a ==-1   and b  ==0    :
        return 180
    elif a ==1   and b  ==1    :
        return 45
    elif a ==1   and b  ==-1    :
        return -45
    elif a ==-1   and b  ==1    :
        return 135
    elif a ==-1   and b  ==-1    :
        return -135






def obstacleMapLookup(map,pos):
    return map[pos[0]][pos[1]]


def addNeighbours(cell,pos,map,visitati,visitare,val):
    mapDim=getMapDim(map)
    for i in range(-1,2):
        for j in range(-1,2):
            cella = (cell[0]+i,cell[1]+j)
            if validCell(cella,mapDim,visitati):
                
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

