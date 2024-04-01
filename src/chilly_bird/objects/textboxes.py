"""Implementations of `Sprite` based text boxes."""

from typing import Any

import pygame as pg
from typing_extensions import override

from chilly_bird.types import ColorValue, Coordinate


class TextSprite(pg.sprite.Sprite):
    """A sprite for displaying text with Pygame, supporting dynamic text updates."""

    @override
    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        color: ColorValue,
        pos: Coordinate,
    ) -> None:
        """Construct new textbox `Sprite`.

        Args:
        ----
            text: text to display
            font: displayed text's font
            color: font color
            pos: where to draw the text

        """
        super().__init__()
        self.font = font
        self.previous_text: str | None = None
        self.current_text = text
        self.color = color
        self.image = self.font.render(text, True, self.color)  # noqa: FBT003
        self.rect = self.image.get_rect(topleft=pos)

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:
        new_text: str | None = kwargs.get("text")
        if new_text is not None and new_text != self.previous_text:
            self.previous_text = self.current_text
            self.current_text = new_text
            self.image = self.font.render(new_text, True, self.color)  # noqa: FBT003
