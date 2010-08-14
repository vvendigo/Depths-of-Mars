import pygame
import core
from misc import *
import data
import math
from random import randint
import anim

class BaseObj:
    sprite = None
    speed = [0,0]
    level = None

    def __init__(self, x=0, y=0, pos='tl'):
        self.rect = self.sprite.getSurface().get_rect()
        self.y = y
        if pos =='c':
            self.rect.centerx = x
            self.rect.centery = y
        else:
            self.rect.left = x
            self.rect.top = y
    #enddef

    def draw(self, corrx, corry):
        self.sprite.draw(core.screen, self.rect.left+corrx, self.rect.top+corry)
    #enddef

    def behave(self):
        self.rect = self.rect.move(self.speed)
        return True
    #enddef

    def hurt(self, armSpec):
        hurtEnergy = self.energy
        self.energy -= armSpec
        return hurtEnergy
    #enddef

#endclass

class Floater(BaseObj):
    def __init__(self, x, y):
        self.sprite = anim.Slot(data.images['alien'])
        mvlim = 2
        while self.speed[0]==0 and self.speed[1]==0:
            self.speed = [random.randint(-mvlim,mvlim), random.randint(-mvlim,mvlim)]
            if self.speed[0] or self.speed[1]:
                break
        #endwhile
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

        # level collision
        if self.speed[1]<0 and \
            ( self.level.collision(self.rect.left, self.rect.top+self.speed[1])\
            or self.level.collision(self.rect.right, self.rect.top+self.speed[1])):
            self.speed[1] *= -1
        if self.speed[1]>0 and \
            ( self.level.collision(self.rect.left, self.rect.bottom+self.speed[1])\
            or self.level.collision(self.rect.right, self.rect.bottom+self.speed[1])):
            self.speed[1] *= -1
        if self.speed[0]<0 and \
            ( self.level.collision(self.rect.left+self.speed[0], self.rect.top)\
            or self.level.collision(self.rect.left+self.speed[0], self.rect.bottom)):
            self.speed[0] *= -1
        if self.speed[0]>0 and \
            ( self.level.collision(self.rect.right+self.speed[0], self.rect.top)\
            or self.level.collision(self.rect.right+self.speed[0], self.rect.bottom)):
            self.speed[0] *= -1

        if self.rect.right < 0 or self.rect.left > self.level.width:
            self.energy = 0
        if self.rect.bottom < 0 or self.rect.top > self.level.height:
            self.energy = 0
        return BaseObj.behave(self)
    #enddef
#endclass


class AlienBase(BaseObj):
    def behave(self):
        for m in self.level.playerMissiles:
            if self.rect.colliderect(m.rect):
                self.energy -= m.hurt(self.energy)
        #endfor
        if self.energy <= 0:
            return False
        return BaseObj.behave(self)
    #enddef
#endclass

class Brooder(AlienBase):
    def __init__(self, x, y):
        self.sprite = anim.Slot(data.images['brooder'])
        self.energy = 50
        self.speed = [0,0]
        self.toDelivery = 0
        AlienBase.__init__(self, x, y)
    #enddef

    def behave(self):
        if randint(0, 32000) < self.toDelivery:
            self.level.aliens.append(Crawler(self.rect.left, self.rect.top))
            self.toDelivery = 0
        else:
            self.toDelivery += 1
        #endif
        return AlienBase.behave(self)
    #enddef
#endclass

class Crawler(BaseObj):
    def __init__(self, x, y):
        self.sprite = anim.Slot(data.images['alien'])
        self.energy = 5
        self.speed = [0, -1]
        BaseObj.__init__(self, x, y)
    #enddef

    def behave(self):
        for m in self.level.playerMissiles:
            if self.rect.colliderect(m.rect):
                self.energy -= m.hurt(self.energy)
        #endfor
        if self.energy <= 0:
            return False

        # level collision
        if self.speed[1]<0 and \
            ( self.level.collision(self.rect.left, self.rect.top+self.speed[1])\
            or self.level.collision(self.rect.right, self.rect.top+self.speed[1])):
            self.speed[1] = 0
            self.speed[0] = 1
        if self.speed[1]>0 and \
            ( self.level.collision(self.rect.left, self.rect.bottom+self.speed[1])\
            or self.level.collision(self.rect.right, self.rect.bottom+self.speed[1])):
            self.speed[1] = 0
            self.speed[0] = -1
        if self.speed[0]<0 and \
            ( self.level.collision(self.rect.left+self.speed[0], self.rect.top)\
            or self.level.collision(self.rect.left+self.speed[0], self.rect.bottom)):
            self.speed[0] = 0
            self.speed[1] = -1
        if self.speed[0]>0 and \
            ( self.level.collision(self.rect.right+self.speed[0], self.rect.top)\
            or self.level.collision(self.rect.right+self.speed[0], self.rect.bottom)):
            self.speed[0] = 0
            self.speed[1] = 1

        if self.rect.right < 0 or self.rect.left > self.level.width:
            self.energy = 0
        if self.rect.bottom < 0 or self.rect.top > self.level.height:
            self.energy = 0
        return BaseObj.behave(self)
    #enddef
#endclass



