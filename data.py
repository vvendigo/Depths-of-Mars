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

def makeTile(setup = [[1,1,1],[1,0,1],[1,1,1]]):
    """ Make tile filled with random noise
    """
    smpSize = core.tileSize/4 # sample radius
    smpArea = float((2*smpSize)*(2*smpSize))

    s = pygame.Surface((core.tileSize, core.tileSize))
    for x in xrange(0, core.tileSize):
        for y in xrange(0, core.tileSize):
            px = smpSize
            py = smpSize
            sx1 = x - smpSize
            sy1 = y - smpSize
            sx2 = x + smpSize
            sy2 = y + smpSize
            if sx1 < 0: px = -sx1
            if sy1 < 0: py = -sy1
            if sx2 >= core.tileSize: px = 2*smpSize - (sx2-core.tileSize)
            if sy2 >= core.tileSize: py = 2*smpSize - (sy2-core.tileSize)
            opacity = 0.0
            if px>=0 and py>=0:
                opacity = (\
                      setup[sy1/core.tileSize+1][sx1/core.tileSize+1]*(px*py)\
                    + setup[sy1/core.tileSize+1][sx2/core.tileSize+1]*((2*smpSize-px)*py)\
                    + setup[sy2/core.tileSize+1][sx2/core.tileSize+1]*((2*smpSize-px)*(2*smpSize-py))\
                    + setup[sy2/core.tileSize+1][sx1/core.tileSize+1]*(px*(2*smpSize-py)) ) / smpArea
            #print opacity
            r = randint(20,150)
            s.set_at((x,y),\
                (int((r+90)*opacity),\
                int((r+randint(-r/10,r/10))*opacity),\
                int((r+randint(-r/20,+r/20))*opacity)))
    #endfor

    return s.convert()
#enddef



def init():
    global playerShip, tiles, alien, missile, mnuFont1, mnuFont2
    playerShip = load('img/module.png')
    alien = load('img/alien.png')
    missile = load('img/missile.png')
    tiles = []
    for i in xrange(0,1):
        tiles.append(makeTile())
#    import sys
#    sys.exit()
    #loadTiles('img/tiles.png', core.tileSize)
    mnuFont1 = pygame.font.Font(pygame.font.get_default_font(), 30)
    mnuFont2 = pygame.font.Font(pygame.font.get_default_font(), 50)
    mnuFont2.set_bold(True)
#enddef
