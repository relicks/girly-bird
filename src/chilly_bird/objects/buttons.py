"""Contains UI buttons."""

from time import perf_counter_ns
from typing import Any

import pygame as pg
from typing_extensions import override

from chilly_bird import game
from chilly_bird.types import Coordinate


class Button(pg.sprite.Sprite):
    """A simple button that employs pygame's direct mouse access.

    Publishes the `CUSTOM_BUTTON_PRESSED` click event on the pygame's event queue.
    """

    def __init__(
        self,
        pos: Coordinate,
        image: pg.Surface,
        button_event_name: str,
        press_delay_ms: int = 500,
    ) -> None:
        """Create a UI clickable button at the `pos` that sends click events.

        Args:
        ----
            pos: a position to place the button at
            image: Pygame Surface that will be the body of the button
            button_event_name: name of the button attribute of the created event
            press_delay_ms: the button won't send signals more often than that delay

        """
        super().__init__()
        self.image: pg.Surface = image
        self.rect: pg.Rect = self.image.get_rect(topleft=pos)
        self.button_event_name = button_event_name
        self.was_pressed_on_ns = perf_counter_ns()
        self.press_delay_ns = press_delay_ms * 10**6

    @override
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