class Player(BaseObj):
    def __init__(self, x, y, controls):
        self.controls = controls
        self.sprite = anim.Slot(data.images['module'])
        self.reloadTime = pygame.time.get_ticks()
        self.shootSnd = pygame.mixer.Sound("snd/31855__HardPCM__Chip015.wav")
        self.speed = [0,0]
        self.vizor = [0,0]
        self.energy = 100
        self.fuel = 100
        self.ammo = 100
        BaseObj.__init__(self, x, y)
    #enddef

    def fire(self):
        self.reloadTime = pygame.time.get_ticks() + 700
        self.level.playerMissiles.append(\
            PlayerMissile(self.rect.centerx, self.rect.bottom))
        playStereo(self.shootSnd, self.rect.centerx)
    #enddef

    def behave(self):
        # monster collisions
        for m in self.level.aliens:
            if self.rect.colliderect(m.rect):
                self.energy -= m.hurt(self.energy)
                dx = m.rect.centerx - self.rect.centerx
                dy = m.rect.centery - self.rect.centery
                d = math.hypot(dx, dy)
                if d:
                    self.speed[0] -= (dx/d)*3.0
                    self.speed[1] -= (dy/d)*3.0
            #endif
        #endfor
        # level collision
        if self.speed[1]<0 and \
            ( self.level.collision(self.rect.left, self.rect.top+self.speed[1])\
            or self.level.collision(self.rect.right, self.rect.top+self.speed[1])):
            self.energy += self.speed[1]
            self.speed[1] *= -1
        if self.speed[1]>0 and \
            ( self.level.collision(self.rect.left, self.rect.bottom+self.speed[1])\
            or self.level.collision(self.rect.right, self.rect.bottom+self.speed[1])):
            self.energy -= self.speed[1]
            self.speed[1] *= -1
        if self.speed[0]<0 and \
            ( self.level.collision(self.rect.left+self.speed[0], self.rect.top)\
            or self.level.collision(self.rect.left+self.speed[0], self.rect.bottom)):
            self.energy += self.speed[0]
            self.speed[0] *= -1
        if self.speed[0]>0 and \
            ( self.level.collision(self.rect.right+self.speed[0], self.rect.top)\
            or self.level.collision(self.rect.right+self.speed[0], self.rect.bottom)):
            self.energy -= self.speed[0]
            self.speed[0] *= -1

        if self.energy <= 0:
            return False
        if self.controls.fire and pygame.time.get_ticks() > self.reloadTime:
            self.fire()
        #endif
        if self.controls.left:
            self.speed[0] -= 1
            self.vizor[0] -= 2
        if self.controls.right:
            self.speed[0] += 1
            self.vizor[0] += 2
        if self.controls.up:
            self.speed[1] -= 1
            self.vizor[1] -= 2
        if self.controls.down:
            self.speed[1] += 1
            self.vizor[1] += 2
        self.speed[0] *= 0.9
        self.speed[1] *= 0.9
        self.vizor[0] *= 0.98
        self.vizor[1] *= 0.98
        return BaseObj.behave(self)
    #enddef

    def getPos(self):
        return self.rect.centerx+self.vizor[0], self.rect.centery+self.vizor[1]
    #enddef

    def draw(self, corrx, corry):
        BaseObj.draw(self, corrx, corry)
        # draw status bars
        x = y = 15
        core.screen.fill((0,0,0), (x+0*7, y, 6, 52))
        core.screen.fill((0,0,0), (x+1*7, y, 6, 52))
        core.screen.fill((0,0,0), (x+2*7, y, 6, 52))

        core.screen.fill((200,0,0), (x+1+0*7, y+1, 4, self.ammo/2))
        core.screen.fill((0,0,200), (x+1+1*7, y+1, 4, self.fuel/2))
        core.screen.fill((0,200,0), (x+1+2*7, y+1, 4, self.energy/2))
        
    #enddef
#endclass

class PlayerMissile(BaseObj):
    def __init__(self, x, y):
        self.sprite = anim.Slot(data.images['missile'])
        self.speed = [0, 10]
        self.energy = 10
        BaseObj.__init__(self, x, y, 'c')
    #enddef

    def behave(self):
        if self.level.collision(\
            self.rect.centerx+self.speed[0], self.rect.centery+self.speed[1]):
            self.energy = 0
        self.speed[1] *= 0.98
        if self.speed[1] < 5 or self.energy <= 0:
            return False
        return BaseObj.behave(self)
    #enddef

#endclass

class DummyPlayer (BaseObj):
    def __init__(self, x, y):
        self.dx = 1
        self.dy = 0.25
        self.x = x
        self.y = y
    #enddef

    def draw(self, corrx, corry):
        pass
    #enddef

    def behave(self):
        if self.dx > 0 and self.x > self.level.width-core.width/2:
            self.dx = -1
        if self.dx < 0 and self.x < core.width/2:
            self.dx = +1
        if self.dy > 0 and self.y > self.level.height-core.height/2:
            self.dy *= -1
        if self.dy < 0 and self.y < core.height/2:
            self.dy *= -1
        m = self.level.width/2
        n = (self.level.width-core.width)/2

        self.x += self.dx+self.dx*(n - abs(self.x - m))/float(n/2)
        self.y += self.dy
        return True
    #enddef

    def getPos(self):
        return self.x, self.y
    #enddef

#endclass

