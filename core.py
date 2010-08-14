import pygame

font = None
width = 640
height = 480
appNme = "appName"

tileSize = 40

screen = None

def init():
    global font, screen
    font = pygame.font.Font(pygame.font.get_default_font(), 10)

    screen = pygame.display.set_mode((width,height), \
                pygame.HWSURFACE|pygame.DOUBLEBUF)#, pygame.RESIZABLE)
    pygame.display.set_caption(appName)
#endif

class Controls:
    def __init__(self):
        self.exit = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False
        self.enter = False
    #enddef

    def onKeyDn(self, key):
        if key==pygame.K_RETURN: self.enter = True
        if key==pygame.K_ESCAPE: self.exit = True
        if key==pygame.K_UP:     self.up = True
        if key==pygame.K_DOWN:   self.down = True
        if key==pygame.K_LEFT:   self.left = True
        if key==pygame.K_RIGHT:  self.right = True
        if key==pygame.K_RCTRL:  self.fire = True
    #endif

    def onKeyUp(self, key):
        if key==pygame.K_RETURN: self.enter = False
        if key==pygame.K_ESCAPE: self.exit = False
        if key==pygame.K_UP:     self.up = False
        if key==pygame.K_DOWN:   self.down = False
        if key==pygame.K_LEFT:   self.left = False
        if key==pygame.K_RIGHT:  self.right = False
        if key==pygame.K_RCTRL:  self.fire = False
    #enddef
#endclass

controls = Controls()

