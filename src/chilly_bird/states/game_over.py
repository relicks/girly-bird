"""Contains implemented state of the GameOver scene."""

from collections.abc import Mapping

import pygame as pg
from pygame.event import Event
from pygame.sprite import AbstractGroup
from typing_extensions import override

from chilly_bird import game
from chilly_bird.configs import MainConfig
from chilly_bird.objects.buttons import Button
from chilly_bird.objects.girls import Girl
from chilly_bird.states.base import BaseState


class GameOver(BaseState):
    """GameOver scene."""

    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        """Initialize the GameOver.

        Raises `ValueError` if `cfg` is not passed.
        """
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")  # noqa: TRY003

        self.groups.update(
            {
                "girl": pg.sprite.GroupSingle(
                    Girl(
                        pos=(120, 240),
                        image=pg.image.load(
                            cfg.main_scene.disappointed_girl_img
                        ).convert_alpha(),
                    )
                ),
                "restart_button": pg.sprite.GroupSingle(
                    Button(
                        pos=(
                            self.screen_rect.width // 2 - 40,
                            self.screen_rect.height // 2 - 80,
                        ),
                        image=pg.image.load(
                            cfg.main_scene.restart_button_img
                        ).convert_alpha(),
                        button_event_name="restart",
                    )
                ),
            }
        )

    @override
    def on_enter(self, passed_groups: Mapping[str, AbstractGroup]) -> None:
        carry_over = ["bird", "pipes", "road", "score"]
        for group_name in carry_over:
            self.groups[group_name] = passed_groups[group_name]
        self.groups["pipes"].update(scroll_speed=0)

        # ? swapping girl sprite to the end, so it would be drawn on the front
        girl = self.groups["girl"]
        del self.groups["girl"]
        self.groups["girl"] = girl

        restart_button = self.groups["restart_button"]
        del self.groups["restart_button"]
        self.groups["restart_button"] = restart_button

    @override
    def on_exit(self) -> dict[str, AbstractGroup]:
        self.groups["bird"].sprites()[0].reset()
        self.groups["pipes"].empty()
        return super().on_exit()

    @override
    def handle_event(self, event: Event) -> None:
        if (
            event.type == game.EventTypes.CUSTOM_BUTTON_PRESSED
            and event.button == "restart"
        ):
            self.done = True
