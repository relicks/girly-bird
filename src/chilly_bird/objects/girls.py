import pygame as pg

# from loguru import logger


class Girl(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
