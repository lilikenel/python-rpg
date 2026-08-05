import pygame

from game import settings
from game.object_manager import ObjectManager
from game.player import Player
from game.tile_manager import TileManager


class Game:

	def __init__(self) -> None:
		pygame.init()
		self.screen: pygame.Surface = pygame.display.set_mode(
			(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
		)
		pygame.display.set_caption(settings.WINDOW_TITLE)

		self.clock: pygame.time.Clock = pygame.time.Clock()
		self.is_running: bool = False

		self.map_id: int = 1
		self.tile_manager: TileManager = TileManager(self.map_id)
		self.object_manager: ObjectManager = ObjectManager(self.map_id)
		self.player: Player = Player()

		self.camera_x: int = 0
		self.camera_y: int = 0

	def run(self) -> None:
		self.is_running = True
		try:
			while self.is_running:
				delta_seconds = self.clock.tick(settings.FPS) / 1000.0
				self._process_events()
				self._update(delta_seconds)
				self._draw()
		finally:
			pygame.quit()

	def _process_events(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

	def _update(self, delta_seconds: float) -> None:
		pressed_keys = pygame.key.get_pressed()
		self.player.update(pressed_keys, delta_seconds)

	def _draw(self) -> None:
		self.screen.fill(settings.BACKGROUND_COLOR)

		self.camera_x = int(self.player.x - (settings.SCREEN_WIDTH / 2) + (settings.TILE_SIZE / 2))
		self.camera_y = int(self.player.y - (settings.SCREEN_HEIGHT / 2) + (settings.TILE_SIZE / 2))

		self.camera_x = max(0, min(self.camera_x, self.tile_manager.world_width - settings.SCREEN_WIDTH))
		self.camera_y = max(0, min(self.camera_y, self.tile_manager.world_height - settings.SCREEN_HEIGHT))

		self.tile_manager.draw(self.screen, self.camera_x, self.camera_y)
		self.object_manager.draw(self.screen, self.camera_x, self.camera_y)
		self.player.draw(self.screen, self.camera_x, self.camera_y)
		pygame.display.flip()
