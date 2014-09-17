"""
This module has the basic elements of a voxel based grid.
All the pixel coordinates are global here. This means bsolutely no scene
or screen pixel coordinates!"
Author: Huba Nagy
"""
import pygame
from common_util import *
from world_base import *
import mpmath as mp



class VoxelWorld(WorldBase):
	def __init__(self, resource_handler, voxel_handler,
	             world_dimensions = (64, 64, 16),
	             voxel_dimensions = (72, 36, 36),
	             active_layer = 0,
	             visibility_flag = ONLY_SHOW_EXPOSED):
		
		
		self._world_dimensions = world_dimensions
		self._voxel_dimensions = voxel_dimensions
		grid_length = world_dimensions[WIDTH] * world_dimensions[HEIGHT] * world_dimensions[DEPTH]
		
		self._active_layer = active_layer
		self.visibility_flag = visibility_flag
		
		WorldBase.__init__(self, resource_handler, voxel_handler,
		                   grid_length, (0, 0))
	
	
	def scroll_layer(self, dl):
		if self._world_dimensions[DEPTH] > (self._active_layer + dl) > -1:
			self._active_layer += dl
	
	
	def on_update(self):
		for mx, my, mz, voxel in self:
			if voxel:
				voxel.on_update()
	
	
	def __iter__(self):
		for mz in xrange(self._world_dimensions[WIDTH]):
			for my in xrange(self._world_dimensions[HEIGHT]):
				for mx in xrange(self._world_dimensions[DEPTH]):
					voxel = self[(mx, my, mz)]
					yield mx, my, mz, voxel
	
	
	def on_render(self, viewport):
		"""
		This function calls the render function of all voxels onto a given viewport
		"""
		for mx, my, mz, voxel in self:
			if self.visibility_flag == ONLY_SHOW_EXPOSED and mz > self._active_layer:
				return
			
			#Make sure it does not render anything else
			if isinstance(voxel, ElementaryVoxel):
				#Also make sure that only voxels in the view are rendered
				#if viewport.scene_to_global(viewport.scene.get_rect()).colliderect(viewport.global_to_scene(voxel.rect)):
				voxel.on_render(viewport)
	
	
	def on_event(self, event):
		pass
	
	
	def get_dimension(self, dimension):
		return self._world_dimensions[dimension]
	
	
	def is_voxel_rendered(self, coordinate):
		try:
			return self[coordinate].is_rendered()
		
		except AttributeError:
			return False
	
	
	def is_top_layer(self, coordinate):
		return coordinate[DEPTH] == self._active_layer
	
	
	def _coordinate_to_index(self, coordinate):
		"""
		Calculates the index in the list holding the _grid based on x, y and z 
		coordinates. z major y secondary and x minor
		"""
		(x, y, z) = coordinate
		return self._world_dimensions[WIDTH] * self._world_dimensions[HEIGHT] * z + self._world_dimensions[HEIGHT] * y + x
	
	
	def _validate_coordinate(self, coordinate):
		"""
		Validates that the world coordinates are actually within the world
		Make sure you handle the exceptions when you use this!!!
		"""
		(x, y, z) = coordinate
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
	
	
	def global_to_map(self, global_coordinates):
		"""
		Maps global coordinates to map coordinates. Mainly used to tell which 
		voxel the mouse pointer is on. Implementation based on article:
                http://www.alcove-games.com/advanced-tutorials/isometric-tile-picking/
		"""
		(gx, gy) = global_coordinates
		
                #REVERSE ISOMETRIC PROJECTION:
                #Rotation angle 135 degrees
                theta = 3 * mp.pi / 4
                
                #length of a side before iso projection
                side_length = mp.nint(self._voxel_dimensions[WIDTH] * mp.sin(mp.pi / 4))
                
                #rotate by angle
                unrotate = mp.matrix([[ mp.cos(theta), -mp.sin(theta), 0],
                                      [ mp.sin(theta),  mp.cos(theta), 0],
                                      [             0,              0, 1]])
                
                #unsquash vertically
                unsquash = mp.matrix([[1, 0, 0],
                                      [0, 2, 0],
                                      [0, 0, 1]])
                
                #depth info comes from the currently activated layer
                mz = self._active_layer
                #turn the global coordinates into an affine matrix
                g_coord = mp.matrix([[gx], [gy + mz * self._voxel_dimensions[DEPTH]], [1]])
                g_coord = unrotate * (unsquash * g_coord)
                
                #divide and round the coordinates to get integer indexes.
		mx = - int(mp.nint(g_coord[1]) / side_length)
                my = - int(mp.nint(g_coord[0]) / side_length)
		
		return (mx, my, mz)
	
	
	def map_to_global(self, mx, my, mz):
		"""
		Maps world coordinates the coordinates of the top left corner of the image on the world surface.
		No translation is applied yet. NOTE all the translation happens in the viewport.
		"""
		gx = - mx * (self._voxel_dimensions[WIDTH] / 2) + my * (self._voxel_dimensions[WIDTH] / 2) - (self._voxel_dimensions[WIDTH] / 2)
		gy = my * (self._voxel_dimensions[HEIGHT] / 2)  + mx * (self._voxel_dimensions[HEIGHT] / 2) - mz * self._voxel_dimensions[DEPTH]
		
		return (gx, gy)
	
	



