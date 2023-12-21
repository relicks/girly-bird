from collections.abc import Mapping

import pygame as pg
from loguru import logger
from pygame.event import Event

from chilly_bird import utils
from chilly_bird.configs import MainConfig
from chilly_bird.objects.bird import Bird
from chilly_bird.objects.buttons import (
    RedressButton,
    ReskinButton,
    StartButton,
    consts,
)
from chilly_bird.objects.road import Road
from chilly_bird.objects.textboxes import TextSprite
from chilly_bird.states.base import BaseState


class StartScreen(BaseState):
    def __init__(self, cfg: MainConfig | None = None, next_state: str | None = None):
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")
        self.cfg = cfg
        self.font = pg.font.Font(cfg.fonts.text_font, cfg.fonts.text_font_size)
        self.font_color = (235, 221, 190)
        self.texts = [
            TextSprite(
                "    ".join("press mouse wheel to mute the music".split()),
                font=self.font,
                color=self.font_color,
                pos=(45, 290),
            ),
            TextSprite(
                "    ".join("press right mouse button to unmute the music".split()),
                font=self.font,
                color=self.font_color,
                pos=(5, 305),
            ),
        ]
        self.groups.update(
            {
                "text": pg.sprite.Group(*self.texts),
                "bird": pg.sprite.GroupSingle(
                    Bird(50, self.screen_rect.height / 2, cfg)
                ),
                "road": pg.sprite.GroupSingle(Road(cfg)),
                "start_button": pg.sprite.GroupSingle(
                    StartButton(
                        x=self.screen_rect.width // 2 - 40,
                        y=self.screen_rect.height // 2 + 25,
                        image=pg.image.load(
                            cfg.main_scene.start_button_img
                        ).convert_alpha(),
                    )
                ),
                "reskin_button": pg.sprite.GroupSingle(
                    ReskinButton(
                        x=self.screen_rect.width // 2 - 40,
                        y=self.screen_rect.height - 40,
                        image=pg.image.load(
                            cfg.main_scene.reskin_button_img
                        ).convert_alpha(),
                    )
                ),
                "redress_button": pg.sprite.GroupSingle(
                    RedressButton(
                        x=self.screen_rect.width // 4 - 40,
                        y=self.screen_rect.height - 40,
                        image=pg.image.load(
                            cfg.main_scene.redress_button_img
                        ).convert_alpha(),
                    )
                ),
            }
        )

    def on_enter(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        return super().on_enter(passed_groups)

    def handle_event(self, event: Event) -> None:
        match event.type:
            case consts.CUSTOM_BUTTON_PRESSED:
                match event.button:
                    case "start":
                        self.done = True
                    case "reskin":
                        logger.info("Reskin button pressed")
                        self.reskin_bird()
                    case "redress":
                        logger.info("Redress button pressed")
                        self.groups["bird"].sprites()[0].redress()
            case _:
                pass

    def reskin_bird(self):
        bird: Bird = self.groups["bird"].sprites()[0]
        if new_image := utils.open_image(self.cfg.main_scene.bird_size):
            bird.images = [new_image] * 3
