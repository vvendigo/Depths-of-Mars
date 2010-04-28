import pygame
import core
from random import randint

playerShip = None
tiles = None
emptyTiles = None
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

def makeTile(setup = (1,1,1, 1,1,1, 1,1,1)):
    """ Make tile filled with random noise
    """
    smpSize = core.tileSize/4 # sample radius
    smpArea = float((2*smpSize)*(2*smpSize)*0.75)

    s = pygame.Surface((core.tileSize, core.tileSize))
    for x in xrange(0, core.tileSize):
        for y in xrange(0, core.tileSize):
            if setup[4]:
                opacity = 1.0
            else:
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
                          setup[(sy1/core.tileSize+1)*3+sx1/core.tileSize+1]*(px*py)\
                        + setup[(sy1/core.tileSize+1)*3+sx2/core.tileSize+1]*((2*smpSize-px)*py)\
                        + setup[(sy2/core.tileSize+1)*3+sx2/core.tileSize+1]*((2*smpSize-px)*(2*smpSize-py))\
                        + setup[(sy2/core.tileSize+1)*3+sx1/core.tileSize+1]*(px*(2*smpSize-py)) ) / smpArea
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
    global playerShip, tiles, emptyTiles, alien, missile, mnuFont1, mnuFont2
    playerShip = load('img/module.png')
    alien = load('img/alien.png')
    missile = load('img/missile.png')
    tiles = []
    
    for i in xrange(0, 5):
        tiles.append(makeTile())

    emptyTiles = {}
    patt = [0,0,0, 0,0,0, 0,0,0]
    t = pygame.time.get_ticks()
    for i in xrange(1, 2**9):
        i = 0
        while patt[i]:
            patt[i] = 0
            i += 1
        patt[i] = 1
        if patt[4]:
            continue
        emptyTiles[tuple(patt)] = makeTile(patt)
    #endfor
    print (pygame.time.get_ticks() - t)/1000.0
#    import sys
#    sys.exit()
    #loadTiles('img/tiles.png', core.tileSize)
    mnuFont1 = pygame.font.Font(pygame.font.get_default_font(), 30)
    mnuFont2 = pygame.font.Font(pygame.font.get_default_font(), 50)
    mnuFont2.set_bold(True)
#enddef
