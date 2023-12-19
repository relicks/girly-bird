import sys

import pygame as pg
from loguru import logger

from chilly_bird.configs import load_config
from chilly_bird.game import Game
from chilly_bird.logging import configure_logger
from chilly_bird.states import Flying, GameOver, StartScreen

pg.init()
screen = pg.display.set_mode((432, 468))
cfg = load_config()
configure_logger(logger, print_stdout=True)
states = {
    "Start": StartScreen(cfg, "Flying"),
    "Flying": Flying(cfg, "GameOver"),
    "GameOver": GameOver(cfg, "Start"),
}

game = Game(screen, states, "Start", cfg)
game.run()

pg.quit()
sys.exit()
