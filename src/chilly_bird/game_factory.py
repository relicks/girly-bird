"""Contains game app initialization logic."""

import sys
from dataclasses import dataclass
from typing import NoReturn

import pygame as pg
from loguru import logger

from chilly_bird.configs import MainConfig, load_config
from chilly_bird.game import Game
from chilly_bird.logging import configure_logger
from chilly_bird.states import Flying, GameOver, StartScreen


@dataclass
class MainScene:
    """Represents all the states employed in the game."""

    start_screen: StartScreen
    flying: Flying
    game_over: GameOver


class GameFactory:
    """Constructs the instance of the `Game` class, supports with-statement."""

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize the game state, window and logs."""

        # Loading game config
        default_config_path = "./conf/config.yaml"
        self.cfg: MainConfig = load_config(config_path or default_config_path)

        # Initializing Pygame window
        pg.init()
        pg.mixer.init()
        self.screen: pg.Surface = pg.display.set_mode(
            (self.cfg.window.screen_width, self.cfg.window.screen_height)
        )
        pg.display.set_caption(self.cfg.window.caption)
        pg.display.set_icon(pg.image.load(self.cfg.window.icon_path))

        # Creating game states for State Machine
        self.main_scene = MainScene(
            StartScreen(self.cfg, "Flying"),
            Flying(self.cfg, "GameOver"),
            GameOver(self.cfg, "Start"),
        )

        # Logger's stuff
        configure_logger(logger, print_stdout=True)

        # Creating game core object
        self.game: Game = Game(
            screen=self.screen,
            states={
                "Start": self.main_scene.start_screen,
                "Flying": self.main_scene.flying,
                "GameOver": self.main_scene.game_over,
            },
            start_state="Start",
            cfg=self.cfg,
        )

    def __enter__(self) -> Game:
        """Return the instance of the created `Game`."""
        return self.game

    def __exit__(self, *exc_details) -> NoReturn:  # noqa: ANN002
        """Shut down the `Game` app."""
        pg.quit()
        sys.exit()