class ElementaryVoxel(GridElement):
	def __init__(self, voxel_id, dimensions = (72, 36, 36)):
		self._dimensions = dimensions
		self._image_size = (dimensions[WIDTH], dimensions[HEIGHT] + dimensions[DEPTH])
		self._coordinates = (0, 0, 0)
		self._screen_coordinates = (0, 0)
		self.rect = pygame.Rect(self._screen_coordinates, self._image_size)
		
		self._world = None
		self._voxel_id = voxel_id
		self._highlighted = False
		self._rendered = False
	
	
	def is_rendered(self):
		return self._rendered
	
	
	def put_into_world(self, world, x, y, z):
		self._coordinates = (x, y, z)
		self._world = world
		self._screen_coordinates = self._world.map_to_global(*self._coordinates)
		self.rect = pygame.Rect(self._screen_coordinates, self._image_size)
	
	
	def highlight(self):
		self._highlighted = not self._highlighted
		#print 'highlighting {0}'.format(self)
	
	
	def on_update(self):
		"""
		A hook to implement that is called befor the voxel is rendered
		"""
		pass
	
	
	def on_render(self, viewport):
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
		if not self._world.is_voxel_rendered((mx, my - 1, mz)):
			#print '\tNothing behind'
			if not self._world.is_voxel_rendered((mx + 1, my - 1, mz)):
				#print '\t\tNothing to the left'
				self._dark_outline[5] = True
			
			if not self._world.is_voxel_rendered((mx, my - 1, mz + 1)):
				#print '\t\tNothing over'
				self._dark_outline[0] = True
		
		if not self._world.is_voxel_rendered((mx - 1, my, mz)):
			#print '\tNothing to the right'
			if not self._world.is_voxel_rendered((mx - 1, my + 1, mz)):
				#print '\t\tNothing infront'
				self._dark_outline[2] = True
			
			if not self._world.is_voxel_rendered((mx - 1, my, mz + 1)):
				#print '\t\tNothing over'
				self._dark_outline[1] = True
		
		if not self._world.is_voxel_rendered((mx, my, mz - 1)):
			if not self._world.is_voxel_rendered((mx, my + 1, mz)):
				if not self._world.is_voxel_rendered((mx, my + 1, mz -1)):
					self._dark_outline[3] = True
			
			if not self._world.is_voxel_rendered((mx + 1, my, mz)):
				if not self._world.is_voxel_rendered((mx + 1, my, mz -1)):
					self._dark_outline[4] = True
		
		if self._world.visibility_flag == ONLY_SHOW_EXPOSED:
			if (isinstance(self._world[(mx, my, mz + 1)], Block) and
			  not isinstance(self._world[(mx + 1, my, mz)], Void) and
			  not isinstance(self._world[(mx, my + 1, mz)], Void) and
			  not isinstance(self._world[(mx - 1, my, mz)], Void) and
			  not isinstance(self._world[(mx, my - 1, mz)], Void)):
				self._rendered = False
			
			else:
				self._rendered = True
		
		else:
			self._rendered = True
	
	
	def on_render(self, viewport):
		if not self._rendered:
			return
		
		
		coordinates = (int((self._screen_coordinates[X] + viewport.scene_placement[X]) * viewport.scene_scale), int((self._screen_coordinates[Y] + viewport.scene_placement[Y]) * viewport.scene_scale))
		
		target_surface = pygame.Surface(self.rect.size, flags = pygame.SRCALPHA)
		
		#blit the base image
		target_surface.blit(self._world.resource_handler.get_image(self._voxel_id), (0, 0))
		
		#blit the dark outlines
		(mx, my, mz) = self._coordinates
		for i in xrange(len(self._dark_outline)):
			if self._dark_outline[i]:
				target_surface.blit(self._world.resource_handler.get_image('overlay-dark-outline-{0}'.format(i)), (0, 0))
			
			elif (i == 0 or i == 1) and self._world.is_top_layer((mx, my, mz)):
				if i == 0 and not self._world.is_voxel_rendered((mx, my - 1, mz)):
					target_surface.blit(self._world.resource_handler.get_image('overlay-dark-outline-{0}'.format(i)), (0, 0))
				
				elif i == 1 and not self._world.is_voxel_rendered((mx - 1, my, mz)):
					target_surface.blit(self._world.resource_handler.get_image('overlay-dark-outline-{0}'.format(i)), (0, 0))
		
		#blit the highlight
		#NOTE: do not rely on this it will be removed
		if self._highlighted:
			target_surface.blit(self._world.resource_handler.get_image('overlay-yellow-highlight'), (0, 0))
		
		target_surface = pygame.transform.scale(target_surface, (int(self.rect.w * viewport.scene_scale), int(self.rect.h * viewport.scene_scale)))
		viewport.scene.blit(target_surface, coordinates)
	
	
	def on_create(self):
		(mx, my, mz) = self._coordinates
		#update own outlines
		self.update_visibility()
		#Update the visibility on all of the voxels around
		for ox in xrange(-1, 2):
			for oy in xrange(-1, 2):
				for oz in xrange(-1, 2):
					voxel = self._world[(mx + ox, my + oy, mz + oz)]
					if isinstance(voxel, Block):
						voxel.update_visibility()
	
	
	def on_destroy(self):
		(mx, my, mz) = self._coordinates
		#Update the visibility on all of the voxels around
		for ox in xrange(-1, 2):
			for oy in xrange(-1, 2):
				for oz in xrange(-1, 2):
					voxel = self._world[(mx + ox, my + oy, mz + oz)]
					if isinstance(voxel, Block):
						voxel.update_visibility()
	
	



class Void(ElementaryVoxel):
	def __init__(self, dimensions = (72, 36, 36)):
		ElementaryVoxel.__init__(self, 'void', dimensions)
		self._rendered = False
	
	



class VoxelHandler(ElementClassHandler):
	def __init__(self):
		ElementClassHandler.__init__(self, Void)
		self.add_voxel_type = self.add_element_type
		self.construct_voxel = self.construct_element
	
	


