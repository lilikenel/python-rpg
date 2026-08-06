import pygame

from game import settings
from game.enums.tile_types import TileTypesEnum
from game.utils.camera import Camera
from game.utils.image_loader import ImageLoader

class TileManager:

	def __init__(self, tiles: list[list[int]], image_cacher: ImageLoader) -> None:

		self.tiles: list[list[int]] = tiles
		self.image_loader: dict[int, pygame.Surface] = image_cacher.load_from_path("res/tiles/tile_{0}_01.png", TileTypesEnum)
	
	def is_solid_at(self, rect: pygame.Rect) -> bool:

		left_col = rect.left // settings.TILE_SIZE
		right_col = (rect.right - 1) // settings.TILE_SIZE
		top_row = rect.top // settings.TILE_SIZE
		bottom_row = (rect.bottom - 1) // settings.TILE_SIZE

		for row in range(top_row, bottom_row + 1):
			for col in range(left_col, right_col + 1):

				if row < 0 or row >= len(self.tiles) or col < 0 or col >= len(self.tiles[0]):
					return True
				
				tile_id = self.tiles[row][col]
				tile_type = TileTypesEnum(tile_id)

				if tile_type.is_blocking:
					return True

		return False

	def draw(self, surface: pygame.Surface, camera: Camera) -> None:

		for row_index, row in enumerate(self.tiles):
			for col_index, tile in enumerate(row):

				map_x = col_index * settings.TILE_SIZE
				map_y = row_index * settings.TILE_SIZE

				screen_x, screen_y = camera.apply(map_x, map_y)

				surface.blit(self.image_loader[tile], (screen_x, screen_y))
