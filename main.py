#! /usr/bin/python
import sys, pygame
import core
import data
from level import Level

pygame.mixer.pre_init(22050, -16, 2, 2048)
pygame.init()

core.width = 640
core.height = 480
core.appName = "Pygame experiment"
core.init()

data.init()

framerate = 40
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT+1, 1000/framerate)

#snd = pygame.mixer.Sound("snd/31855__HardPCM__Chip015.wav")

level = Level()

while not core.controls.quit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: core.controls.quit = True
        if event.type == pygame.KEYDOWN: core.controls.onKeyDn(event.key)
        if event.type == pygame.KEYUP: core.controls.onKeyUp(event.key)
        if event.type == pygame.USEREVENT+1: level.behave()
    #endfor

    core.screen.fill((0,0,0))
    level.draw()
    core.screen.blit(core.font.render("%.3f"%(clock.get_fps()), False, (0,255,0)), (0,0))
    pygame.display.flip()

    clock.tick(framerate)
#endwhile
