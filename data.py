import pygame
import core

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

def init():
    global playerShip, tiles, alien, missile, mnuFont1, mnuFont2
    playerShip = load('img/module.png')
    alien = load('img/alien.png')
    missile = load('img/missile.png')
    tiles = loadTiles('img/tiles.png', core.tileSize)
    mnuFont1 = pygame.font.Font(pygame.font.get_default_font(), 30)
    mnuFont2 = pygame.font.Font(pygame.font.get_default_font(), 50)
    mnuFont2.set_bold(True)
#enddef
