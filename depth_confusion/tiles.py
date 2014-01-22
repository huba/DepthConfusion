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
	
	
	def global_to_map(self, global_coordinates):
		"""
		Maps screen coordinates to world coordinates
		"""
		(gx, gy) = global_coordinates
		
		#Calculate rough x, y, z coordinate in the map
		mx = ((gy + self._active_layer * self._voxel_dimensions[DEPTH]) / (self._voxel_dimensions[HEIGHT] / 2) - gx / (self._voxel_dimensions[WIDTH] / 2)) / 2
		my = (gx / (self._voxel_dimensions[WIDTH] / 2) + (gy) / (self._voxel_dimensions[HEIGHT] / 2)) / 2
		
		#Calculate where the corner of the image is
		cx, cy = self.map_to_global(mx, my)
		#calculate where the screen cordinate is relative to the corner of the image
		ix, iy = gx - cx, gy - cy
		
		#print 'corner: {0}, {1}'.format(cx, cy)
		#print 'image: {0}, {1}'.format(ix, iy)
		
		#Check the image coordinate accuired above against the mouse helper image
		#and make corrections to the map coordinates if necessary
		pixel_array = pygame.PixelArray(self.image_handler.get_image('mouse-help'))
		pixel_color = pygame.Color(pixel_array[ix][iy])
		#print pixel_color
		if pixel_color == TEST_RED:
			#print 'got red'
			my -= 1
		
		elif pixel_color == TEST_GREEN:
			#print 'got green'
			mx -= 1
		
		elif pixel_color == TEST_BLUE:
			#print 'got blue'
			my += 1
		
		elif pixel_color == TEST_YELLOW:
			#print 'got yellow'
			mx += 1
		
		return (mx, my)
	
	
	def map_to_global(self, mx, my):
		"""
		Maps world coordinates the coordinates of the top left corner of the image on the world surface.
		No translation is applied yet.
		"""
		gx = - mx * (self._voxel_dimensions[WIDTH] / 2) + my * (self._voxel_dimensions[WIDTH] / 2)
		gy = my * (self._voxel_dimensions[HEIGHT] / 2)  + mx * (self._voxel_dimensions[HEIGHT] / 2)
		
		return (gx, gy)



class ElementaryTile:
	def __init__(self, tile_id, dimensions = (72, 36)):
		self._dimensions = dimensions
		self._image_size = dimensions
		self._coordinates = (0, 0)
		self._screen_coordinates = (0, 0)
		
		self._world = None
		self._tile_id = tile_id
	
	
	def put_into_world(self, world, x, y, ):
		self._coordinates = (x, y)
		self._world = world
		self._screen_coordinates = self._world.map_to_global(*self._coordinates)
	
	
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
	
	



class GroundTile(ElementaryTile):
	def __init__(self, tile_id, dimensions = (72, 36)):
		ElementaryTile.__init__(self, tile_id, dimensions)
	
	
	def on_render(self, target_surface, translation):
		coordinates = (self._screen_coordinates[0] + translation[0], self._screen_coordinates[1] + translation[1])
		#blit image
		target_surface.blit(self._world.image_handler.get_image(self._voxel_id), coordinates)
	
	


class Void(ElementaryTile):
	def __init__(self, dimensions = (72, 36)):
		ElementaryTile.__init__(self, 'void', dimensions)
	
	



class TileHandler(ElementClassHandler):
	def __init__(self):
		ElementClassHandler.__init__(self, Void)
		self.add_tile_type = self.add_element_type
		self.construct_tile = self.construct_element
	
	


