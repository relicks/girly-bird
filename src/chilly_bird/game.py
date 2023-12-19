from collections.abc import Mapping

import pygame as pg
import pygame.locals as l
from loguru import logger

from chilly_bird.configs import MainConfig
from chilly_bird.states import BaseState


class Background:
    def __init__(self, cfg: MainConfig) -> None:
        self.background = pg.image.load(cfg.main_scene.bg_img).convert()
        self.road_img = pg.image.load(cfg.main_scene.road_texture).convert()


class Game:
    def __init__(
        self,
        screen: pg.Surface,
        states: Mapping[str, BaseState],
        start_state: str,
        cfg: MainConfig,
    ):
        self.running = True
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        # self.state_name = start_state
        self.current_state: BaseState = self.states[start_state]

        self.background = pg.image.load(cfg.main_scene.bg_img).convert()
        self.road_img = pg.image.load(cfg.main_scene.road_texture).convert()

        pg.mixer.music.load(cfg.main_scene.bg_music)
        pg.mixer.music.play(-1)  # Infinite music loop

    def handle_events(self):
        for event in pg.event.get():
            if event.type == l.QUIT:
                logger.info("Close button was pressed")
                self.running = False
            self.current_state.handle_event(event)

    def flip_state(self):
        # current_state = self.state_name
        if (next_state := self.current_state.next_state) is not None:
            self.current_state.done = False

            persistent = self.current_state.on_exit()
            self.current_state = self.states[next_state]
            self.current_state.on_enter(persistent)
        else:
            logger.warning(
                "State {} was attempted to flip, while not specifying next state",
                self.current_state.__class__,
            )

    def update_state(self, dt):
        if self.current_state.done:
            self.flip_state()
        self.current_state.update(dt)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.current_state.draw(self.screen)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps)
            self.handle_events()
            self.update_state(dt)
            self.draw()
            # pg.display.update()
            pg.display.flip()
