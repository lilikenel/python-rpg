from pathlib import Path

import pygame

from game import settings
from game.enums.object_types import ObjectTypesEnum

class ObjectManager:
	def __init__(self, map_id: int):
		self.map_id = map_id
		self.map_object_data = self._load_map_object_data()

		self.rendered_object_images: dict[int, pygame.Surface] = {}

		for object_type in ObjectTypesEnum:
			relative_path = f"res/objects/object_{object_type.name}_01.png"
			self.rendered_object_images[object_type.value] = self._load_object(relative_path)

	def _load_map_object_data(self) -> list[tuple[int, int, int]]:
		map_module_name = f"game.maps.map_{self.map_id:02d}"
		try:
			map_module = __import__(map_module_name, fromlist=["OBJECTS"])
		except ImportError as error:
			raise RuntimeError(f"Failed to import map module {map_module_name}: {error}") from error

		if not hasattr(map_module, "OBJECTS"):
			raise RuntimeError(f"Map module {map_module_name} does not contain OBJECTS")

		object_data = getattr(map_module, "OBJECTS")
		if not isinstance(object_data, list) or not all(isinstance(obj, tuple) and len(obj) == 3 for obj in object_data):
			raise RuntimeError(f"OBJECTS in {map_module_name} is not a valid list of tuples")

		return object_data
	
	def _load_object(self, relative_path: str) -> pygame.Surface:
		object_path = Path(relative_path)
		if not object_path.is_file():
			raise FileNotFoundError(f"Object image not found: {object_path.resolve()}")

		try:
			image = pygame.image.load(str(object_path)).convert()
			image.set_colorkey((0, 0, 0))
		except pygame.error as error:
			raise RuntimeError(f"Failed to load object image {object_path}: {error}") from error

		return pygame.transform.scale(image, (settings.TILE_SIZE, settings.TILE_SIZE))

	def draw(self, surface: pygame.Surface, camera_x: int, camera_y: int) -> None:
		for obj in self.map_object_data:
			x, y, obj_type = obj
			world_x = x * settings.TILE_SIZE
			world_y = y * settings.TILE_SIZE
			screen_x = world_x - camera_x
			screen_y = world_y - camera_y
			surface.blit(self.rendered_object_images[obj_type], (screen_x, screen_y))