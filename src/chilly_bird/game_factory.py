import sys

import pygame as pg
from loguru import logger

from chilly_bird.configs import MainConfig, load_config
from chilly_bird.game import Game
from chilly_bird.logging import configure_logger
from chilly_bird.states import Flying, GameOver, StartScreen
from chilly_bird.states.base import BaseState


class GameFactory:
    def __init__(self, config_path: str | None = None) -> None:
        # Loading game config
        default_config_path = "./conf/config.yaml"
        self.cfg: MainConfig = load_config(config_path or default_config_path)

        # Initializing Pygame window
        pg.init()
        self.screen: pg.Surface = pg.display.set_mode((432, 468))
        pg.display.set_caption(self.cfg.window.caption)
        pg.display.set_icon(pg.image.load(self.cfg.window.icon_path))

        # Creating game states for State Machine
        self.states: dict[str, BaseState] = {
            "Start": StartScreen(self.cfg, "Flying"),
            "Flying": Flying(self.cfg, "GameOver"),
            "GameOver": GameOver(self.cfg, "Start"),
        }

        # Logger's stuff
        configure_logger(logger, print_stdout=True)

    def __enter__(self):
        # Creating game core object
        return Game(self.screen, self.states, "Start", self.cfg)

    def __exit__(self, *exc_details):
        pg.quit()
        sys.exit()
