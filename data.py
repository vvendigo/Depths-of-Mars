import pygame

playerShip = None
tiles = None
alien = None
missile = None


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
    global playerShip, tiles, alien, missile
    playerShip = load('img/module.png')
    alien = load('img/alien.png')
    missile = load('img/missile.png')
    tiles = loadTiles('img/tiles.png', 40)
#enddef
