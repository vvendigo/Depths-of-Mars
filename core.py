import pygame

font = None
width = 640
height = 480
appNme = "appName"
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
        self.quit = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False
    #enddef

    def onKeyDn(self, key):
        if key==27:  self.quit = True
        if key==273: self.up = True
        if key==274: self.down = True
        if key==276: self.left = True
        if key==275: self.right = True
        if key==305: self.fire = True
    #endif

    def onKeyUp(self, key):
        if key==273: self.up = False
        if key==274: self.down = False
        if key==276: self.left = False
        if key==275: self.right = False
        if key==305: self.fire = False
    #enddef
#endclass

controls = Controls()

