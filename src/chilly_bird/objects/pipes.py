"""Contains implementations of game pipe-like obstacles."""

from typing import Any, Literal

import pygame as pg
from loguru import logger
from typing_extensions import override

from chilly_bird.configs import MainConfig
from chilly_bird.types import Coordinate


class Pipe(pg.sprite.Sprite):
    """The generic pipe, but with a little jiggle."""

    def __init__(  # noqa: PLR0913
        self,
        pos: Coordinate,
        direction: Literal["up"] | Literal["down"],
        pipe_gap: int,
        scroll_speed: int,
        cfg: MainConfig,
    ) -> None:
        """Construct a new Pipe object.

        Args:
        ----
            pos: a position to place the pipe at
            direction: where pipe will be pointing
            pipe_gap: a gap between consecutive pipes, in px
            scroll_speed: of pipe, in px/frame
            cfg: main config object

        """
        super().__init__()

        self.image = pg.image.load(cfg.main_scene.pipe_img).convert_alpha()
        self.rect = self.image.get_rect()

        self.pipe_gap = pipe_gap
        self.scroll_speed = scroll_speed

        self.counter = 0
        self.div = 10
        self.step = 1

        x, y = pos
        match direction:
            case "up":
                # ? +35 pixels in order to create a gap
                self.rect.topleft = (round(x), round(y + self.pipe_gap / 2))
            case "down":
                # Flipping not by the x-axis (False), but by the y-axis (True)
                self.image = pg.transform.flip(self.image, flip_x=False, flip_y=True)
                # ? -35 pixels in order to create a gap (70 pixels overall)
                self.rect.bottomleft = (round(x), round(y - self.pipe_gap / 2))
            case _:
                raise ValueError(  # noqa: TRY003
                    "`direction` must be either 'up' or 'down'"
                )

        # if location == 1:  # Pipe pointing up
        # if location == -1:  # Pipe pointing down
        logger.trace("Pipe initialized at ({}, {}), direction={}", x, y, direction)

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:
        # Pipes are scrolled here
        logger.trace("Pipe updating")
        # new_scroll_speed = kwargs.get("scroll_speed")
        if (new_scroll_speed := kwargs.get("scroll_speed")) is not None:
            logger.debug(
                "Pipes scroll speed changed from {} to {}",
                self.scroll_speed,
                new_scroll_speed,
            )
            self.scroll_speed = new_scroll_speed

        if self.scroll_speed == 0:
            return

        self.rect.x -= self.scroll_speed  # Forces pipes to constantly move to the left

        if self.counter >= 0:
            self.rect.y -= self.step
            if self.counter >= self.div:
                self.counter -= 2 * self.div
        else:
            self.rect.y += self.step
        self.counter += self.step

        if self.rect.right < 0:
            logger.trace("Pipe moved out of screen, killing it")
            # As soon as the rightmost point of a pipe disappears
            # from the screen, it is deleted. Otherwise, disappeared
            # pipes remain in the game memory
            self.kill()
