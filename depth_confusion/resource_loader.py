"""
A utility module for managing sprites and other resources
Author: Huba Nagy
"""
import pygame



class ImageHandler:
	def __init__(self):
		self._images = {}
	
	def load_image(self, image_path, image_id):
		self._images[image_id] = pygame.image.load(image_path)
	
	
	def get_image(self, image_id):
		try:
			return self._images[image_id]
	
	
		except KeyError:
			return None
	
	



class EntityHandler:
	def __init__(self):
		self._entities = {}
	
	def add_entity(self, entity_class, entity_id, image_id):
		pass 
	
	


