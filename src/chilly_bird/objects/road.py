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

    # def update(self, *args: Any, **kwargs: Any) -> None:
    #     new_scroll = kwargs.get("road_scroll")
    #     if new_scroll is not None and new_scroll != self.initial_scroll:
    #         self.rect.move_ip(x=kwargs["road_scroll"], y=self.y_pos)
