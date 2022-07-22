# Write your robot program hereenable

import math
from random import randint

from marrtino_apps.program.robot_cmd_ros import enableObstacleAvoidance



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
import enum



class Map:
    def __init__(self,bBox,dim):
        self.dim= dim
        n = int(bBox[0]//dim)
        m = int(bBox[1]//dim)
        self.n = n
        self.m = m
        self.mappa = []
        self.numCelle = n * m
        for i in range(n):
            l=[]
            for j in range(m):
                l.append(0)
            self.mappa.append(l)

    def __str__(self) -> str:
        a=""
        for x in self.mappa:
            a = a + str(x) + "\n"
        
        return a[:-1]


    def lookup(self,cell):
        return self.mappa[cell.x][cell.y]

    def updateCell(self,cell,val):
        self.mappa[cell.x][cell.y] = val

    def addVal(self,cell,val):
        self.mappa[cell.x][cell.y] += val

    def predictLookup(self,cell,dir):
        return self.mappa[cell.x+ dir.x][cell.y + dir.y]

    def validCell(self,pos):
        return pos.x >= 0 and pos.x < self.n and pos.y >= 0 and pos.y < self.m




class Position:
    def __init__(self,x,y,th=361):
        self.x =x
        self.y = y
        self.th = th
        self.nextPosition = None
    
    def __hash__(self) -> int:
        return self.x+self.y + self.x*self.y
        
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y #and self.th == __o.th
    
    def copy(self):
        return Position(self.x,self.y,self.th)

    def tryUpdate(self,dir):
        dir = self.turn(dir)
        th = dir.value.th
        x = self.x + dir.value.x
        y = self.y + dir.value.y
        self.nextPosition = Position(x,y,th)
        return self.nextPosition
    
    def update(self):
        self.x = self.nextPosition.x
        self.y = self.nextPosition.y
        self.th = self.nextPosition.th
        self.nextPosition = None
    
    def turn(self,dir):
        #sali
        if ( self.th == 0 and dir == Directions.forward ) or (self.th == -90 and dir == Directions.left) \
             or (self.th == 90 and dir == Directions.right) or (self.th == 180 and dir == Directions.backward) :
             return Directions.forward
        #destra
        elif ( self.th == 0 and dir == Directions.right ) or (self.th == -90 and dir == Directions.forward) \
             or (self.th == 90 and dir == Directions.backward) or (self.th == 180 and dir == Directions.left) :
             return Directions.right
        #sinistra
        elif ( self.th == 0 and dir == Directions.left ) or (self.th == -90 and dir == Directions.backward) \
             or (self.th == 90 and dir == Directions.forward) or (self.th == 180 and dir == Directions.right) :
             return Directions.left
        #scendi
        elif ( self.th == 0 and dir == Directions.backward ) or (self.th == -90 and dir == Directions.right) \
             or (self.th == 90 and dir == Directions.left) or (self.th == 180 and dir == Directions.forward) :
             return Directions.backward
             

class Directions(enum.Enum):
    right = Position(0,-1,90)
    left = Position(0,1,-90)
    forward = Position(1,0,0)
    backward = Position(-1,0,180)


def obstacleSistematicMapping(bBox,dim,err):
    map=Map(bBox,dim)
    #mapDim = getMapDim(map)
    #numCelle = mapDim[0] * mapDim[1]

    pos = Position(0,0,0)
    map.updateCell(pos,-1)
    backward = False
    mapping = True
    count = 0
    while mapping:
        if count == map.numCelle:
            mapping=False
        elif tryRight(err,map,pos.tryUpdate(Directions.right)):
            say("right")
            count += 1
            pos.update()
            map.updateCell(pos,-1)
            forward(dim)
            if map.lookup(pos) >= 0 :
                backward = False




        elif tryForward(err,map,pos.tryUpdate(Directions.forward),backward):
            say("forward")
            pos.update()
            if map.lookup(pos) == -1:
                map.updateCell(pos,-2)
            else:
                count += 1
                if map.lookup(pos) >= 0 :
                    backward = False
                map.updateCell(pos,-1)
            forward(dim)


        elif tryLeft(err,map,pos.tryUpdate(Directions.left)):
            say("left")
            count += 1
            pos.update()
            map.updateCell(pos,-1)
            forward(dim)
            if map.lookup(pos) >= 0 :
                backward = False



        elif tryBackward(err,map,pos.tryUpdate(Directions.backward)):
            say("backward")
            backward = True
            map.updateCell(pos,-2)
            pos.update()
            map.updateCell(pos,-2)
            forward(dim)
        else:
            mapping = False
        display(str(map))
    return map,pos







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
    display(str(map))
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

def validCell(cell,visitati):
    return (cell not in visitati) and map.validCell(cell) and map.lookup(cell) != -3


say("start")

enableObstacleAvoidance(False)

mappa, posizione = obstacleSistematicMapping((1.5,1),0.5,0.1)

say("finish mapping")

target = Position(0,1)

obstacleMoveTo(mappa,posizione,target)