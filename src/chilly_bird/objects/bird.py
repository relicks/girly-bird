"""Contains an implementation of the main player controller."""

from typing import Any

import pygame as pg
from loguru import logger
from typing_extensions import override

from chilly_bird.configs import MainConfig
from chilly_bird.types import Coordinate


class Bird(pg.sprite.Sprite):
    """Player controller with drawing and game logic."""

    def __init__(self, initial_pos: Coordinate, cfg: MainConfig) -> None:
        """Construct a new Bird object.

        Args:
        ----
            initial_pos: an initial position of the object
            cfg: main configuration object

        """
        super().__init__()
        self.initial_pos = initial_pos
        self.scale = cfg.main_scene.bird_size

        self.images = [  # ? Creates the bird animation frames:
            pg.transform.scale(frame, self.scale)
            for frame in [
                pg.image.load(frame).convert_alpha()
                for frame in cfg.main_scene.bird_aframes
            ]
        ]
        self.initial_images = self.images[:]  # shallow copy

        self.jump_sound = pg.mixer.Sound(cfg.main_scene.bird_jump_sound)
        self.road_y_pos = 384

        # region Setting the starting parameters:
        self.i = 0  # Index of the image in the self.images list
        self.anim_spd = 0  # Speed at which the animation runs
        self.image = self.images[self.i]
        self.rect = self.image.get_rect(center=initial_pos)
        self.gravity = 0.0
        self.clicked = False
        self.flying = False
        self.visible = True
        # endregion

        logger.info(f"{__class__} initialized")

    def reset(self) -> None:
        """Reset the bird state to the starting one."""
        self.i = 0
        self.anim_spd = 0  # Speed at which the animation runs
        self.image = self.images[self.i]
        self.position(self.initial_pos)
        self.gravity = 0.0
        self.clicked = False
        self.flying = False
        self.visible = True

    def position(self, pos: Coordinate | None = None) -> None:
        """Move the bird to the given position `pos`.

        Args:
        ----
            pos: position to move the bird in

        """
        if pos is None:
            pos = self.initial_pos
        self.rect = self.image.get_rect(center=pos)

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401, D102
        logger.trace("Bird updating")
        if self.flying:
            self.fly()

        if self.visible:
            if self.flying:
                # ? Creating the bird's ability to jump
                if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                    logger.trace("Fly key pressed")
                    self.clicked = True
                    self.gravity = -3.5
                    self.jump_sound.play()
                if not pg.mouse.get_pressed()[0] == 1:
                    self.clicked = False

            # ? Flapping animation
            self.anim_spd += 1
            anim_spd_limit = 5  # flapping animation speed
            if self.anim_spd > anim_spd_limit:
                # Otherwise the speed of the wings flapping
                # would be indefinitely increasing
                self.anim_spd = 0
                self.i += 1
                if self.i >= len(self.images):
                    # In order to create an endless loop of animation and
                    # the bird would not stop flapping its wings right after
                    # the first iteration of the list
                    self.i = 0
            # Improving the animation of jumping:
            self.image = pg.transform.rotate(self.images[self.i], self.gravity * -1.25)
        else:
            # Animation of the bird falling:
            self.image = pg.transform.rotate(self.images[self.i], -75)
            self.gravity = 10

    def fly(self) -> None:
        """Process the bird flying movement.

        Creates the force that pulls the bird down (essentially gravity).
        """
        logger.trace("Bird is flying down")
        self.gravity += 0.17
        self.gravity = min(self.gravity, 2.6)
        if self.rect.bottom < self.road_y_pos:
            self.rect.y += int(self.gravity)

    def redress(self) -> None:
        """Change the current bird skin to the original one."""
        self.images = self.initial_images[:]  # shallow copy
