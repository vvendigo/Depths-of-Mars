import pygame
import core
import os
import asciiart

# dir setup
sndDir = 'snd'

# global for msg display 
screenY = screenX = 0

# data holders
images = None

mnuFont1 = None
mnuFont2 = None

sounds = None

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
    global images, mnuFont1, mnuFont2, sounds

    writeMsg("Initializing data:")

    writeMsg("Loading sprites...")
    images = asciiart.load('./graphics.txt', 4)

    t = pygame.time.get_ticks()

    writeMsg("Loading fonts...")
    mnuFont1 = pygame.font.Font(pygame.font.get_default_font(), 30)
    mnuFont2 = pygame.font.Font(pygame.font.get_default_font(), 50)
    mnuFont2.set_bold(True)

    writeMsg("Loading sounds...")
    sounds = {}
    sounds['shoot'] = pygame.mixer.Sound("snd/31855__HardPCM__Chip015.wav")
    sounds['engine'] = pygame.mixer.Sound("snd/engine.wav")

#enddef
