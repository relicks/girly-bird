"""Contains game over scene reproachful characters."""

import pygame as pg
from loguru import logger

from chilly_bird.types import Coordinate


class Girl(pg.sprite.Sprite):
    """Sad girl."""

    def __init__(self, pos: Coordinate, image: pg.Surface) -> None:
        """Create new girl object.

        Args:
        ----
            pos: a position to place the sprite at
            image: sprite image

        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

        logger.info(f"{__class__} initialized")
