import pygame
import core
from level import Level
from menu import Menu
import anim
import data

class Scenario:
    level = 0
    levels = []
    menuOn = False
    menu = None
    quit = False

    def __init__(self):
        menu = Menu()
        menu.set(0, anim.Slot(data.images['menu_newgame']), \
                    anim.Slot(data.images['menu_newgame_act']), self.newGame)
        menu.set(1, anim.Slot(data.images['menu_random']), \
                    anim.Slot(data.images['menu_random_act']), self.randomLevel1)
        menu.set(2, anim.Slot(data.images['menu_random']), \
                    anim.Slot(data.images['menu_random_act']), self.randomLevel2)
        menu.set(4, anim.Slot(data.images['menu_quit']), \
                    anim.Slot(data.images['menu_quit_act']), self.end )
        self.menu = menu

        self.levels.append((0, 0, Level(0)))
        self.levels.append((1, 1, Level(1)))
        self.levels.append((2, 2, Level(2)))
        self.initLevel()
    #enddef

    def newGame(self):
        self.level = 1
        self.initLevel()
        self.menuOn = False
    #enddef

    def randomLevel(self):
        self.levels[self.level][2].generate()
        self.menuOn = False
    #enddef

    def randomLevel1(self):
        self.level = 1
        self.randomLevel()
    #enddef

    def randomLevel2(self):
        self.level = 2
        self.randomLevel()
    #enddef


    def end(self):
        self.quit = True
    #enddef

    def initLevel(self):
        self.levels[self.level][2].load()
    #enddef

    def draw(self):
        self.levels[self.level][2].draw()
        if self.menuOn:
            self.menu.draw()
    #enddef

    def behave(self):
        if self.menuOn:
            self.menu.behave()
        else:
            self.levels[self.level][2].behave()

        if core.controls.exit:
            self.menuOn = not self.menuOn
            core.controls.exit = False
    #enddef

#endclass
