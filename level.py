import pygame
import core
import objects
import data
import random



class Empty:
    impassable = False
    def draw(self, x, y):
        pass
    #enddef
#endclass

class Edge:
    impassable = False
    def __init__(self, pattern):
        self.img = data.tiles[tuple(pattern)]
        self.rect = self.img.get_rect()
    #enddef

    def draw(self, x, y):
        self.rect.topleft = (x,y)
        core.screen.blit(self.img, self.rect)
    #enddef
#endclass

class Wall:
    impassable = True

    def __init__(self, pattern):
        self.img = data.tiles[tuple(pattern)]
        self.rect = self.img.get_rect()
    #enddef

    def draw(self, x, y):
        self.rect.topleft = (x,y)
        core.screen.blit(self.img, self.rect)
    #enddef
#endclass

class Level:

    number = 0
    players = []
    playerMissiles = []
    aliens = []

    width = 0
    height = 0
    walls = []
    x = 0
    y = 0

    def __init__(self, no):
        self.number = no
    #enddef

    def reset(self):
        # set static refference of objs
        objects.BaseObj.level = self

        self.players = []
        self.playerMissiles = []
        self.aliens = []
        self.walls = []
        self.width = 0
        self.height = 0
    #enddef

    def load(self):
        self.reset()
        x = 0
        y = 0
        lvlData = []

        f = open("lvl/%03d.lvl"%(self.number))
        maxX = 0
        for y,ln in enumerate(f):
            ln = ln.rstrip()
            if len(ln)>maxX:
                maxX = len(ln)
            wall = []
            for x,ch in enumerate(ln):
                # actors
                if ch == 'p':
                    self.players.append(objects.Player(x*core.tileSize, y*core.tileSize, core.controls))
                if ch == 'f':
                    self.aliens.append(objects.Floater(x*core.tileSize, y*core.tileSize))
                if ch == 'c':
                    self.aliens.append(objects.Crawler(x*core.tileSize, y*core.tileSize))
                if ch == 'b':
                    self.aliens.append(objects.Brooder(x*core.tileSize, y*core.tileSize))
                # walls
                if ch == '#':
                    wall.append(1)
                else:
                    wall.append(0)
            #endfor
            lvlData.append(wall)
            self.height += core.tileSize
        #endfor
        self.width = maxX * core.tileSize
        if not self.players:
            self.players.append(objects.DummyPlayer(core.width/2, core.height/2))

        self.setTiles(lvlData)
    #enddef

    def randDir(self, width, x):
        dx = 0
        while not dx:
            dx = random.randint(1,width-2) - x
        return dx
    #enddef

    def generate(self):
        self.reset()
        lvlData = []
        width = 10 + self.number * 10
        depth = 20 + self.number * 50
        for i in xrange(0,depth):
            ln = []
            for j in xrange(0,width):
                ln.append(1)
            lvlData.append(ln)
        #endfor

        x = width / 2
        y = 0
        dx = 0
        dy = 5
        random.seed(self.number)
        while y < depth-1:
            for i in range(0,random.randint(2,4)):
                for j in range(random.randint(-1,0),random.randint(2,4)):
                    if x+j < width-1 and x+j>0 and y+i < depth:
                        lvlData[y+i][x+j] = 0
            if dy:
                dy -= 1
                y += 1
                if not dy:
                    dx = self.randDir(width-1, x)
            elif dx:
                if dx > 0:
                    dx -= 1
                    x += 1
                else:
                    dx += 1
                    x -= 1
                if not dx:
                    dy = random.randint(2,10)
        #endwhile

        self.height = depth * core.tileSize
        self.width = width * core.tileSize
        self.players.append(objects.Player(self.width/2, 10, core.controls))
        self.setTiles(lvlData)
    #enddef

    def setTiles(self, lvlData):
        for y in xrange(0, len(lvlData)):
            row = []
            for x in xrange(0, len(lvlData[y])):
                patt = []
                for j in xrange(y-1,y+2):
                    for i in xrange(x-1,x+2):
                        if j<0 or i<0 \
                            or j>=len(lvlData) or i>=len(lvlData[j]):
                            patt.append(0)
                        else:
                            patt.append(lvlData[j][i])
                if patt == [0,0,0, 0,0,0, 0,0,0]:
                    row.append(Empty())
                elif lvlData[y][x]:
                    row.append(Wall(patt))
                else:
                    row.append(Edge(patt))
            #endfor
            self.walls.append(row)
        #endfor
    #enddef


    def behave(self):
        newList = []
        for obj in self.players:
            if obj.behave():
                newList.append(obj)
            else:
                del obj
        self.players = newList
        newList = []
        for obj in self.playerMissiles:
            if obj.behave():
                newList.append(obj)
            else:
                del obj
        self.playerMissiles = newList
        newList = []
        for obj in self.aliens:
            if obj.behave():
                newList.append(obj)
            else:
                del obj
        self.aliens = newList
    #enddef

    def draw(self):
        x = 0
        y = 0
        if self.players:
            plx, ply = self.players[0].getPos()
            y = ply - core.height/2
            x = plx - core.width/2
            if x < 0:
                x = 0
            if x > self.width - core.width:
                x = self.width - core.width
            if y < 0:
                y = 0
            if y > self.height - core.height:
                y = self.height - core.height
        else:
            x = (self.width - core.width) / 2
        #endif

        x = int(x)
        y = int(y)

        for ty, wall in enumerate(self.walls[y/core.tileSize:y/core.tileSize+core.height/core.tileSize+1]):
            for tx, w in enumerate(wall):
                w.draw(tx*core.tileSize-x, ty*core.tileSize-y%core.tileSize)
        for obj in self.playerMissiles:
            obj.draw(-x, -y)
        for obj in self.aliens:
            obj.draw(-x, -y)
        for obj in self.players:
            obj.draw(-x, -y)
    #enddef

    def collision (self, x, y):
        if x<0 or x>=self.width:
            return False
        if y<0 or y>=self.height:
            return False
        x = int(x/core.tileSize)
        y = int(y/core.tileSize)
        if x>len(self.walls[y]):
            return False
        return self.walls[y][x].impassable
    #enddef
#endclass
