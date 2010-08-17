import pygame
import anim


def makeImg(buff, colors, pxSz):
    maxLen = 0
    for ln in buff:
        if len(ln) > maxLen:
            maxLen = len(ln)
    s = pygame.Surface((pxSz*maxLen, pxSz*len(buff)), )
    s.fill((255,0,255))
    for y,ln in enumerate(buff):
        for x,px in enumerate(ln):
            if px == ' ':
                continue
            if colors.has_key(px):
                c = colors[px]
            else:
                c = (0,0,0)
            s.fill(c, (x*pxSz,y*pxSz, pxSz, pxSz))
        #endfor
    #endfor
    s.set_colorkey((255, 0, 255), pygame.RLEACCEL)
    return s.convert()
#enddef

def load(fName, pxSz=1):
    colors = {
        'W': (255,255,255), 'w': (128,128,128),
        'R': (255,0,0), 'r': (128,0,0),
        'G': (0,255,0), 'g': (0,128,0),
        'B': (0,0,255), 'b': (0,0,128) }
    out = {}
    oName = ''
    buff = []
    duration = 1
    f = open(fName, 'r')
    lnNo = 0
    for ln in f:
        lnNo += 1
        if ln.startswith('#'):
            continue
        ln = ln.rstrip()
        if ln=='':
            if buff and oName:
                out[oName].append(makeImg(buff, colors, pxSz), duration)
                buff = []
            continue
        if ln.startswith('@'):
            if ln.startswith('@duration'):
                duration = int(ln[9:].strip())
            elif ln.startswith('@name'):
                oName = ln[5:].strip()
                out[oName] = anim.Animation()
            elif ln.startswith('@end') and oName:
                out[oName].cycle = False
            elif ln.startswith('@color'):
                (ch, r, g, b) = ln[6:].strip().split(' ')
                colors[ch] = (int(r), int(g), int(b))
            else:
                raise "Wrong directive '%s' on line %d, name '%s'"\
                        %(ln, lnNo, oName)
            continue
        #endif
        buff.append(ln.strip("'"))
    #endfor
    if buff and oName:
        out[oName].append(makeImg(buff), duration)

    return out
#enddef


if __name__ == "__main__":
    import sys

    pygame.init()

    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    aag = load('./graphics.txt', 4)
    cavySprite = anim.Slot(aag['cavy'])
    cavySprite2 = anim.Slot(aag['cavy'])
    cavySprite2.rewind(20)
    invaderSprite = anim.Slot(aag['invader'])
    cx = 0
    cy = 300

    left = False
    right = False
    up = False
    down = False


    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key==27:  sys.exit(0) #self.exit = True
                if key==273: up = True
                if key==274: down = True
                if key==276: left = True
                if key==275: right = True
    #            if key==305: self.fire = True
            if event.type == pygame.KEYUP:
                key = event.key
                if key==273: up = False
                if key==274: down = False
                if key==276: left = False
                if key==275: right = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print pygame.mouse.get_pressed()
                (cx, cy) = pygame.mouse.get_pos()
        #endfor

        if up: cy -= 1
        if down: cy += 1
        if left: cx -= 1
        if right: cx += 1


        screen.fill((0,0,0))
        cavySprite.draw(screen, cx, cy)
        invaderSprite.draw(screen, 0, 350)
        cavySprite2.draw(screen, 100, 350)
        pygame.display.flip()

        clock.tick(30)

        cavySprite.behave()
        cavySprite2.behave()
        invaderSprite.behave()
    #endwhile

#endmain
