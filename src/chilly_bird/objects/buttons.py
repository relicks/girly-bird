import types
from typing import Any

import pygame as pg

consts = types.SimpleNamespace()

# from loguru import logger

consts.CUSTOM_BUTTON_PRESSED = pg.event.custom_type()


class StartButton(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args: Any, **kwargs: Any) -> None:
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.event.post(
                    pg.event.Event(consts.CUSTOM_BUTTON_PRESSED, {"button": "start"})
                )


class RestartButton(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args: Any, **kwargs: Any) -> None:
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.event.post(
                    pg.event.Event(consts.CUSTOM_BUTTON_PRESSED, {"button": "restart"})
                )


class ReskinButton(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args: Any, **kwargs: Any) -> None:
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.event.post(
                    pg.event.Event(consts.CUSTOM_BUTTON_PRESSED, {"button": "reskin"})
                )
