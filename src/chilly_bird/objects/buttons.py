from typing import Any

import pygame as pg

# from loguru import logger

BUTTON_PRESSED = pg.event.custom_type()


class RestartButton(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pg.Surface):
        # logger.trace("Drawing restart button")
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True
        surface.blit(self.image, self.rect)
        return action

    def update(self, *args: Any, **kwargs: Any) -> None:
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.event.post(pg.event.Event(BUTTON_PRESSED, {"button": "restart"}))
