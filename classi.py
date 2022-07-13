import enum



class Map:
    def __init__(self,bBox,dim):
        self.dim= dim
        n = int(bBox[0]//dim)
        m = int(bBox[1]//dim)
        self.size = (n,m)
        self.mappa = []
        for i in range(n):
            l=[]
            for j in range(m):
                l.append(-1)
            self.mappa.append(l)

    def lookup(self,cell):
        return self.mappa[cell[0]][cell[1]]

    def updateCell(self,cell,val):
        self.mappa[cell[0]][cell[1]] = val

    def addVal(self,cell,val):
        self.mappa[cell[0]][cell[1]] += val

    def predictLookup(self,cell,dir):
        return self.mappa[cell[0]+ dir[0]][cell[1] + dir[1]]

        



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

    

        