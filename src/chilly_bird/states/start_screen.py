"""Contains implemented state of the Flying scene."""

# flake8: noqa: D102
from collections.abc import Mapping

import pygame as pg
from loguru import logger
from pygame.event import Event

from chilly_bird import game, utils
from chilly_bird.configs import MainConfig
from chilly_bird.objects.bird import Bird
from chilly_bird.objects.buttons import Button
from chilly_bird.objects.road import Road
from chilly_bird.objects.textboxes import TextSprite
from chilly_bird.states.base import BaseState


class StartScreen(BaseState):
    """StartScreen scene with UI and instructions."""

    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        """Initialize the StartScreen.

        Raises `ValueError` if `cfg` is not passed.
        """
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")  # noqa: TRY003
        self.cfg = cfg
        self.font = pg.font.Font(cfg.fonts.text_font, cfg.fonts.text_font_size)
        self.font_color = (235, 221, 190)
        self.texts = [
            TextSprite(
                "    ".join("press start to start the game".split()),
                font=self.font,
                color=self.font_color,
                pos=(75, 300),
            ),
            TextSprite(
                "    ".join("press skin to change the skin of the bird".split()),
                font=self.font,
                color=self.font_color,
                pos=(21, 320),
            ),
            TextSprite(
                "    ".join("close the editor window to exit the skin".split()),
                font=self.font,
                color=self.font_color,
                pos=(22, 353),
            ),
            TextSprite(
                "    ".join("editor and save your progress".split()),
                font=self.font,
                color=self.font_color,
                pos=(75, 365),
            ),
        ]
        self.groups.update(
            {
                "text": pg.sprite.Group(*self.texts),
                "bird": pg.sprite.GroupSingle(
                    Bird(50, self.screen_rect.height / 2, cfg)
                ),
                "road": pg.sprite.GroupSingle(Road(cfg)),
                "buttons": pg.sprite.Group(
                    Button(
                        x=self.screen_rect.width // 2 - 40,
                        y=self.screen_rect.height // 2 + 25,
                        image=pg.image.load(
                            cfg.main_scene.start_button_img
                        ).convert_alpha(),
                        button_event_name="start",
                    ),
                    Button(
                        x=self.screen_rect.width // 2 - 40,
                        y=self.screen_rect.height - 40,
                        image=pg.image.load(
                            cfg.main_scene.reskin_button_img
                        ).convert_alpha(),
                        button_event_name="reskin",
                    ),
                    Button(
                        x=self.screen_rect.width // 4 - 40,
                        y=self.screen_rect.height - 40,
                        image=pg.image.load(
                            cfg.main_scene.redress_button_img
                        ).convert_alpha(),
                        button_event_name="redress",
                    ),
                    Button(
                        x=self.screen_rect.topright[0] - (26 + 10),
                        y=self.screen_rect.topright[1] + 10,
                        image=pg.image.load(
                            cfg.main_scene.music_button_img
                        ).convert_alpha(),
                        button_event_name="toggle_music",
                    ),
                ),
            }
        )

    def on_enter(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        super().on_enter(passed_groups)

    def handle_event(self, event: Event) -> None:
        match event.type:
            case game.EventTypes.CUSTOM_BUTTON_PRESSED:
                match event.button:
                    case "start":
                        self.done = True
                    case "reskin":
                        logger.info("Reskin button pressed")
                        self.reskin_bird()
                    case "redress":
                        logger.info("Redress button pressed")
                        self.groups["bird"].sprites()[0].redress()
                    case "toggle_music":
                        logger.info(f"toggle_music button pressed: {event.dict}")
                        pg.event.post(pg.event.Event(game.EventTypes.TOGGLE_MUSIC))
            case pg.constants.MOUSEBUTTONDOWN:
                if event.button == 1:  # ? LMB
                    for button in self.groups["buttons"]:
                        button.update(event=event)
            case _:
                pass

    def reskin_bird(self) -> None:
        bird: Bird = self.groups["bird"].sprites()[0]
        if new_image := utils.open_editor(self.cfg.main_scene.bird_size):
            bird.images = [new_image] * 3
