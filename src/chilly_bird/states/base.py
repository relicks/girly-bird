from abc import ABC, abstractmethod
from collections.abc import Mapping

import pygame as pg

from chilly_bird.configs import MainConfig


class BaseState(ABC):
    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        self.done = False
        self.next_state = next_state
        self.screen_rect = pg.display.get_surface().get_rect()
        self.groups: dict[str, pg.sprite.AbstractGroup] = {}

    def handle_event(self, event: pg.event.Event) -> None:
        return None

    def update(self, dt: int) -> None:
        for group in self.groups.values():
            group.update()

    def draw(self, surface: pg.Surface) -> None:
        for group in self.groups.values():
            group.draw(surface)

    @abstractmethod
    def on_enter(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        pass

    def on_exit(self) -> dict[str, pg.sprite.AbstractGroup]:
        return self.groups
