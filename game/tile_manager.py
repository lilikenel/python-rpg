from pathlib import Path

import pygame

from game import settings
from game.enums.tile_types import TileTypesEnum

class TileManager:

	def __init__(self, map_id: int) -> None:
		self.map_id: int = map_id
		self.map_tile_data: list[list[int]] = self._load_map_tile_data()
		self.world_width: int = len(self.map_tile_data[0]) * settings.TILE_SIZE
		self.world_height: int = len(self.map_tile_data) * settings.TILE_SIZE

		self.rendered_tile_images: dict[int, pygame.Surface] = {}

		for tile_type in TileTypesEnum:
			relative_path = f"res/tiles/tile_{tile_type.name}_01.png"
			self.rendered_tile_images[tile_type.value] = self._load_tile(relative_path)

	def _load_map_tile_data(self) -> list[list[int]]:
		map_module_name = f"game.maps.map_{self.map_id:02d}"
		try:
			map_module = __import__(map_module_name, fromlist=["MAP_DATA"])
		except ImportError as error:
			raise RuntimeError(f"Failed to import map module {map_module_name}: {error}") from error

		if not hasattr(map_module, "MAP_DATA"):
			raise RuntimeError(f"Map module {map_module_name} does not contain MAP_DATA")

		map_data = getattr(map_module, "MAP_DATA")
		if not isinstance(map_data, list) or not all(isinstance(row, list) for row in map_data):
			raise RuntimeError(f"MAP_DATA in {map_module_name} is not a valid 2D list")

		return map_data

	def _load_tile(self, relative_path: str) -> pygame.Surface:
		tile_path = Path(relative_path)
		if not tile_path.is_file():
			raise FileNotFoundError(f"Tile image not found: {tile_path.resolve()}")

		try:
			image = pygame.image.load(str(tile_path)).convert()
		except pygame.error as error:
			raise RuntimeError(f"Failed to load tile image {tile_path}: {error}") from error

		return pygame.transform.scale(image, (settings.TILE_SIZE, settings.TILE_SIZE))

	def draw(self, surface: pygame.Surface, camera_x: int, camera_y: int) -> None:
		for row_index, row in enumerate(self.map_tile_data):
			for col_index, tile in enumerate(row):

				world_x = col_index * settings.TILE_SIZE
				world_y = row_index * settings.TILE_SIZE

				screen_x = world_x - camera_x
				screen_y = world_y - camera_y

				surface.blit(self.rendered_tile_images[tile], (screen_x, screen_y))