import types
from typing import Any

import pygame as pg

consts = types.SimpleNamespace()

# from loguru import logger

consts.CUSTOM_BUTTON_PRESSED = pg.event.custom_type()


class BaseButton(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface, button_event_name: str):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.button_event_name = button_event_name

    def update(self, *args: Any, **kwargs: Any) -> None:
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.event.post(
                    pg.event.Event(
                        consts.CUSTOM_BUTTON_PRESSED,
                        {"button": self.button_event_name},
                    )
                )
