import pygame
import core
from misc import *
import data

class BaseObj:
    img = None
    speed = [0,0]

    def __init__(self, x=0, y=0):
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
    #enddef

    def draw(self, corrx, corry):
        core.screen.blit(self.img, self.rect.move((corrx, corry)))
    #enddef

    def behave(self):
        self.rect = self.rect.move(self.speed)
        return True
    #enddef
#endclass

class Ball(BaseObj):
    def __init__(self, x, y, level):
        self.img = data.alien
        self.level = level
        mvlim = 2
        self.speed = [random.randint(-mvlim,mvlim), random.randint(-mvlim,mvlim)]
        self.energy = 5
        BaseObj.__init__(self, x, y)
    #enddef

    def behave(self):
        for m in self.level.playerMissiles:
            if self.rect.colliderect(m.rect):
                self.energy -= m.hurt(self.energy)
        #endfor
        if self.energy <= 0:
            return False

        if self.rect.left < 0 or self.rect.right > core.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > core.height:
            self.speed[1] = -self.speed[1]
        return BaseObj.behave(self)
    #enddef
#endclass

class Player(BaseObj):
    def __init__(self, x, y, controls, level):
        self.controls = controls
        self.level = level
        self.img = data.playerShip
        self.reloadTime = pygame.time.get_ticks()
        self.shootSnd = pygame.mixer.Sound("snd/31855__HardPCM__Chip015.wav")
        BaseObj.__init__(self, x, y)
    #enddef

    def fire(self):
        self.reloadTime = pygame.time.get_ticks() + 400
        self.level.playerMissiles.append(PlayerMissile(self.rect.centerx, self.rect.top))
        playStereo(self.shootSnd, self.rect.centerx)
    #enddef

    def behave(self):
        if self.controls.fire and pygame.time.get_ticks() > self.reloadTime:
            self.fire()
        #endif
        if self.controls.left: self.speed[0] -= 1
        if self.controls.right: self.speed[0] += 1
        if self.controls.up: self.speed[1] -= 1
        if self.controls.down: self.speed[1] += 1
        self.speed[0] *= 0.9
        self.speed[1] *= 0.9
        return BaseObj.behave(self)
    #enddef

    def getPos(self):
        return self.rect.center
    #enddef
#endclass

class PlayerMissile(BaseObj):
    def __init__(self, x, y):
        self.img = data.missile
        self.speed = [0, -1]
        self.energy = 10
        BaseObj.__init__(self, x-3, y)
    #enddef

    def hurt(self, armSpec):
        self.energy = 0
        return 10
    #enddef

    def behave(self):
        if self.speed[1] > -5:
            self.speed[1] *= 1.3
        if self.rect.top < 0 or self.energy <= 0:
            return False
        return BaseObj.behave(self)
    #enddef

#endclass


