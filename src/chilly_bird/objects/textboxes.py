from typing import TypeAlias

import pygame as pg

ColorValue: TypeAlias = pg.color.Color | int | str | tuple[int, int, int]


class TextSprite(pg.sprite.Sprite):
    def __init__(
        self, text: str, font: pg.font.Font, color: ColorValue, pos: tuple[int, int]
    ):
        super().__init__()
        self.font = font
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(topleft=pos)
