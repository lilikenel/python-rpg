from enum import Enum

class TileTypesEnum(Enum):

	def __new__(cls, tile_id: int, is_blocking: bool) -> "TileTypesEnum":
		obj = object.__new__(cls)
		obj._value_ = tile_id
		obj.is_blocking = is_blocking
		return obj

	mud = (1, False)
	grass = (2, False)
	water = (3, True)
	grass_flowers = (4, False)