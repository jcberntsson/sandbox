from typing import Set
import pygame as pg

from lib.core.collision import compute_collision_states
from lib.core.player import Player
from lib.core.states import CollisionState
from lib.sprites.platform import Platform
from lib.utilities.constants import SCREEN_HEIGHT, GROUND_IMG_PATH, SCREEN_WIDTH


class Level:
    """Class for constructing a level scene from settings."""

    def __init__(self, settings: dict):
        self._settings = settings
        self._world_width = SCREEN_WIDTH
        self._platform_height = 16
        self._ground_height = 64
        self.ground = self._create_ground()
        self.platforms = self._create_platforms()

    def get_height(self) -> int:
        return self._ground_height

    @property
    def _objects(self):
        return list(self.platforms) + list(self.ground)

    def _create_ground_sprite(self, start: int, end: int) -> Platform:
        y_pos = SCREEN_HEIGHT - self._ground_height
        size = (end - start, self._ground_height)
        return Platform(GROUND_IMG_PATH, (start, y_pos), size)

    def _create_platform_sprite(self, start: int, end: int, y_pos: int) -> Platform:
        size = (end - start, self._platform_height)
        return Platform(GROUND_IMG_PATH, (start, SCREEN_HEIGHT - self._ground_height - y_pos), size)

    def _create_ground(self) -> pg.sprite.Group:
        grounds = pg.sprite.Group()
        if self._settings['holes']:
            last_x = 0
            for (x_start, x_end) in self._settings['holes']:
                grounds.add(self._create_ground_sprite(last_x, x_start))
                last_x = x_end
            grounds.add(self._create_ground_sprite(last_x, self._world_width))
        else:
            grounds.add(self._create_ground_sprite(0, self._world_width))
        
        return grounds

    def _create_platforms(self) -> pg.sprite.Group:
        platforms = pg.sprite.Group()
        for (x_start, x_end, y_start) in self._settings['platforms']:
            platforms.add(self._create_platform_sprite(x_start, x_end, y_start))
        return platforms

    def compute_collisions(self, sprite: Player) -> Set[CollisionState]:
        colliding_ground = compute_collision_states(sprite, list(self.ground))
        colliding_platforms = compute_collision_states(sprite, list(self.platforms))
        return set(colliding_ground + colliding_platforms)

    def draw(self, screen):
        self.ground.draw(screen)
        self.platforms.draw(screen)
