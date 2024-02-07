import pygame as pg

from chilly_bird.configs import MainConfig
from chilly_bird.states.base import BaseState


class SpriteEditor(BaseState):
    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")
        self.groups.update({})
