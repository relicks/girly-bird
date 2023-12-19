import pygame as pg
from loguru import logger


class Pipe(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, location: int, pipe_gap: int, scroll_speed: int):
        super().__init__()

        self.image = pg.image.load("game_files/pipe.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.pipe_gap = pipe_gap
        self.scroll_speed = scroll_speed

        self.counter = 0
        self.div = 10
        self.step = 1

        if location == 1:  # Pipe pointing up
            # ? +35 pixels in order to create a gap
            self.rect.topleft = (x, round(y + self.pipe_gap / 2))
        if location == -1:  # Pipe pointing down
            # Fliping not by the x-axis (False), but by the y-axis (True)
            self.image = pg.transform.flip(self.image, False, True)
            # ? -35 pixels in order to create a gap (70 pixels overall)
            self.rect.bottomleft = (x, round(y - self.pipe_gap / 2))
        logger.trace("Pipe initialized at ({}, {}), loc={}", x, y, location)

    def update(self):
        logger.trace("Pipe updating")
        self.rect.x -= self.scroll_speed  # Forces pipes to constantly move to the left

        if self.counter >= 0:
            self.rect.y -= self.step
            if self.counter >= self.div:
                self.counter -= 2 * self.div
        else:
            self.rect.y += self.step
        self.counter += self.step

        if self.rect.right < 0:
            logger.trace("Pipe moved out of screen, killing it")
            # As soon as the rightmost point of a pipe disappears
            # from the screen, it is deleted. Otherwise disappeared
            # pipes remain in the game memory
            self.kill()
