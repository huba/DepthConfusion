"""
Module with a class to represent a flat isometric tile grid
Author: Huba Nagy
"""
import pygame
from common_util import *



class TiledWorld:
	def __init__(self, image_handler, tile_handler,
	             world_dimensions = (64, 64),
	             tile_dimensions = (72, 36)):
		self.image_handler = image_handler
		self.tile_handler = tile_handler
		
		self._world_dimensions = world_dimensions
		self._tile_dimensions = tile_dimensions
		self._grid = [None] * world_dimensions[WIDTH] * world_dimensions[HEIGHT]
		
		self._translation = (0, 0)
	
	
	def translate(self, dx, dy):
		self._translation = (dx, dy)
	
	
	def on_update(self):
		for tile in self._grid:
			if tile:
				tile.on_update()
	
	
	def on_render(self, target_surface):
		for mx in xrange(self._world_dimensions[WIDTH]):
			for my in xrange(self.world_dimensions[HEIGHT]):
				
	
	
	def on_event(self, event):
		pass
	
	
	def get_dimension(self, dimension):
		return self._world_dimensions[dimension]
	
	
	def get_tile(self, mx, my):
		try:
			self._validate_coordinates(mx, my)
			return self._grid[self._get_index(mx, my)]
		
		except OutOfIt as out_of_this_world:
			print out_of_this_world
	
	def set_tile(self, mx, my, tile):
		pass
	
	
	def _get_index(self, x, y, z):
		return self._world_dimensions[WIDTH] * y x
	
	
	def _validate_coordinates(self, x, y, z):
		"""
		Validates that the world coordinoates are actually within the world
		Make sure you handle the exceptions when you use this!!!
		"""
		if x < 0:
			raise OutOfIt('X coordinate is less than 0...' , x)
		
		elif x >= self._world_dimensions[WIDTH]:
			raise OutOfIt('X coordinate is more than the width of the world...' , x)
		
		elif y < 0:
			raise OutOfIt('Y coordinate is less than 0...' , y)
		
		elif y >= self._world_dimensions[HEIGHT]:
			raise OutOfIt('Y coordinate is more than the height of the world...' , y)
	
	
	def map_to_world(self, sx, sy):
		pass
	
	
	def map_to_screen(self, mx, my):
		pass



class ElementaryTile:
	def __init__(self):
		pass
	
	
	def put_into_world(self, world, x, y, ):
		self._coordinates = (x, y)
		self._world = world
		self._screen_coordinates = self._world.map_to_screen(*self._coordinates)
	
	
	def on_update(self):
		"""
		A hook to implement that is called befor the tile is rendered
		"""
		pass
	
	
	def on_render(self, target_surface, translation):
		"""
		How the tile gets rendered
		"""
		pass
	
	
	def on_create(self):
		"""
		A hook to implement that is called when the tile is added to a world
		"""
		pass
	
	
	def on_destroy(self):
		"""
		A hook to implement that is called when the tile is removed from a world
		"""
		pass
	
	