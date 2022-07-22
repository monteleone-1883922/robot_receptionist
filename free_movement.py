from robot_cmd_ros import *
import math
from random import randint

from vision import findChairs

from classi import Map,GlobalData

from classi import Position as Pos







#random mapping----------------------------------------------------------------------------------------------

def randomMapping(bBox,dim,movements):
    """
    inputs: 
    bBox is a touple that contains the size of the map, for example 2x3 = (2,3). Size is expressed in meters.
    dim is the dimension of the cell of the map, for example dim = 0.5 the cell size is 0.5x0.5 . Size is expressed in meters.
    movements is the number of movements the robot should do until it stops

    outputs:
    pos is the position where the robot is
    map is the map

    it makes the robot moving randomly in the map looking for chairs and trying not to go again to the same cell
    """
    glob = GlobalData.createGlobalData()
    glob.diedcell-=1
    map = Map(bBox,dim)
    pos = map.middlePos()
    gira=0
    
    while gira<movements:
        m = glob.diedcell+1
        sceglidir=True
        count=0
        dir = Pos(0,0)
        retry = True
        while sceglidir:
            dir = takeDirection(map,pos)
            
            m = min(m,map.predictLookup(map,pos,dir))
            if m == -1 or count == glob.tries  :
                if m != glob.diedcell:
                    sceglidir = False
                elif retry: 
                    count=0
                    retry = False
                else:
                    say("mapping complete")
                    return map,pos

            count += 1
        #say("going to " + str( pos[0]+dir[0]) +str( pos[1]+dir[1]))
        moveRobot(dir,dim)
        
        updateMapAndPos(map,pos,dir)
        gira+=1
    #return to hall
    say("mapping complete")
    return map,pos


def updateMapAndPos(map,pos,dir):
    pos.tryUpdate(dir,False)
    pos.update()
    map.addVal(pos,1)
    
#rimanere in mappa
def moveRobot(dir,dim):
    #sinistra
    if dir.x ==0   and dir.y  ==1    :
        left(1)
        forward(dim)
    #destra
    elif dir.x ==0   and dir.y  == -1     :
        right(1)
        forward(dim)
    #avanti
    elif dir.x == 1  and dir.y  == 0    :
        forward(dim)
    #indietro
    elif dir.x == -1  and dir.y  == 0    :
        right(2)
        forward(dim)
    #alto sinistra
    elif dir.x == 1  and dir.y  == 1     :
        left(0.5)
        forward(dim*math.sqrt(2))
    #alto destra
    elif dir.x ==  1 and dir.y  ==  -1   :
        right(0.5)
        forward(dim*math.sqrt(2))
    #basso sinistra
    elif dir.x ==  -1 and dir.y  ==  1   :
        left(1.5)
        forward(dim*math.sqrt(2))
    #basso destra
    elif dir.x ==  -1 and dir.y  ==  -1   :
        right(1.5)
        forward(dim*math.sqrt(2))




def takeDirection(map,pos):
    a,b,c,d = possibleDir(map,pos)
    while 1:
        x = randint(a,b)
        y = randint(c,d)
        if x+y != 0:
            return Pos(x,y)

def possibleDir(map,pos):
    a=-1
    b=1
    c=-1
    d=1

    if map.n <= pos.x + 1:
        b=0
    if 0 > pos.x -1:
        a=0
    if map.m <= pos.y +1:
        d=0
    if 0 > pos.y -1:
        c=0
    return a,b,c,d


# mapping sistematico senza ostacoli---------------------------------------------------------------------------------------

def freeSistematicMapping(bBox,dim,directions):
    """
    inputs: 
    bBox is a touple that contains the size of the map, for example 2x3 = (2,3). Size is expressed in meters.
    dim is the dimension of the cell of the map, for example dim = 0.5 the cell size is 0.5x0.5 . Size is expressed in meters.
    directions is the number of directions where the robot should look at searching for chairs

    outputs:
    pos is the position where the robot is
    map is the map

    it makes the robot moving through every cell of the map looking for chairs at every step
    """
    map=Map(bBox,dim)
    c = -1
    for j in range(map.m):
        for i in range(map.n-1):
            forward(dim)
            findChairs(directions)
        c *= -1
        if j != map.m -1 :
            turn(90*c)
            forward(dim)
            findChairs(directions)
            turn(90*c)
    
    if map.m % 2 == 0:
        pos = Pos(0,map.m-1)
    else:
        pos = Pos(map.n-1,map.m-1)
    say("mapping complete")

    return map,pos

#movimento senza ostacoli--------------------------------------------------------------------------------------------------------------


def freeMoveTo(map,src,trg):
    
   if not map.validCell(src) or not map.validCell(trg):
      raise Exception("src or trg not in map")
   if src.x != trg.x and src.y != trg.y:
      dir= findDiag(src,trg)
      n = min(abs(src.x - trg.x),abs(src.y - trg.y))
      turn(dir, ref ="ABS")
      forward(n*map.dim * math.sqrt(2))
      updateSrc(src,trg,n)
   dir,n = findDir(src,trg)
   turn(dir,ref ="ABS")
   forward(n*map.dim)
      

def updateSrc(src,trg,n):
    a = trg.x - src.x
    b = trg.y - src.y
    src.tryUpdate(src.x + n * a/abs(a), src.y + n * b/abs(b) ,False)
    src.update()


def findDiag(src,trg):
   c=1
   d=0
   if src.x > trg.x:
      d=180
      c=-1
    #destra
   if src.y > trg.y:
      d+= c*-45
    #sinistra
   else :
      d+= c*45
   return d
      
def findDir(src,trg):
   a=0
   b=0
   if src.y == trg.y:
      a = src.x - trg.x
      if a > 0:
         b=180
   else :
      a = src.y - trg.y
      #destra
      if a > 0:
         b=-90
      #sinistra
      else:
         b=90
   return b,abs(a)
   