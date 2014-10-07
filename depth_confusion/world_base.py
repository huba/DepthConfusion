"""
Author: Huba Nagy
"""
import pygame
from common_util import *



class WorldBase(object):
	"""
	Base class for different types of grid based world,
	this class is absolutely not intended for use outside this
	package so don't use it, it will throw errors at you. 
	See the tiles and the voxels modules.
	"""
	def __init__(self, resource_handler, element_class_handler,
	             grid_length, translation):
		self.resource_handler = resource_handler
		self.element_class_handler = element_class_handler
		
		self._grid = [None] * grid_length
	
	
	def on_update(self):
		pass
	
	
	def on_render(self, target_surface):
		pass
	
	
	def __iter__(self):
		"""
		Simply returns an iterator of the _grid, different types of worlds would need
		to iterate over their grid in different orders.
		"""
		return self._grid.__iter__()
	
	
	def __setitem__(self, coordinate, grid_element):
		"""
		Replaces the element at the given grid coordinate with a given grid element.
		"""
		try:
			#validate the coordinate and calculate the index of the desired grid element
			self._validate_coordinate(coordinate)
			old_element = self[coordinate]
			index = self._coordinate_to_index(coordinate)
			
			#replace the given grid element
			self._grid[index] = grid_element
			grid_element.put_into_world(self, *coordinate)
			
			if old_element:
				old_element.on_destroy()
			
			grid_element.on_create()
		
		except OutOfIt as out_of_this_world:
			print(out_of_this_world)
		
		except ValueError:
			print('Not enough digits in the coordinate {0}!'.format(coordinate))
		
		except TypeError:
			print('Not enough digits in the coordinate {0}!'.format(coordinate))
	
	
	def __getitem__(self, coordinate):
		"""
		Gets the element from the given grid coordinate.
		"""
		try:
			#validate the coordinate and calculate the index of the desired grid element
			self._validate_coordinate(coordinate)
			index = self._coordinate_to_index(coordinate)
			
			#replace the given grid element
			return self._grid[index]
		
		except OutOfIt as out_of_this_world:
			print(out_of_this_world)
		
		except ValueError:
			print('Not enough digits in the coordinate {0}!'.format(coordinate))
	
	
	def __delitem__(self, coordinate):
		"""
		Replaces the element at the given grid coordinate with
		the void type element of the element_class_handler...
		"""
                self[coordinate].on_destroy()
		self[coordinate] = self.element_class_handler.construct_element('void')
	
	
	def _validate_coordinate(self, coordinate):
		pass
	
	
	def _coordinate_to_index(self, coordinate):
		return 0
	
	



class GridElement(object):
	"""
	Avoid using this class at all cost similarly to WorldBase.
	If you use it and it blows up on you it's your fault. :) Thanks.
	"""
	def __init__(self):
		pass
	
	
	def put_into_world(self, world, coordinate):
		pass
	
	
	def remove_from_world(self):
		pass
	
	
	def on_update(self):
		"""
		A hook to implement that is called befor this is rendered
		"""
		pass
	
	
	def on_render(self, target_surface, translation):
		"""
		A hook that is called by the world
		"""
		pass
	
	
	def on_create(self):
		"""
		A hook to implement that is called when this is added to a world
		"""
		pass
	
	
	def on_destroy(self):
		"""
		A hook to implement that is called when this is removed from a world
		"""
		pass
	
	



class ElementClassHandler:
	def __init__(self, void_type):
		self._element_types = {}
		self.add_element_type('void', void_type)
	
	
	def add_element_type(self, element_id, base_class):
		self._element_types[element_id] = base_class
	
	
	def construct_element(self, element_id, *args):
		try:
			return self._element_types[element_id]()
		
		except:
			return self._element_types['void']()
	
	


