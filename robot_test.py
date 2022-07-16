# Write your robot program hereenable

import math
from random import randint



enableObstacleAvoidance(False)




#mapping randomico----------------------------------------------------------------------------------------------
def movimento1(bBox,dim,spostamenti,tentativi,diedcell):
    diedcell-=1
    map,pos,dummy = mapCreate(bBox,dim)
    gira=0
    say("i am in" + str(pos))
    while gira<spostamenti:
        m= diedcell+1
        sceglidir=True
        count=0
        dir = (0,0)
        retry = True
        while sceglidir:
            dir = takeDirection(map,pos)
            
            m = min(m,mapLookup(map,pos,dir))
            if m == -1 or count == tentativi  :
                if m != diedcell:
                    sceglidir = False
                elif retry: 
                    count=0
                    retry = False
                else:
                    say("mapping complete")
                    return dummy,pos

            count += 1
        say("going to " + str( pos[0]+dir[0]) +str( pos[1]+dir[1]))
        moveRobot(dir,dim)
        
        pos = updateMapAndPos(map,pos,dir)
        gira+=1
    #return to hall
    say("mapping complete")
    return dummy,pos



def visitaCompleta(map):
    for i in range (len(map )) :
        for j in range(len(map[0])):
            if map[i][j] == 0:
                return False
    return True     


def updateMapAndPos(map,pos,dir):
    p = (pos[0]+ dir[0],pos[1] + dir[1])
    map[p[0]][p[1]] += 1
    return p
#rimanere in mappa
def moveRobot(dir,dim):
    #sinistra
    if dir[0] ==0   and dir[1]  ==1    :
        turn(90,ref="ABS")
        forward(dim)
    #destra
    elif dir[0] ==0   and dir[1]  == -1     :
        turn(-90,ref="ABS")
        forward(dim)
    #avanti
    elif dir[0] == 1  and dir[1]  == 0    :
        turn(0,ref="ABS")
        forward(dim)
    #indietro
    elif dir[0] == -1  and dir[1]  == 0    :
        turn(180,ref="ABS")
        forward(dim)
    #alto sinistra
    elif dir[0] == 1  and dir[1]  == 1     :
        turn(45,ref="ABS")
        forward(dim*math.sqrt(2))
    #alto destra
    elif dir[0] ==  1 and dir[1]  ==  -1   :
        turn(-45,ref="ABS")
        forward(dim*math.sqrt(2))
    #basso sinistra
    elif dir[0] ==  -1 and dir[1]  ==  1   :
        turn(135,ref="ABS")
        forward(dim*math.sqrt(2))
    #basso destra
    elif dir[0] ==  -1 and dir[1]  ==  -1   :
        turn(-135,ref="ABS")
        forward(dim*math.sqrt(2))



    
def mapLookup(map,pos,dir):
    return map[pos[0]+ dir[0]][pos[1] + dir[1]]

def takeDirection(map,pos):
    a,b,c,d = possibleDir(map,pos)
    while 1:
        x = randint(a,b)
        y = randint(c,d)
        if x+y != 0:
            return x,y

def possibleDir(map,pos):
    a=-1
    b=1
    c=-1
    d=1

    if len(map) <= pos[0] + 1:
        b=0
    if 0 > pos[0] -1:
        a=0
    if len(map[0] ) <= pos[1] +1:
        d=0
    if 0 > pos[1] -1:
        c=0
    return a,b,c,d




