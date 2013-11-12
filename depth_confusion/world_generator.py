"""
A utility module for generating maps
Author: Huba Nagy
"""
import voxels
from voxels import WIDTH, HEIGHT, DEPTH


def generate_flat(dimensions, fill_height, voxel_handler, image_handler, fill_voxel_id):
	#Hint: IRON MAIDEN Song and a novel that takes place in a futuristic dystopia
	brave_new_world = voxels.VoxelWorld(image_handler, voxel_handler, world_dimensions = dimensions)
	
	for z in xrange(dimensions[DEPTH]):
		for y in xrange(dimensions[HEIGHT]):
			for x in xrange(dimensions[WIDTH]):
				new_voxel = voxel_handler.construct_voxel('grass-block') if z < fill_height else voxel_handler.construct_voxel('void')
				brave_new_world.set_voxel(x, y, z, new_voxel)
	
	return brave_new_world