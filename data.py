import pygame
import core
from random import randint

playerShip = None
tiles = None
alien = None
missile = None

mnuFont1 = None
mnuFont2 = None

def load(fName):
    return pygame.image.load(fName).convert_alpha()
#enddef

def loadTiles(fName, tileSize):
    out = []
    src = pygame.image.load(fName).convert_alpha()
    for y in xrange(0, src.get_height(), tileSize):
        for x in xrange(0, src.get_width(), tileSize):
            img = pygame.Surface((tileSize, tileSize), 0, src)
            img.blit(src, (0,0), (x,y,tileSize,tileSize))
            out.append(img)
        #endfor
    #endfor
    return out
#enddef

def makeTile(setup = [[1,1,1],[1,1,1],[1,1,1]]):
    """ Make tile filled with random noise
    """

    s = pygame.Surface((core.tileSize, core.tileSize))
    for x in xrange(0, core.tileSize):
        for y in xrange(0, core.tileSize):
            r = randint(20,150)
            s.set_at((x,y), (r+90, r+randint(-r/10,r/10), r+randint(-r/20,+r/20)))
    #endfor

    return s.convert()
#enddef



def init():
    global playerShip, tiles, alien, missile, mnuFont1, mnuFont2
    playerShip = load('img/module.png')
    alien = load('img/alien.png')
    missile = load('img/missile.png')
    tiles = []
    for i in xrange(0,6):
        tiles.append(makeTile())
    #loadTiles('img/tiles.png', core.tileSize)
    mnuFont1 = pygame.font.Font(pygame.font.get_default_font(), 30)
    mnuFont2 = pygame.font.Font(pygame.font.get_default_font(), 50)
    mnuFont2.set_bold(True)
#enddef
