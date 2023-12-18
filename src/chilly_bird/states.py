from abc import ABC, abstractmethod
from collections.abc import Mapping

import pygame as pg
import pygame.locals as l
from loguru import logger
from pygame.event import Event
from pygame.sprite import AbstractGroup
from typing_extensions import Self

from chilly_bird.configs import MainConfig
from chilly_bird.objects.bird import Bird
from chilly_bird.objects.textboxes import TextSprite


class BaseState(ABC):
    def __init__(self, cfg: MainConfig | None = None) -> None:
        self.done = False
        self.next_state: Self | None = None
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
    def boot(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        pass

    def persist(self) -> dict[str, pg.sprite.AbstractGroup]:
        return self.groups


class StartScreen(BaseState):
    def __init__(self, cfg: MainConfig | None = None):
        super().__init__(cfg)
        if cfg is None:
            raise ValueError("cfg argument can't be None")
        self.bird = Bird(50, self.screen_rect.height / 2)
        self.font = pg.font.Font(cfg.fonts.text_font, cfg.fonts.text_font_size)
        self.font_color = (235, 221, 190)
        self.texts = [
            TextSprite(
                "    ".join("press left mouse button to start the game".split()),
                font=self.font,
                color=self.font_color,
                pos=(20, 275),
            ),
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
                "bird": pg.sprite.GroupSingle(self.bird),
            }
        )

    def boot(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        return super().boot(passed_groups)

    def handle_event(self, event: Event) -> None:
        if event.type == pg.constants.MOUSEBUTTONDOWN:
            match event.button:
                case 1:  # LMB
                    self.done = True
                case 2:  # MMB
                    logger.trace("MMB pressed")
                    # Stops the music if mouse wheel is pressed with the 1 second delay
                    pg.mixer.music.fadeout(1000)
                case 3:
                    logger.trace("RMB pressed")
                    # Unmutes the music if right mouse button is pressed
                    pg.mixer.music.play(-1)
        # if pg.mouse.get_pressed()[1]:
        #     logger.trace("MMB pressed")
        #     # Stops the music if mouse wheel is pressed with the 1 second delay
        #     pg.mixer.music.fadeout(1000)
        # if pg.mouse.get_pressed()[2]:
        #     logger.trace("RMB pressed")
        #     # Unmutes the music if right mouse button is pressed
        #     pg.mixer.music.play(-1)

    # def persist(self) -> dict[str, pg.sprite.GroupSingle]:
    #     # self.groups["bird"].empty()
    #     return {"bird": self.groups["bird"]}  # type: ignore


class Flying(BaseState):
    def __init__(self, cfg: MainConfig | None = None) -> None:
        super().__init__(cfg)
        if cfg is None:
            raise ValueError("cfg argument can't be None")

    def boot(self, passed_groups: dict[str, AbstractGroup]) -> None:
        self.groups.update(passed_groups)

    def persist(self):
        return self.groups


class GameOver(BaseState):
    def __init__(self, cfg: MainConfig | None = None) -> None:
        super().__init__(cfg)

    def boot(self, passed_groups: Mapping[str, AbstractGroup]) -> None:
        return super().boot(passed_groups)
