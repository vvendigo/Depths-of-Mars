import pygame
import core
import objects
import data
import random

tileSize = 40


class Empty:
    impassable = False
    def draw(self, x, y):
        pass
    #enddef
#endclass

class Wall:
    img = None
    impassable = True

    def __init__(self):
        self.img = data.tiles[4]
        self.rect = self.img.get_rect()
    #enddef

    def draw(self, x, y):
        self.rect.topleft = (x,y)
        core.screen.blit(self.img, self.rect)
    #enddef


#endclass

class Level:

    players = []
    playerMissiles = []
    aliens = []

    width = 0
    height = 0
    walls = []
    x = 0
    y = 0

    def __init__(self, no = 0):
        self.load(no)
#        for i in xrange(0,10):
#            self.aliens.append(objects.Ball((i*20)%core.width, 10*((i*20)/core.width), self))
    #enddef

    def load(self, no):
        players = []
        playerMissiles = []
        aliens = []
        self.walls = []
        x = 0
        y = 0
        
        f = open("lvl/%03d.lvl"%(no))
        maxX = 0
        for y,ln in enumerate(f):
            ln = ln.rstrip()
            if len(ln)>maxX:
                maxX = len(ln)
            wall = []
            for x,ch in enumerate(ln):
                if ch == 'p':
                    self.players.append(objects.Player(x*tileSize, y*tileSize, core.controls, self))
                if ch == '#':
                    wall.append(Wall())
                else:
                    wall.append(Empty())
            #endfor
            self.walls.append(wall)
            self.height += tileSize
        #endfor
        self.width = maxX * tileSize
        if not self.players:
            self.players.append(objects.DummyPlayer(0, 0, self))
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

        for ty, wall in enumerate(self.walls[y/tileSize:y/tileSize+core.height/tileSize+1]):
            for tx, w in enumerate(wall):
                w.draw(tx*tileSize-x, ty*tileSize-y%tileSize)
        for obj in self.players:
            obj.draw(-x, -y)
        for obj in self.playerMissiles:
            obj.draw(-x, -y)
        for obj in self.aliens:
            obj.draw(-x, -y)
    #enddef

    def collision (self, x, y):
        if x<0 or x>=self.width:
            return False
        if y<0 or y>=self.height:
            return False
        x = int(x/tileSize)
        y = int(y/tileSize)
        if x>len(self.walls[y]):
            return False
        return self.walls[y][x].impassable
    #enddef
#endclass
