from abc import ABC, abstractmethod

import pygame as pg


class BaseState(ABC):
    def __init__(self):
        self.done = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.cache = {}

    @abstractmethod
    def handle_event(self, event: pg.event.Event):
        pass

    @abstractmethod
    def update(self, dt: int):
        pass

    @abstractmethod
    def draw(self, surface: pg.Surface):
        pass


class StartScreen(BaseState):
    def __init__(self):
        super().__init__()
