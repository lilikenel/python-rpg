import pygame

from game import settings
from game.enums.tile_types import TileTypesEnum
from game.utils.camera import Camera
from game.utils.image_loader import ImageLoader

class TileManager:

	def __init__(self, tiles: list[list[int]], image_cacher: ImageLoader) -> None:

		self.tiles: list[list[int]] = tiles
		self.image_loader: dict[int, pygame.Surface] = image_cacher.load_from_path("res/tiles/tile_{0}_01.png", TileTypesEnum)

	def draw(self, surface: pygame.Surface, camera: Camera) -> None:

		for row_index, row in enumerate(self.tiles):
			for col_index, tile in enumerate(row):

				map_x = col_index * settings.TILE_SIZE
				map_y = row_index * settings.TILE_SIZE

				screen_x, screen_y = camera.apply(map_x, map_y)

				surface.blit(self.image_loader[tile], (screen_x, screen_y))
