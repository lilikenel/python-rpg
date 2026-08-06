from game import settings


class Camera:

	def __init__(self, map_width: int, map_height: int) -> None:

		self.map_width: int = map_width
		self.map_height: int = map_height
		self.camera_x: int = 0
		self.camera_y: int = 0

	def update(self, target_x: float, target_y: float) -> None:

		self.camera_x = int(target_x - (settings.SCREEN_WIDTH / 2) + (settings.TILE_SIZE / 2))
		self.camera_y = int(target_y - (settings.SCREEN_HEIGHT / 2) + (settings.TILE_SIZE / 2))

		self.camera_x = max(0, min(self.camera_x, self.map_width - settings.SCREEN_WIDTH))
		self.camera_y = max(0, min(self.camera_y, self.map_height - settings.SCREEN_HEIGHT))

	def apply(self, map_x: int, map_y: int) -> tuple[int, int]:
		
		return map_x - self.camera_x, map_y - self.camera_y
