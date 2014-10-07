"""
A moudel whith generic utilities used throughout the other modules
Author: Huba Nagy
"""
import pygame
import mpmath as mp

#indexes in coordinate tuples for better readibility
WIDTH = X = 0
HEIGHT = Y = 1
DEPTH = Z = 2

#Colors for mapping coordinates
TEST_RED = pygame.Color(255, 0, 0, 255)#-16776961
TEST_GREEN = pygame.Color(0, 255, 0, 255)#-16711936
TEST_YELLOW = pygame.Color(255, 0, 255, 255)#-16711681
TEST_BLUE = pygame.Color(0, 0, 255, 255)#-65536

#Visibility flags
SHOW_ALL = 0
ONLY_SHOW_EXPOSED = 1

#135 degrees
THETA = 3 * mp.pi / 4

#Isometric Unprojection
UNPROJECT = mp.matrix([[1,  0, 0],
                       [0, -1, 0], #NOTE: the y coordinate has to be inverted because my
                       [0,  0, 1]]) #grid coordinates are a bit weird

UNPROJECT *= mp.matrix([[ mp.cos(THETA),  mp.sin(THETA), 0],
                       [-mp.sin(THETA),  mp.cos(THETA), 0],
                       [             0,              0, 1]])

UNPROJECT *= mp.matrix([[1, 0, 0],
                        [0, 2, 0],
                        [0, 0, 1]])


class OutOfIt(Exception):
	def __init__(self, msg, value):
		self.msg = msg
		self.value = value
	
	
	def __repr__(self):
		return '{0} {1}'.format(self.msg, self.value)
	
	


