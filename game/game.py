import pygame

from game import settings
from game.camera import Camera
from game.object_manager import ObjectManager
from game.player_manager import PlayerManager
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
		self.camera: Camera = Camera(self.tile_manager.map_width, self.tile_manager.map_height)
		self.player_manager: PlayerManager = PlayerManager()

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
		self.player_manager.update(pressed_keys, delta_seconds)
		self.camera.update(self.player_manager.map_x, self.player_manager.map_y)

	def _draw(self) -> None:

		self.screen.fill(settings.BACKGROUND_COLOR)

		self.tile_manager.draw(self.screen, self.camera)
		self.object_manager.draw(self.screen, self.camera)
		self.player_manager.draw(self.screen, self.camera)
		pygame.display.flip()
