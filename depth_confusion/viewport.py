"""
This module is where all the dark magic used for transformations 
and translation between screen and scene coordinates lives.

Also I think I should elaborate on some of my coordinate naming here:
*map/grid coordinates are the integer coordinates for referencing elements in a grid
*global coordinates are pixel coordinates that are relative to the top left
corner of the entire world's image
*scene coordinates are coordinates relative to the top left corner of the viewport
*screen coordinates are relative to the top left corner of the screen

Author: Huba Nagy
"""
import pygame
import mpmath as mp
from common_util import *

class Viewport(object):
	"""
	This object keeps track of transformations, you can blit it anywhere on the screen
	it is esentially a viewport. It can be attached to a World object.
	This will later be part of a possible gui api. One day...
	#TODO: implement transformations using mpmath. ATM I'm just figuring out what should happen.
	"""
	def __init__(self, screen, placement = (0, 0), scene_dimensions = None, bg_color = (100, 100, 100)):
		self._world = None
		#the target screen which the final image of the screen is blitted onto
		self.screen = screen
		#the placement of the final image of the scene on the screen defaults to the top left corner
		#these are screen coordinates
		self.screen_placement = placement
                self.scr_t = mp.matrix([[1, 0, placement[X]],
                                        [0, 1, placement[Y]],
                                        [0, 0,            1]])
		
		#Scene is a surface which everything in the world is blitted onto
		if not scene_dimensions:
			#the scene's width and height defaults to the width and height of the screen
			scene_dimensions = (screen.get_width(), screen.get_height())
		
		self.scene = pygame.Surface(scene_dimensions)
		self.scene_rect = self.scene.get_rect()
		
		#the placement of the viewport in terms of global coordinates
		self.scene_placement = (0, 0)
		self.scene_scale = 1
		
		self.bg_color = bg_color
	
	
	def on_render(self):
		self.scene.fill(self.bg_color)
		if self._world:
			self._world.on_render(self)
			#self.blit_scene = pygame.transform.scale(self.scene, (int(self.scene_rect.w * self.scene_scale), int(self.scene_rect.h * self.scene_scale)))
			self.screen.blit(self.scene, self.screen_placement)
	
	
	def attach_to_world(self, world):
		if not self._world:
			self._world = world
	
	
	def deattach_from_world(self, world):
		if self._world:
			self._world = None
	
	
	def pan_view(self, delta):
		"""
		Changes the xy coordinates of the scene by the xy coordinates of the delta
		"""
		self.scene_placement = (self.scene_placement[X] + delta[X], self.scene_placement[Y] + delta[Y])
        
        
        def center_on(self, coordinate):
            """Centers view on given coordinate"""
            #TODO: implement this, first need to sort out zooming though...
            pass
	
	
	def global_to_scene(self, global_coordinates):
		if isinstance(global_coordinates, pygame.Rect):
			(gx, gy) = global_coordinates.topleft
			(w, h) = global_coordinates.size
		
		else:
			(gx, gy) = global_coordinates
		
		#Do the translation here
		scn_x = int((self.scene_placement[X] + gx) * self.scene_scale)
		scn_y = int((self.scene_placement[Y] + gy) * self.scene_scale)
		
		if isinstance(global_coordinates, pygame.Rect):
			return pygame.Rect((scn_x, scn_y), (int(w * self.scene_scale), int(h * self.scene_scale)))
		
		else:
			return (scn_x, scn_y)
	
	
	def scene_to_global(self, scene_coordinates):
		if isinstance(scene_coordinates, pygame.Rect):
			(scn_x, scn_y) = scene_coordinates.topleft
			(w, h) = scene_coordinates.size
		
		else:
			(scn_x, scn_y) = scene_coordinates
		
		#Do the translation here
		gx = int(scn_x / self.scene_scale) - self.scene_placement[X]
		gy = int(scn_y / self.scene_scale) - self.scene_placement[Y]
		
		if isinstance(scene_coordinates, pygame.Rect):
			return pygame.Rect((gx, gy), (int(w * self.scene_scale), int(h * self.scene_scale)))
		
		else:
			return (gx, gy)
	
	
	def scene_to_screen(self, scene_coordinates):
		if isinstance(scene_coordinates, pygame.Rect):
			(scn_x, scn_y) = scene_coordinates.topleft
		
		else:
			(scn_x, scn_y) = scene_coordinates
		
		#Do the translation here
		scr_x = scn_x - self.screen_placement[X]
		scr_y = scn_y - self.screen_placement[Y]
		
		if isinstance(scene_coordinates, pygame.Rect):
			return pygame.Rect((scr_x, scr_y), scene_coordinates.size)
		
		else:
			return (scr_x, scr_y)
	
	
	def screen_to_scene(self, screen_coordinates):
		if isinstance(screen_coordinates, pygame.Rect):
			(scr_x, scr_y) = screen_coordinates.topleft
		
		else:
			(scr_x, scr_y) = screen_coordinates
		
		#Do the translation here
		scn_x = (scr_x + self.screen_placement[X])
		scn_y = (scr_y + self.screen_placement[Y])
		
		if isinstance(screen_coordinates, pygame.Rect):
			return pygame.Rect((scn_x, scn_y), screen_coordinates.size)
		
		else:
			return (scn_x, scn_y)
	
	
	def screen_to_global(self, screen_coordinates):
		if isinstance(screen_coordinates, pygame.Rect):
			(scr_x, scr_y) = screen_coordinates.topleft
		
		else:
			(scr_x, scr_y) = screen_coordinates
		
		#Do the translation here
		g_x = scr_x - self.screen_placement[X] - self.scene_placement[X]
		g_y = scr_y - self.screen_placement[Y] - self.scene_placement[Y]
                
                #print "clicked on {}".format((g_x, g_y))
                
		if isinstance(screen_coordinates, pygame.Rect):
			return pygame.Rect((g_x, g_y), screen_coordinates.size)
		
		else:
			return (g_x, g_y)


