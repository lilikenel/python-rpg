from enum import Enum
from pathlib import Path

import pygame

from game import settings
from game.utils.camera import Camera


class Direction(Enum):

	UP = "up"
	DOWN = "down"
	LEFT = "left"
	RIGHT = "right"


class PlayerManager:

	def __init__(self) -> None:

		self.map_x: float = (settings.SCREEN_WIDTH / 2) - (settings.TILE_SIZE / 2)
		self.map_y: float = (settings.SCREEN_HEIGHT / 2) - (settings.TILE_SIZE / 2)
		self.speed: float = settings.PLAYER_SPEED

		self.facing_direction: Direction = Direction.DOWN

		self.sprite_number: int = 1
		self.sprite_timer: float = 0.0

		self.frames: dict[tuple[Direction, int], pygame.Surface] = self._load_frames()

	def _load_frames(self) -> dict[tuple[Direction, int], pygame.Surface]:

		filename_by_direction = {
			Direction.UP: "back",
			Direction.DOWN: "front",
			Direction.LEFT: "left",
			Direction.RIGHT: "right",
		}

		frames: dict[tuple[Direction, int], pygame.Surface] = {}

		for direction, name in filename_by_direction.items():
			for frame_number in (1, 2):
				relative_path = f"res/hero/hero_{name}_0{frame_number}.png"
				frames[(direction, frame_number)] = self._load_image(relative_path)

		return frames

	def _load_image(self, relative_path: str) -> pygame.Surface:

		image_path = Path(relative_path)

		if not image_path.is_file():
			raise FileNotFoundError(f"Hero image not found: {image_path.resolve()}")

		try:
			image = pygame.image.load(str(image_path)).convert_alpha()

		except pygame.error as error:
			raise RuntimeError(f"Failed to load hero image {image_path}: {error}") from error

		return pygame.transform.scale(image, (settings.TILE_SIZE, settings.TILE_SIZE))

	def update(self, pressed_keys: pygame.key.ScancodeWrapper, delta_seconds: float) -> None:

		move_x, move_y = self._read_movement_input(pressed_keys)
		is_moving = move_x != 0 or move_y != 0

		if is_moving:
			self._face(move_x, move_y)
			self._move(move_x, move_y, delta_seconds)
			self._advance_animation(delta_seconds)
		else:
			self.sprite_number = 1
			self.sprite_timer = 0.0

	def _read_movement_input(

		self, pressed_keys: pygame.key.ScancodeWrapper
	) -> tuple[int, int]:
		move_x = 0
		move_y = 0

		if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
			move_y -= 1
		if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
			move_y += 1
		if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
			move_x -= 1
		if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
			move_x += 1

		return move_x, move_y

	def _face(self, move_x: int, move_y: int) -> None:

		if move_y < 0:
			self.facing_direction = Direction.UP
		elif move_y > 0:
			self.facing_direction = Direction.DOWN
		elif move_x < 0:
			self.facing_direction = Direction.LEFT
		elif move_x > 0:
			self.facing_direction = Direction.RIGHT

	def _move(self, move_x: int, move_y: int, delta_seconds: float) -> None:

		distance = self.speed * delta_seconds

		if move_x != 0 and move_y != 0:
			diagonal_factor = 0.70710678  # 1 / sqrt(2)
			self.map_x += move_x * distance * diagonal_factor
			self.map_y += move_y * distance * diagonal_factor
		else:
			self.map_x += move_x * distance
			self.map_y += move_y * distance

	def _advance_animation(self, delta_seconds: float) -> None:

		self.sprite_timer += delta_seconds

		if self.sprite_timer >= settings.WALK_ANIMATION_INTERVAL:
			
			self.sprite_number = 2 if self.sprite_number == 1 else 1
			self.sprite_timer = 0.0

	def draw(self, surface: pygame.Surface, camera: Camera) -> None:

		current_frame = self.frames[(self.facing_direction, self.sprite_number)]

		screen_x, screen_y = camera.apply(self.map_x, self.map_y)

		surface.blit(current_frame, (round(screen_x), round(screen_y)))