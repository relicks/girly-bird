from collections.abc import Mapping

import pygame as pg
import pygame.locals as l
from loguru import logger

from chilly_bird.configs import MainConfig
from chilly_bird.states import Flying
from chilly_bird.states.base import BaseState


class EventTypes:
    CUSTOM_BUTTON_PRESSED = pg.event.custom_type()
    TOGGLE_MUSIC = pg.event.custom_type()


class Game:
    def __init__(
        self,
        screen: pg.Surface,
        states: Mapping[str, BaseState],
        start_state: str,
        cfg: MainConfig,
    ):
        self.running = True
        self.screen: pg.Surface = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.current_state: BaseState = self.states[start_state]

        self.background: pg.Surface = pg.image.load(cfg.main_scene.bg_img).convert()
        self.road_img: pg.Surface = pg.image.load(cfg.main_scene.road_texture).convert()

        self.music_plays = True
        pg.mixer.music.load(cfg.main_scene.bg_music)
        pg.mixer.music.play(-1)  # Infinite music loop

    def global_event_handler(self, event: pg.event.Event) -> None:
        match event.type:
            case l.QUIT:
                logger.info("Close button was pressed")
                self.running = False

            case pg.constants.MOUSEBUTTONDOWN:
                match event.button:
                    case 2:  # ? MMB
                        logger.trace("MMB pressed")
                        # Stops the music if mouse wheel is pressed
                        # with 1 second delay
                        self.toggle_music(False)
                    case 3:  # ? RMB
                        logger.trace("RMB pressed")
                        # Unmutes the music if right mouse button is pressed
                        self.toggle_music(True)

            case EventTypes.TOGGLE_MUSIC:
                self.toggle_music(not self.music_plays)

    def toggle_music(self, enabled: bool) -> bool:
        if enabled:
            pg.mixer.music.play(-1)
            self.music_plays = True
            return True
        pg.mixer.music.fadeout(500)
        self.music_plays = False
        return False

    def handle_events(self) -> None:
        for event in pg.event.get():
            self.global_event_handler(event)
            self.current_state.handle_event(event)

    def flip_state(self) -> None:
        # current_state = self.state_name
        if (next_state := self.current_state.next_state) is not None:
            logger.info(
                "Flipping from `{}` to `{}` state",
                self.current_state.__class__,
                next_state,
            )
            self.current_state.done = False

            persistent = self.current_state.on_exit()
            logger.debug("Passing groups `{}` to `{}` state", persistent, next_state)
            self.current_state = self.states[next_state]
            self.current_state.on_enter(persistent)
        else:
            logger.critical(
                "State {} was attempted to flip, while not specifying next state",
                self.current_state.__class__,
            )

    def update_state(self, dt: int) -> None:
        if self.current_state.done:
            self.flip_state()
        self.current_state.update(dt)

    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.current_state.draw(self.screen)

        # road scrolling ugly fix 🤦‍♀️🐈🐈‍⬛
        if isinstance(self.current_state, Flying):
            self.screen.blit(self.road_img, (self.current_state.road_scroll, 384))

    def run(self) -> None:
        while self.running:
            dt: int = self.clock.tick(self.fps)
            self.handle_events()
            self.update_state(dt)
            self.draw()
            # pg.display.update()
            pg.display.flip()
