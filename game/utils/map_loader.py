import importlib
from types import ModuleType
from typing import Callable

from game import settings


class MapLoader:

	def __init__(self, map_id: int) -> None:

		map_module_name: str = f"game.maps.map_{map_id:02d}"
		map_module: ModuleType = self._import_map_module(map_module_name)

		self.tiles: list[list[int]] = self._read(map_module, "MAP_DATA", self._is_tile_list)
		self.objects: list[tuple[int, int, int]] = self._read(map_module, "OBJECTS", self._is_object_list)

		self.map_width: int = len(self.tiles[0]) * settings.TILE_SIZE if self.tiles else 0
		self.map_height: int = len(self.tiles) * settings.TILE_SIZE if self.tiles else 0

	def _import_map_module(self, map_module_name: str) -> ModuleType:

		try:
			map_module = importlib.import_module(map_module_name)

		except ImportError as error:
			raise RuntimeError(f"Failed to import map module {map_module_name}: {error}") from error
		
		return map_module

	def _read(self, module: ModuleType, attribute_name: str, is_valid: Callable[[object], bool]) -> object:

		if not hasattr(module, attribute_name):
			raise RuntimeError(f"Map module {module.__name__} does not contain {attribute_name}")

		data: object = getattr(module, attribute_name)

		if not is_valid(data):
			raise RuntimeError(f"{attribute_name} in {module.__name__} is not valid")

		return data

	@staticmethod
	def _is_tile_list(data: object) -> bool:

		return isinstance(data, list) and all(isinstance(row, list) for row in data)

	@staticmethod
	def _is_object_list(data: object) -> bool:

		return isinstance(data, list) and all(isinstance(obj, tuple) and len(obj) == 3 for obj in data)