# misc functions
import pygame
import random
import core

def playStereo(sound, x):
    """ Play sound with volume setting dependent on x-axis position
    """
    ch = pygame.mixer.find_channel(True)
    ch.play(sound)
    pos = x / float(core.width*2)
    if pos < 0:   pos = 0
    if pos > 0.5: pos = 0.5
    ch.set_volume(1.0-pos, pos + 0.5)
#enddef

def makeImg(pointSet):
    """ Make syntetic image from set of points
    """
    minX, minY, maxX, maxY = (None, None, None, None)

    for x, y in pointSet:
        if minX==None or minX>x:
            minX = x
        if maxX==None or maxX<x:
            maxX = x
        if minY==None or minY>y:
            minY = y
        if maxY==None or maxY<y:
            maxY = y
    #endfor

    w = maxX - minX
    h = maxY - minY
    s = pygame.Surface((w+1, h+1))
    s.fill((0,0,0))
    s.set_colorkey((0,0,0))

    ordSet = []
    for x, y in pointSet:
        bestSet = sorted(pointSet, key=lambda(x2,y2): (x2-x)*(x2-x)+(y2-y)*(y2-y))
        ordSet.append(bestSet[1:3])
    #endfor

    i = 0
    for x, y in pointSet:
        for x2, y2 in ordSet[i]:
            pygame.draw.line(s,
                (random.randint(10,255),random.randint(10,255),random.randint(10,255)),
                (x-minX, y-minY), (x2-minX, y2-minY))
        i += 1
    #endfor

    return s.convert()
#enddef


