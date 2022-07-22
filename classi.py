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

    def __str__(self):
        a=""
        for x in self.mappa:
            a = a + str(x) + "\n"
        
        return a[:-1]
    
    def middlePos(self):
        return Position(self.n//2, self.m//2)


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

        



class Gender(enum.Enum):
    male  = ("he","his" , "him")
    female = ("she", "her", "her")

class Guest:
    def __init__(self,name,gender,drink):
        self.name = name
        self.gender = gender
        self.drink = drink


class Chair:
    def __init__(self,pos):
        self.pos = pos
        self.person = None

    def sit(self,person):
        self.person = person

    def unsit(self):
        self.person = None

    def isEmpty(self):
        return self.person is None

    def __eq__(self, __o):
        return self.pos == __o.pos


class Position:
    def __init__(self,x,y,th=361):
        self.x =x
        self.y = y
        self.th = th
        self.nextPosition = None

    def __hash__(self):
        return self.x+self.y + self.x*self.y
        
    def __eq__(self, __o):
        return self.x == __o.x and self.y == __o.y #and self.th == __o.th
    

    def __str__(self) :
        s = self.x + ", " + self.y 
        if self.th != 361:
            s = s + ", " + self.th
        return s

    def copy(self):
        return Position(self.x,self.y,self.th)

    def tryUpdate(self,dir,fix=True):
        if fix:
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
    right = Position(0,-1,-90)
    left = Position(0,1,90)
    forward = Position(1,0,0)
    backward = Position(-1,0,180)

class GlobalData:
    def __init__(self,tries,diedCell):
        self.itself = None
        self.tries = tries
        self.diedCell = diedCell

    def createGlobalData(self):
        self.itself = GlobalData(6,3)

        
        