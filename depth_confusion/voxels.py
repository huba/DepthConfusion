"""
This module has the basic elements of a voxel based grid
Author: Huba Nagy
"""
import pygame
from common_util import *



class VoxelWorld:
	def __init__(self, image_handler, voxel_handler,
	             world_dimensions = (64, 64, 16),
	             voxel_dimensions = (72, 36, 36),
	             active_layer = 0,
	             visibility_flag = ONLY_SHOW_EXPOSED):
		self.image_handler = image_handler
		self.voxel_handler = voxel_handler
		self.visibility_flag = visibility_flag
		self._world_dimensions = world_dimensions
		self._voxel_dimensions = voxel_dimensions
		self._grid = [None] * world_dimensions[WIDTH] * world_dimensions[HEIGHT] * world_dimensions[DEPTH]
		
		self._translation = (0, 0)
		self._active_layer = active_layer
	
	
	def translate(self, dx, dy):
		self._translation = (dx, dy)
	
	
	def scroll_layer(self, dl):
		if self._world_dimensions[DEPTH] > (self._active_layer + dl) > -1:
			self._active_layer += dl
	
	
	def on_update(self):
		for voxel in self._grid:
			if voxel:
				voxel.on_update()
	
	
	def on_render(self, target_surface):
		"""
		This function calls the render function of all voxels
		"""
		for mx in xrange(self._world_dimensions[WIDTH]):
			for my in xrange(self._world_dimensions[HEIGHT]):
				for mz in xrange(self._active_layer + 1):
					voxel = self.get_voxel(mx, my, mz)
					if isinstance(voxel, ElementaryVoxel):
						voxel.on_render(target_surface, self._translation)
	
	
	def on_event(self, event):
		pass
	
	
	def get_dimension(self, dimension):
		return self._world_dimensions[dimension]
	
	
	def get_voxel(self, mx, my, mz):
		"""
		Returns a handle to a voxel based on world coordinates
		"""
		try:
			self._validate_coordinates(mx, my, mz)
			return self._grid[self._get_index(mx, my, mz)]
		
		except OutOfIt as out_of_this_world:
			print out_of_this_world
	
	
	def is_voxel_rendered(self, mx, my, mz):
		try:
			return self.get_voxel(mx, my, mz).is_rendered()
		
		except AttributeError:
			return False
	
	
	def is_top_layer(self, mx, my, mz):
		return mz == self._active_layer
	
	def set_voxel(self, mx, my, mz, voxel):
		"""
		Sets a voxel in a given world coordinate
		"""
		try:
			self._validate_coordinates(mx, my, mz)
			old_voxel = self.get_voxel(mx, my, mz)
			
			self._grid[self._get_index(mx, my, mz)] = voxel
			voxel.put_into_world(self, mx, my, mz)
			
			if old_voxel:
				old_voxel.on_destroy()
			
			voxel.on_create()
		
		except OutOfIt as out_of_this_world:
			print out_of_this_world
	
	
	def _get_index(self, x, y, z):
		"""
		Calculates the index in the list holding the _grid based on x, y and z 
		coordinates. z major y secondary and x minor
		"""
		return self._world_dimensions[WIDTH] * self._world_dimensions[HEIGHT] * z + self._world_dimensions[HEIGHT] * y + x
	
	def _validate_coordinates(self, x, y, z):
		"""
		Validates that the world coordinot_of_this_worldates are actually within the world
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
		
		elif z < 0:
			raise OutOfIt('Z coordinate is less than 0...' , z)
		
		elif z >= self._world_dimensions[DEPTH]:
			raise OutOfIt('Z coordinate is more than the depth of the world...' , z)
	
	
	def map_to_world(self, sx, sy):
		"""
		Maps screen coordinates to world coordinates
		"""
		#Apply translation to screen coordinates
		sx -= self._translation[0]
		sy -= self._translation[1]
		
		#Calculate rough x, y, z coordinate in the map
		mx = ((sy + self._active_layer * self._voxel_dimensions[DEPTH]) / (self._voxel_dimensions[HEIGHT] / 2) - sx / (self._voxel_dimensions[WIDTH] / 2)) / 2
		my = (sx / (self._voxel_dimensions[WIDTH] / 2) + (sy + self._active_layer * self._voxel_dimensions[DEPTH]) / (self._voxel_dimensions[HEIGHT] / 2) ) / 2
		mz = self._active_layer
		
		#Calculate where the corner of the image is
		cx, cy = self.map_to_screen(mx, my, mz)
		#calculate where the screen cordinate is relative to the corner of the image
		ix, iy = sx - cx, sy - cy
		
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
		
		return (mx, my, mz)
	
	
	def map_to_screen(self, mx, my, mz):
		"""
		Maps world coordinates the coordinates of the top left corner of the image on the world surface.
		No translation is applied yet.
		"""
		sx = - mx * (self._voxel_dimensions[WIDTH] / 2) + my * (self._voxel_dimensions[WIDTH] / 2)
		sy = my * (self._voxel_dimensions[HEIGHT] / 2)  + mx * (self._voxel_dimensions[HEIGHT] / 2) - mz * self._voxel_dimensions[DEPTH]
		
		return (sx, sy)
	
	



class ElementaryVoxel:
	def __init__(self, voxel_id, dimensions = (72, 36, 36)):
		self._dimensions = dimensions
		self._image_size = (dimensions[WIDTH], dimensions[HEIGHT] + dimensions[DEPTH])
		self._coordinates = (0, 0, 0)
		self._screen_coordinates = (0, 0)
		
		self._world = None
		self._voxel_id = voxel_id
		self._highlighted = False
		self._rendered = False
	
	
	def is_rendered(self):
		return self._rendered
	
	
	def put_into_world(self, world, x, y, z):
		self._coordinates = (x, y, z)
		self._world = world
		self._screen_coordinates = self._world.map_to_screen(*self._coordinates)
	
	
	def highlight(self):
		self._highlighted = not self._highlighted
		#print 'highlighting {0}'.format(self)
	
	
	def on_update(self):
		"""
		A hook to implement that is called befor the voxel is rendered
		"""
		pass
	
	
	def on_render(self, target_surface, translation):
		"""
		How the voxel gets rendered
		"""
		pass
	
	
	def on_create(self):
		"""
		A hook to implement that is called when the voxel is added to a world
		"""
		pass
	
	
	def on_destroy(self):
		"""
		A hook to implement that is called when the voxel is removed from a world
		"""
		pass
	
	



class Block(ElementaryVoxel):
	def __init__(self, voxel_id, dimensions = (72, 36, 36)):
		ElementaryVoxel.__init__(self, voxel_id, dimensions)
		self._dark_outline = [False] * 6
		self._rendered = True
	
	
	def update_visibility(self):
		self._dark_outline = [False] * 6
		(mx, my, mz) = self._coordinates
		#print 'coordinates: {0}, {1}, {2}'.format(*self._coordinates)
		if not self._world.is_voxel_rendered(mx, my - 1, mz):
			#print '\tNothing behind'
			if not self._world.is_voxel_rendered(mx + 1, my - 1, mz):
				#print '\t\tNothing to the left'
				self._dark_outline[5] = True
			
			if not self._world.is_voxel_rendered(mx, my - 1, mz + 1):
				#print '\t\tNothing over'
				self._dark_outline[0] = True
		
		if not self._world.is_voxel_rendered(mx - 1, my, mz):
			#print '\tNothing to the right'
			if not self._world.is_voxel_rendered(mx - 1, my + 1, mz):
				#print '\t\tNothing infront'
				self._dark_outline[2] = True
			
			if not self._world.is_voxel_rendered(mx - 1, my, mz + 1):
				#print '\t\tNothing over'
				self._dark_outline[1] = True
		
		if not self._world.is_voxel_rendered(mx, my, mz - 1):
			if not self._world.is_voxel_rendered(mx, my + 1, mz):
				if not self._world.is_voxel_rendered(mx, my + 1, mz -1):
					self._dark_outline[3] = True
			
			if not self._world.is_voxel_rendered(mx + 1, my, mz):
				if not self._world.is_voxel_rendered(mx + 1, my, mz -1):
					self._dark_outline[4] = True
		
		if self._world.visibility_flag == ONLY_SHOW_EXPOSED:
			if (isinstance(self._world.get_voxel(mx, my, mz + 1), Block) and
			  not isinstance(self._world.get_voxel(mx + 1, my, mz), Void) and
			  not isinstance(self._world.get_voxel(mx, my + 1, mz), Void) and
			  not isinstance(self._world.get_voxel(mx - 1, my, mz), Void) and
			  not isinstance(self._world.get_voxel(mx, my - 1, mz), Void)):
				self._rendered = False
			
			else:
				self._rendered = True
		
		else:
			self._rendered = True
	
	
	def on_render(self, target_surface, translation):
		if not self._rendered:
			return
		
		coordinates = (self._screen_coordinates[0] + translation[0], self._screen_coordinates[1] + translation[1])
		#blit the base image
		target_surface.blit(self._world.image_handler.get_image(self._voxel_id), coordinates)
		
		#blit the dark outlines
		(mx, my, mz) = self._coordinates
		for i in xrange(len(self._dark_outline)):
			if self._dark_outline[i]:
				target_surface.blit(self._world.image_handler.get_image('overlay-dark-outline-{0}'.format(i)), coordinates)
			
			elif (i == 0 or i == 1) and self._world.is_top_layer(mx, my, mz):
				if i == 0 and not self._world.is_voxel_rendered(mx, my - 1, mz):
					target_surface.blit(self._world.image_handler.get_image('overlay-dark-outline-{0}'.format(i)), coordinates)
				
				elif i == 1 and not self._world.is_voxel_rendered(mx - 1, my, mz):
					target_surface.blit(self._world.image_handler.get_image('overlay-dark-outline-{0}'.format(i)), coordinates)
		
		#blit the highlight
		#NOTE: do not rely on this it will be removed
		if self._highlighted:
			target_surface.blit(self._world.image_handler.get_image('overlay-yellow-highlight'), coordinates)
	
	
	def on_create(self):
		(mx, my, mz) = self._coordinates
		#update own outlines
		self.update_visibility()
		#Update the visibility on all of the voxels around
		for ox in xrange(-1, 2):
			for oy in xrange(-1, 2):
				for oz in xrange(-1, 2):
					voxel = self._world.get_voxel(mx + ox, my + oy, mz + oz)
					if isinstance(voxel, Block):
						voxel.update_visibility()
	
	
	def on_destroy(self):
		(mx, my, mz) = self._coordinates
		#Update the visibility on all of the voxels around
		for ox in xrange(-1, 2):
			for oy in xrange(-1, 2):
				for oz in xrange(-1, 2):
					voxel = self._world.get_voxel(mx + ox, my + oy, mz + oz)
					if isinstance(voxel, Block):
						voxel.update_visibility()
	
	



class Void(ElementaryVoxel):
	def __init__(self, dimensions = (72, 36, 36)):
		ElementaryVoxel.__init__(self, 0, dimensions)
		self._rendered = False
	
	



class VoxelHandler:
	def __init__(self):
		self._voxel_types = {}
		self.add_voxel_type('void', Void)
	
	
	def add_voxel_type(self, voxel_id, base_class):
		self._voxel_types[voxel_id] = base_class
	
	
	def construct_voxel(self, voxel_id, *args):
		try:
			return self._voxel_types[voxel_id]()
		
		except:
			return Void()
	
	


