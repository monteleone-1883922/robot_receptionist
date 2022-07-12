
import math
from marrtino_apps.program.robot_receptionist.free_movement import mapLookup

from robot_cmd_ros import *

from free_movement import mapCreate

# mapping sistematico con ostacoli-------------------------------------------------------------------------------------------------
def obstacleSistematicMapping(bBox,dim,err):
    map=mapCreate(bBox,dim)
    mapDim = getMapDim(map)
    pos = (0,0)
    mapping = True
    backward = False
    while mapping:
        if tryRight(dim,err,map,(pos[0], pos[1] + 1),mapDim):
            mapUpdate(map,(pos[0], pos[1] + 1),-1)
            forward(dim)
            if obstacleMapLookup(map,(pos[0], pos[1] + 1)) >= 0 :
                backward = False




        elif tryForward(dim,err,map,(pos[0] + 1, pos[1]),mapDim,backward):
            if obstacleMapLookup(map,(pos[0] + 1, pos[1])) == -1:
                mapUpdate(map,(pos[0] + 1, pos[1]),-2)
            else:
                if obstacleMapLookup(map,(pos[0] + 1, pos[1])) >= 0 :
                    backward = False
                mapUpdate(map,(pos[0] + 1, pos[1]),-1)
            forward(dim)


        elif tryLeft(dim,err,map,(pos[0], pos[1] - 1)):
            mapUpdate(map,(pos[0], pos[1] - 1),-1)
            forward(dim)
            if obstacleMapLookup(map,(pos[0], pos[1] - 1)) >= 0 :
                backward = False



        elif tryBackward(dim,err,map,pos,mapDim):
            backward = True
            mapUpdate(map,(pos[0], pos[1] - 1),-2)
            forward(dim)







def tryRight(dim,err,map,pos,mapDim):
    right(1)
    if pos[1] < mapDim[1] and obstacle_distance() > dim + err and obstacleMapLookup(map,pos) >= 0 :
        return True
    if pos[1] < mapDim[1] and obstacle_distance() <= dim + err:
        mapUpdate(map,pos,-3)
    left(1)

def tryForward(dim,err,map,pos,mapDim,backward):
    val= obstacleMapLookup(map,pos)
    if pos[0] < mapDim[0] and obstacle_distance() > dim + err and (val >= 0 or  (val==-1 and backward)):
        return True
    if pos[0] < mapDim[0] and obstacle_distance() <= dim + err:
        mapUpdate(map,pos,-3)

def tryLeft(dim,err,map,pos):
    
    left(1)
    if pos[1] >= 0 and obstacle_distance() > dim + err and obstacleMapLookup(map,pos) >= 0 :
        return True
    if pos[1] >= 0 and obstacle_distance() <= dim + err:
        mapUpdate(map,pos,-3)
    left(1)

def tryBackward(dim,err,map,pos):
    newpos = (pos[0]-1, pos[1])
    return newpos[0] >= 0 and obstacle_distance() > dim + err and obstacleMapLookup(map,newpos) >= 0


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

