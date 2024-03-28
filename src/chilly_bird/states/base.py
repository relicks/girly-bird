"""Contains (abstract) base classes pertaining to states."""

from abc import ABC, abstractmethod
from collections.abc import Mapping

import pygame as pg

from chilly_bird.configs import MainConfig


class BaseState(ABC):
    """Abstract base state designed for use with the state machine."""

    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        """Initialize the base.

        Args:
        ----
            cfg: the configuration object to use
            next_state: the state to transition to

        """
        self.done = False
        self.next_state = next_state
        self.screen_rect = pg.display.get_surface().get_rect()
        self.groups: dict[str, pg.sprite.AbstractGroup] = {}

    def handle_event(self, event: pg.event.Event) -> None:
        """Event handling happens here.

        Args:
        ----
            event: passed from state machine

        """
        return None

    def update(self, dt: int) -> None:
        """State internal (Groups) are updated here.

        Args:
        ----
            dt: time elapsed since last frame

        """
        for group in self.groups.values():
            group.update()

    def draw(self, surface: pg.Surface) -> None:
        """Draw the objects belonging to this state.

        Args:
        ----
            surface: to draw onto

        """
        for group in self.groups.values():
            group.draw(surface)

    @abstractmethod
    def on_enter(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        """Entrance hook designed for handling the Groups from the previous state.

        Args:
        ----
            passed_groups: from the previous state

        """
        pass

    def on_exit(self) -> dict[str, pg.sprite.AbstractGroup]:
        """Exit hook designed for passing the Groups to the next state.

        Returns
        -------
            Groups of the current state

        """
        return self.groups
