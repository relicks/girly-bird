from time import perf_counter_ns
from typing import Any

import pygame as pg

from chilly_bird import game


class Button(pg.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        image: pg.Surface,
        button_event_name: str,
        press_delay_ms: int = 500,
    ):
        super().__init__()
        self.image: pg.Surface = image
        self.rect: pg.Rect = self.image.get_rect(topleft=(x, y))
        self.button_event_name = button_event_name
        self.was_pressed_on_ns = perf_counter_ns()
        self.press_delay_ns = press_delay_ms * 10**6

    def update(self, *args: Any, **kwargs: Any) -> None:
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and (
                (perf_counter_ns() - self.was_pressed_on_ns) > self.press_delay_ns
            ):
                self.was_pressed_on_ns = perf_counter_ns()
                pg.event.post(
                    pg.event.Event(
                        game.EventTypes.CUSTOM_BUTTON_PRESSED,
                        {"button": self.button_event_name},
                    )
                )
