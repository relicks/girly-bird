from typing import Any

import pygame as pg
from loguru import logger

from chilly_bird.configs import MainConfig


class Bird(pg.sprite.Sprite):
    def __init__(self, x, y, cfg: MainConfig):
        super().__init__()
        # ? Creates the bird animation frames:
        animation_frames = [
            pg.image.load(frame).convert_alpha()
            for frame in cfg.main_scene.bird_aframes
        ]
        self.scale = cfg.main_scene.bird_size
        self.images = [
            pg.transform.scale(frame, self.scale) for frame in animation_frames
        ]
        self.initial_images = self.images[:]  # shallow copy
        self.jump_sound = pg.mixer.Sound(cfg.main_scene.bird_jump_sound)
        self.road_y_pos = 384
        self.initial_pos = (x, y)

        self.reset()

        logger.info("Bird initialized")

    def reset(self):
        self.i = 0  # Index of the image in the self.images list
        self.anim_spd = 0  # Speed at which the animation runs
        self.image = self.images[self.i]
        self.position(self.initial_pos)
        self.gravity = 0
        self.clicked = False
        self.flying = False
        self.visible = True

    def position(self, pos: tuple[int, int] | None = None):
        if pos is None:
            pos = self.initial_pos
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
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
            # Animaton of the bird falling:
            self.image = pg.transform.rotate(self.images[self.i], -75)
            self.gravity = 10

    def fly(self) -> None:
        logger.trace("Bird is flying down")
        # Creating the force that constantly pulls
        # the bird down (essentially gravity)
        self.gravity += 0.17
        self.gravity = min(self.gravity, 2.6)
        if self.rect.bottom < self.road_y_pos:
            self.rect.y += int(self.gravity)

    def redress(self):
        self.images = self.initial_images[:]  # shallow copy
