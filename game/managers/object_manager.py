import pygame

from game import settings
from game.enums.object_types import ObjectTypesEnum
from game.utils.camera import Camera
from game.utils.image_loader import ImageLoader

class ObjectManager:

	def __init__(self, objects: list[tuple[int, int, int]], image_cacher: ImageLoader) -> None:

		self.objects: list[tuple[int, int, int]] = objects
		self.image_loader: dict[int, pygame.Surface] = image_cacher.load_from_path("res/objects/object_{0}_01.png", ObjectTypesEnum, colorkey=(0, 0, 0))

	def draw(self, surface: pygame.Surface, camera: Camera) -> None:

		for object_data in self.objects:

			col, row, object_type = object_data

			map_x = col * settings.TILE_SIZE
			map_y = row * settings.TILE_SIZE

			screen_x, screen_y = camera.apply(map_x, map_y)

			surface.blit(self.image_loader[object_type], (screen_x, screen_y))