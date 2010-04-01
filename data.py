import pygame

playerShip = None
tiles = None
alien = None


def init():
	global playerShip, tiles, alien
	playerShip = pygame.image.load('img/module.png').convert()
	alien = pygame.image.load('img/alien.png').convert()

#enddef
