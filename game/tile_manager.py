from pathlib import Path

import pygame

from game import settings


class TileManager:

	def __init__(self) -> None:
		self.mud_tile: pygame.Surface = self._load_tile("res/tiles/tile_mud_01.png")

	def _load_tile(self, relative_path: str) -> pygame.Surface:
		tile_path = Path(relative_path)
		if not tile_path.is_file():
			raise FileNotFoundError(f"Tile image not found: {tile_path.resolve()}")

		try:
			image = pygame.image.load(str(tile_path)).convert()
		except pygame.error as error:
			raise RuntimeError(f"Failed to load tile image {tile_path}: {error}") from error

		return pygame.transform.scale(image, (settings.TILE_SIZE, settings.TILE_SIZE))

	def draw(self, surface: pygame.Surface) -> None:
		for row in range(settings.MAX_SCREEN_ROW):
			for col in range(settings.MAX_SCREEN_COL):
				x = col * settings.TILE_SIZE
				y = row * settings.TILE_SIZE
				surface.blit(self.mud_tile, (x, y))
