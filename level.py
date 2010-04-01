import pygame
import core
import objects
import data
import random

tileSize = 40


class Empty:
    def draw(self, x, y):
        pass
    #enddef
#endclass

class Wall:
    img = None

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

    w = 0
    walls = []

    def __init__(self):
        self.load(0)
        #self.players.append(objects.Player(core.controls, self))
        for i in xrange(0,10):
            self.aliens.append(objects.Ball((i*20)%core.width, 10*((i*20)/core.width), self))
    #enddef

    def load(self, no):
        players = []
        playerMissiles = []
        aliens = []
        self.walls = []
        
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
        #endfor
        self.w = maxX * tileSize
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
            if x > self.w - core.width:
                x = self.w - core.width
            if y < 0:
                y = 0
        else:
            x = (self.w - core.width) / 2
        #endif

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

#endclass
