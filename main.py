import sys

import pygame as pg

from chilly_bird.configs import load_config
from chilly_bird.game import Game
from chilly_bird.states import Flying, GameOver, StartScreen

pg.init()
screen = pg.display.set_mode((432, 468))
cfg = load_config()
states = {"Start": StartScreen(cfg), "Flying": Flying(cfg), "GameOver": GameOver(cfg)}

game = Game(screen, states, "Start")
game.run()

pg.quit()
sys.exit()
