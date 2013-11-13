"""
A moudel whith generic utilities used throughout the other modules
Author: Huba Nagy
"""
import pygame

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



class OutOfIt(Exception):
	def __init__(self, msg, value):
		self.msg = msg
		self.value = value
	
	
	def __repr__(self):
		return '{0} {1}'.format(self.msg, self.value)