def mapCreate(bBox,dim):
    map=[]
    n = int(bBox[0]//dim)
    m = int(bBox[1]//dim)
    for i in range(n):
        l=[]
        for j in range(m):
            l.append(-1)
        map.append(l)
    return map,(int(n//2),int(m//2)),(n,m)

# mapping sistematico senza ostacoli---------------------------------------------------------------------------------------

def movimento2(bBox,dim,directions):
    map,dummy,mapDim=mapCreate(bBox,dim)
    
    for j in range(mapDim[1]):
        for i in range(mapDim[0]-1):
            forward(dim)
            #findChairs(directions)
        if j != mapDim[1] -1 :
            left(1)
            forward(dim)
            #findChairs(directions)
            left(1)
    
    if mapDim[1] % 2 == 0:
        pos = (0,mapDim[1]-1)
    else:
        pos = (mapDim[0]-1,mapDim[1]-1)
    say("mapping complete")

    return mapDim,pos

#movimento senza ostacoli--------------------------------------------------------------------------------------------------------------


def freeMoveTo(mapDim,dim,src,trg):
   if src[0] != trg[0] and src[1] != trg[1]:
      dir= findDiag(src,trg)
      n= min(abs(src[0] - trg[0]),abs(src[1] - trg[1]))
      turn(dir, ref ="ABS")
      forward(n*dim * math.sqrt(2))
      src = updateSrc(src,trg,n)
   dir,n = findDir(src,trg)
   turn(dir,ref ="ABS")
   forward(n*dim)
      

def updateSrc(src,trg,n):
    a = trg[0] - src[0]
    b = trg[1] - src[1]
    return (src[0] + n * a/abs(a),src[1] + n * b/abs(b) )


def findDiag(src,trg):
   c=1
   d=0
   if src[0] > trg[0]:
      d=180
      c=-1
    #destra
   if src[1] > trg[1]:
      d+= c*-45
    #sinistra
   else :
      d+= c*45
   return d
      
def findDir(src,trg):
   a=0
   b=0
   if src[1] == trg[1]:
      a = src[0] - trg[0]
      if a > 0:
         b=180
   else :
      a = src[1] - trg[1]
      #destra
      if a > 0:
         b=-90
      #sinistra
      else:
         b=90
   return b,abs(a)

#right(1.5)

a,b=movimento1((1.5,1),0.5,5,6,2)

display(str(a) + " " + str(b))

freeMoveTo(a,0.5,b,(1,0))
# obstacle test ---------------------------------------------------------------------------------------------------------




 # mapping sistematico con ostacoli-------------------------------------------------------------------------------------------------
def obstacleSistematicMapping(bBox,dim,err):
    map=mapCreate(bBox,dim)
    mapDim = getMapDim(map)
    display(str(mapDim))
    numCelle = mapDim[0] * mapDim[1]
    pos = (0,0)
    mapping = True
    backward = False
    count = 0
    while mapping:
        say("movement " + str(count))
        if count == numCelle:
            mapping=False
        elif tryRight(dim,err,map,(pos[0], pos[1] + 1),mapDim):
            say("right")
            count += 1
            mapUpdate(map,(pos[0], pos[1] + 1),-1)
            forward(dim)
            if obstacleMapLookup(map,(pos[0], pos[1] + 1)) >= 0 :
                backward = False
            pos = (pos[0],pos[1]+1)




        elif tryForward(dim,err,map,(pos[0] + 1, pos[1]),mapDim,backward):
            say("forward")
            if obstacleMapLookup(map,(pos[0] + 1, pos[1])) == -1:
                mapUpdate(map,(pos[0] + 1, pos[1]),-2)
            else:
                count += 1
                if obstacleMapLookup(map,(pos[0] + 1, pos[1])) >= 0 :
                    backward = False
                mapUpdate(map,(pos[0] + 1, pos[1]),-1)
            forward(dim)


        elif tryLeft(dim,err,map,(pos[0], pos[1] - 1)):
            say("left")
            count += 1
            mapUpdate(map,(pos[0], pos[1] - 1),-1)
            forward(dim)
            if obstacleMapLookup(map,(pos[0], pos[1] - 1)) >= 0 :
                backward = False



        elif tryBackward(dim,err,map,pos,mapDim):
            say("backward")
            backward = True
            mapUpdate(map,(pos[0], pos[1] - 1),-2)
            forward(dim)
        else:
            mapping = False







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
    return newpos[0] >= 0 and obstacle_distance() > dim + err and obstacleMapLookup(map,newpos) >= -1

def mapCreate(bBox,dim):
    map=[]
    n = int(bBox[0]//dim)
    m = int(bBox[1]//dim)
    for i in range(n):
        l=[]
        for j in range(m):
            l.append(-1)
        map.append(l)
    return map,(int(n//2),int(m//2)),(n,m)


def getMapDim(map):
   return len(map), len(map[0])


def mapUpdate(map,cella,val):
    map[cella[0]][cella[1]] = val



def obstacleMapLookup(map,pos):
    return map[pos[0]][pos[1]]


say("start")


obstacleSistematicMapping((5,0.5),0.5,-0.1)

