from typing import Any, TypeAlias

import pygame as pg

ColorValue: TypeAlias = pg.color.Color | int | str | tuple[int, int, int]


class TextSprite(pg.sprite.Sprite):
    def __init__(
        self,
        initial_text: str,
        font: pg.font.Font,
        color: ColorValue,
        pos: tuple[int, int],
    ):
        super().__init__()
        self.font = font
        self.initial_text = initial_text
        self.color = color
        self.image = self.font.render(self.initial_text, True, self.color)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        new_text = kwargs.get("text")
        if new_text is not None and new_text != self.initial_text:
            self.image = self.font.render(new_text, True, self.color)
