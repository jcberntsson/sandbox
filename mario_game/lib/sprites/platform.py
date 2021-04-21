from typing import Tuple
import pygame as pg


class Platform(pg.sprite.Sprite):
    """General platform class, initialized using image, position, and size."""

    def __init__(self, img_path: str, start_position: int, size: Tuple[int, int]):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path).convert()
        self.image = pg.transform.scale(self.image, size)
        self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_position
