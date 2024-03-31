"""Contains game over scene reproachful characters."""

import pygame as pg
from loguru import logger
from typing_extensions import override

from chilly_bird.types import Coordinate


class Girl(pg.sprite.Sprite):
    """Sad girl."""

    @override
    def __init__(self, pos: Coordinate, image: pg.Surface) -> None:
        """Create new Girl Sprite.

        Args:
        ----
            pos: a position to place the sprite at
            image: sprite image

        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

        logger.info(f"{self.__class__} initialized")
