import pygame as pg
from loguru import logger

from chilly_bird.configs import MainConfig


class Road(pg.sprite.Sprite):
    def __init__(self, cfg: MainConfig) -> None:
        super().__init__()
        logger.info("{} initialized", self.__class__)
        self.image = pg.image.load(cfg.main_scene.road_texture).convert()
        self.y_pos = 384
        self.initial_scroll = 0
        self.rect = self.image.get_rect(topleft=(0, self.y_pos))
