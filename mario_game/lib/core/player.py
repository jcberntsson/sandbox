from typing import Tuple

import pygame as pg
from lib.utilities.constants import (
    STEP_SIZE, PLAYER_HEIGHT, PLAYER_WIDTH,
    PLAYER_IMG_PATH
)


class Player(pg.sprite.Sprite):
    """Player class with spawn point init."""

    def __init__(self, spawn_x: int, spawn_y: int):
        pg.sprite.Sprite.__init__(self)
        self._spawn_x = spawn_x
        self._spawn_y = spawn_y
        self.image = self._create_player_image()
        self.rect = self.image.get_rect()
        self._looking_right = True
        self.reset_position()

    @staticmethod
    def _create_player_image():
        image = pg.image.load(PLAYER_IMG_PATH).convert()
        image = pg.transform.scale(image, (PLAYER_HEIGHT, PLAYER_WIDTH))
        image.convert_alpha()
        image.set_colorkey((0, 0, 0))
        return image

    def reset_position(self):
        self.rect.x = self._spawn_x
        self.rect.y = self._spawn_y

    def get_position(self) -> Tuple[int, int]:
        return (self.rect.x, self.rect.y)

    def go_down(self):
        self.rect.y += STEP_SIZE

    def go_up(self):
        self.rect.y -= STEP_SIZE * 2

    def go_left(self):
        self.rect.x -= STEP_SIZE

        if self._looking_right:
            self._looking_right = False
            self.image = pg.transform.flip(self.image, True, False)

    def go_right(self):
        self.rect.x += STEP_SIZE

        if not self._looking_right:
            self._looking_right = True
            self.image = pg.transform.flip(self.image, True, False)
