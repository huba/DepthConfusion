#!/usr/bin/env python2.7

import pygame
from pygame.locals import *

import depth_confusion



class GrassBlock(depth_confusion.voxels.Block):
	def __init__(self):
		depth_confusion.voxels.Block.__init__(self, 'grass-block')
	
	



class Camera:
	def __init__(self, dx, dy):
		self._dx, self._dy = dx, dy
	
	def apply_camera(self, target):
		target.translate(self._dx, self._dy)
	
	def move_camera(self, delta):
		self._dx += delta[0]
		self._dy += delta[1]



class Game:
	def __init__(self, w=600, h=480):
		self._running = False
		self._screen = None
		self._size = (self._width, self._height) = (w, h)
		self._camera = Camera(0, 0)
	
	
	def on_init(self):
		pygame.init()
		self._screen = pygame.display.set_mode(self._size)
		self._background = self._screen.copy()
		self._background.fill((100, 100, 100))
		self._clock = pygame.time.Clock()
		
		pygame.mouse.set_visible(True)
		
		voxel_handler = depth_confusion.voxels.VoxelHandler()
		voxel_handler.add_voxel_type('grass-block', GrassBlock)
		image_handler = depth_confusion.resource_loader.load_image_pack('example_image_pack/pack.json')
		
		self.world = depth_confusion.world_generator.generate_flat((4, 4, 4), 3, voxel_handler, image_handler, 'grass-block')
		
		return True
	
	
	def on_update(self):
		self._camera.apply_camera(self.world)
	
	
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
		
		elif event.type == pygame.MOUSEMOTION:
			#print 'pos: {0}, rel: {1}, buttons:{2}'.format(event.pos, event.rel, event.buttons)
			if event.buttons[2] == 1:
				self._camera.move_camera(event.rel)
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			#print event.button
			if event.button == 1:
				coordinates = self.world.map_to_world(*event.pos)
				voxel = self.world.get_voxel(*coordinates)
				if voxel:
					voxel.highlight()
			
			elif event.button == 4:
				self.world.scroll_layer(1)
			
			elif event.button == 5:
				self.world.scroll_layer(-1)
			
			elif event.button == 3:
				(mx, my, mz) = self.world.map_to_world(*event.pos)
				self.world.set_voxel(mx, my, mz, depth_confusion.voxels.Void())
				
	
	
	def on_render(self):
		self._screen.blit(self._background, (0, 0))
		self.world.on_render(self._screen)
		pygame.display.flip()
	
	
	def execute(self):
		self._running = self.on_init()
		
		while self._running:
			self._clock.tick(60)
			for event in pygame.event.get():
				self.on_event(event)
			
			self.on_update()
			self.on_render()
			
		
		pygame.quit()
	
	
	


if __name__ == '__main__':
	app = Game()
	app.execute()