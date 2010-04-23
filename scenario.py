import pygame
import core
from level import Level
from menu import Menu

class Scenario:
    level = 0
    levels = []
    menuOn = False
    menu = None
    quit = False

    def __init__(self):
        menu = Menu()
        menu.set(0, 'New Game', self.newGame)
        menu.set(1, 'Random Level', self.randomLevel)
        menu.set(3, 'Quit', self.end )
        self.menu = menu

        self.levels.append((0, 0, Level(0)))
        self.levels.append((1, 1, Level(1)))
        self.initLevel()
    #enddef

    def newGame(self):
        self.level = 1
        self.initLevel()
        self.menuOn = False
    #enddef

    def randomLevel(self):
        self.level = 1
        self.levels[self.level][2].generate()
        self.menuOn = False
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
