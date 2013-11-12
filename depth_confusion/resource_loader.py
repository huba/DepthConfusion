"""
A utility module for managing sprites and other resources
Author: Huba Nagy
"""
import pygame
import json



class ImageHandler:
	def __init__(self, root):
		self._images = {}
		self._root = root
	
	def load_image(self, image_path, image_id):
		print('loaded image: {0} as {1}.'.format(image_path, image_id))
		self._images[image_id] = pygame.image.load(self._root + '/' + image_path)
	
	
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
	
	



def as_image_pack(dct):
	if '__image_paths__' in dct:
		image_handler = ImageHandler(dct['__root__'])
		for image_id in dct['__image_paths__']:
			image_handler.load_image(dct['__image_paths__'][str(image_id)], str(image_id))
		
		return image_handler
	
	else:
		return dct


def load_image_pack(filepath):
	f_object = open(filepath)
	return json.load(f_object, object_hook = as_image_pack)

