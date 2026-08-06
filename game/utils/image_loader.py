from enum import Enum
import pygame
from pathlib import Path

from game import settings


class ImageLoader:

	def __init__(self) -> None:
		pass

	def _load_image(self, relative_path: str, colorkey: tuple[int, int, int] | None = None) -> pygame.Surface:

		object_path = Path(relative_path)

		if not object_path.is_file():
			raise FileNotFoundError(f"Image not found: {object_path.resolve()}")

		try:
			image = pygame.image.load(str(object_path))

		except pygame.error as error:
			raise RuntimeError(f"Failed to load object image {object_path}: {error}") from error

		if colorkey is not None:
			surface = image.convert()
			surface.set_colorkey(colorkey)
		else:
			surface = image.convert_alpha()

		return pygame.transform.scale(surface, (settings.TILE_SIZE, settings.TILE_SIZE))

	def load_from_path(self, relative_path: str, enum_class: type[Enum], colorkey: tuple[int, int, int] | None = None) -> dict[int, pygame.Surface]:

		loaded_images: dict[int, pygame.Surface] = {}

		for item in enum_class:
			item_relative_path = relative_path.format(item.name)
			image = self._load_image(item_relative_path, colorkey)
			loaded_images[item.value] = image

		return loaded_images
