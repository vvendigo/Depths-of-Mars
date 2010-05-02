import pygame
import core
from random import randint
import os

# dir setup
generatedDataDir = 'generated'
imgDir = 'img'

# global for msg display 
screenY = screenX = 0

# data holders
playerShip = None
tiles = None
emptyTiles = None
alien = None
brooder = None
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
    smpSize = core.tileSize/6 # sample radius
    smpArea = float((2*smpSize)*(2*smpSize))

    s = pygame.Surface((core.tileSize, core.tileSize), pygame.HWSURFACE)
    s.fill((0,0,0))
    s.lock()
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
            opacity = (\
                  setup[(sy1/core.tileSize+1)*3+sx1/core.tileSize+1]*(px*py)\
                + setup[(sy1/core.tileSize+1)*3+sx2/core.tileSize+1]*((2*smpSize-px)*py)\
                + setup[(sy2/core.tileSize+1)*3+sx2/core.tileSize+1]*((2*smpSize-px)*(2*smpSize-py))\
                + setup[(sy2/core.tileSize+1)*3+sx1/core.tileSize+1]*(px*(2*smpSize-py)) ) / smpArea
            if opacity<=0:
                continue
            r = randint(20,150)
            s.set_at((x,y),\
                (int((r+90)*opacity),\
                int((r+randint(-r/10,r/10))*opacity),\
                int((r+randint(-r/20,+r/20))*opacity)))
    #endfor
    s.unlock()
    return s.convert()
#enddef

def writeMsg(msg):
    global screenY, screenX
    screenY += core.font.get_height()
    if screenY >= core.height - core.font.get_height():
        core.screen.fill((0,0,0))
        screenY = 0
    #endif
    msgI = core.font.render(msg, True, (230,20,9))
    core.screen.blit(msgI, (0, screenY))
    screenX = msgI.get_width()
    pygame.display.flip()
#enddef

def writeProgress(no, of):
    global screenY, screenX
    msgI = core.font.render("%d %%   "%(int((float(no)/of)*100)), True, (230,20,9), (0,0,0))
    core.screen.blit(msgI, (screenX, screenY))
    pygame.display.update((screenX, screenY, msgI.get_width(), msgI.get_height()))
#enddef

def init():
    global imgDir, generatedDataDir,\
        playerShip, tiles, emptyTiles, alien, brooder, missile, \
        mnuFont1, mnuFont2

    writeMsg("Initializing data:")

    writeMsg("Loading sprites...")
    playerShip = load(os.path.join(imgDir, 'module.png'))
    alien = load(os.path.join(imgDir, 'alien.png'))
    brooder = load(os.path.join(imgDir, 'brooder.png'))
    missile = load(os.path.join(imgDir, 'missile.png'))

    t = pygame.time.get_ticks()

    if not os.access(generatedDataDir, os.X_OK):
        os.mkdir(generatedDataDir)
        writeMsg("Generating tiles: ")
    else:
        writeMsg("Loading tiles: ")
    #endif

    tiles = {}
    patt = [0,0,0, 0,0,0, 0,0,0]
    for i in xrange(1, 2**9):
        j = 0
        while patt[j]:
            patt[j] = 0
            j += 1
        patt[j] = 1
        fPath = os.path.join(generatedDataDir, ''.join(map(str, patt)) + '.bmp')
        if os.access(fPath, os.R_OK):
            tiles[tuple(patt)] = load(fPath)
        else:
            tiles[tuple(patt)] = makeTile(patt)
            pygame.image.save(tiles[tuple(patt)], fPath)
        #endif
        writeProgress(i, 2**9)
    #endfor

    writeMsg("Tiles processed in %f secs."% ((pygame.time.get_ticks() - t)/1000.0))

    writeMsg("Loading fonts...")
    mnuFont1 = pygame.font.Font(pygame.font.get_default_font(), 30)
    mnuFont2 = pygame.font.Font(pygame.font.get_default_font(), 50)
    mnuFont2.set_bold(True)
#enddef
