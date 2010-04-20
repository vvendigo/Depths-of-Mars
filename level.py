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

    def load(self):
        self.players = []
        self.playerMissiles = []
        self.aliens = []
        self.walls = []
        self.width = 0
        self.height = 0
        x = 0
        y = 0
        
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
                    self.players.append(objects.Player(x*core.tileSize, y*core.tileSize, core.controls, self))
                if ch == 'b':
                    self.aliens.append(objects.Ball(x*core.tileSize, y*core.tileSize, self))
                if ch == 'c':
                    self.aliens.append(objects.Crawler(x*core.tileSize, y*core.tileSize, self))
                # walls
                if ch == '#':
                    wall.append(Wall())
                else:
                    wall.append(Empty())
            #endfor
            self.walls.append(wall)
            self.height += core.tileSize
        #endfor
        self.width = maxX * core.tileSize
        if not self.players:
            self.players.append(objects.DummyPlayer(core.width/2, core.height/2, self))
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
