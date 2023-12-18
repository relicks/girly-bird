# flake8: noqa: PLR0912, PLR0913, PLR2004

import random

import pygame as pg
import pygame.locals as l
from loguru import logger
from pygame import mixer

from .bird import Bird
from .pipes import Pipe


class RestartButton:
    def __init__(self, x: int, y: int, image: pg.Surface):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pg.Surface):
        logger.trace("Drawing restart button")
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True
        surface.blit(self.image, self.rect)
        return action


class Girl:
    def __init__(self, x: int, y: int, image: pg.Surface):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pg.Surface):
        logger.trace("Drawing Girl")
        surface.blit(self.image, self.rect)


class GameState:
    def __init__(self) -> None:
        raise NotImplementedError


class Game:
    def __init__(self, screen_width, screen_height) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.running = False
        self.fps = 60

        pg.init()
        self.clock = pg.time.Clock()
        self.display: pg.Surface = pg.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        # ? Window properties:
        pg.display.set_caption("Chilly Bird")
        pg.display.set_icon(pg.image.load("game_files/game.icon.png"))

        # ? Fonts:
        self.font_color = (235, 221, 190)
        self.font1 = pg.font.Font(
            "game_files/arcadeclassic.ttf", 30
        )  # For displaying the score
        self.font2 = pg.font.Font(
            "game_files/arcadeclassic.ttf", 18
        )  # For instructing a player

        # ? Loading images
        # convert() enables faster blitting -> improves performance
        self.background = pg.image.load("game_files/background_2.png").convert()

        self.road_img = pg.image.load("game_files/road.png").convert()
        self.restart_button_img = pg.image.load(
            "game_files/restart.button.png"
        ).convert()
        self.disappointed_girl_img = pg.image.load(
            "game_files/disappointed.girl_2.png"
        ).convert_alpha()  # transparent background

        # ? Init params
        self.score = 0
        self.game_is_over = False
        self.road_scroll = 0
        self.within_pipe = False

        self.scroll_speed = 2
        self.pipe_freq = 1250  # New pipes appear every 1.25 seconds
        self.gap_btw_pipes = 100

        # ? Creating Game objects
        self.button = RestartButton(
            self.screen_width / 2 - 40,
            self.screen_height / 2 - 80,
            self.restart_button_img,
        )
        self.girl = Girl(140, 200, self.disappointed_girl_img)

        # First pipe appears right when the game starts
        # (i.e. without a 1.25 seconds delay unlike the subsequent ones)
        self.pipe_group: pg.sprite.Group = pg.sprite.Group()
        self.leftmost_pipe = pg.time.get_ticks() - self.pipe_freq

        self.bird = Bird(50, self.screen_height / 2)
        self.bird_group = pg.sprite.GroupSingle()
        self.bird_group.add(self.bird)

        logger.info("Game instance initialized")

        # ? Start music
        mixer.music.load("game_files/game.music.mp3")
        pg.mixer.music.play(-1)  # Infinite music loop

    def draw_text(self, text: str, font: pg.font.Font, text_col, x, y):
        """Instructs a player and displays score."""
        image = font.render(text, True, text_col)
        self.display.blit(image, (x, y))

    def reset_game(self):
        """Resets everything to its pre-launched position."""
        logger.info("Restarting game")
        self.pipe_group.empty()
        self.bird.rect.x = 50
        self.bird.rect.y = round(self.screen_height / 2)
        self.score = 0

    def process_input(self):
        logger.trace("Processing input")
        if pg.mouse.get_pressed()[1]:
            logger.trace("MMB pressed")
            # Stops the music if mouse wheel is pressed with the 1 second delay
            pg.mixer.music.fadeout(1000)
        if pg.mouse.get_pressed()[2]:
            logger.trace("RMB pressed")
            # Unmutes the music if right mouse button is pressed
            pg.mixer.music.play(-1)

        for event in pg.event.get():
            if event.type == l.QUIT:
                logger.info("Close button was pressed")
                self.running = False

            if (
                event.type == pg.MOUSEBUTTONDOWN
                and not self.bird.flying
                and not self.game_is_over
            ):
                logger.trace("MOUSEBUTTONDOWN, bird should fly")
                self.bird.flying = True

    def update_state(self):
        raise NotImplementedError

    def render(self):
        if self.bird.flying is False and self.game_is_over is False:
            logger.trace("Showing start screen")
            self.draw_text(
                "    ".join("press left mouse button to start the game".split()),
                self.font2,
                self.font_color,
                20,
                275,
            )
            self.draw_text(
                "    ".join("press mouse wheel to mute the music".split()),
                self.font2,
                self.font_color,
                45,
                290,
            )
            self.draw_text(
                "    ".join("press right mouse button to unmute the music".split()),
                self.font2,
                self.font_color,
                5,
                305,
            )

        self.bird_group.draw(self.display)
        self.bird_group.update()
        self.pipe_group.draw(self.display)
        self.display.blit(self.road_img, (self.road_scroll, 384))

        # Counting player's score
        if len(self.pipe_group) > 0:  # Some pipes had been created
            if (
                self.bird_group.sprites()[0].rect.left
                > self.pipe_group.sprites()[
                    0
                ].rect.left  # The leftmost point of the bird has passed
                # the leftmost point of a pipe
                and self.bird_group.sprites()[0].rect.right
                < self.pipe_group.sprites()[
                    0
                ].rect.right  # But the bird's rightmost point has not passed
                # the rightmost point of the pipe
                and not self.within_pipe
            ):
                # The bird is within the range of the leftmost
                # and rightmost points of the pipe
                self.within_pipe = True

            if self.within_pipe:
                logger.debug("Bird within pipe")
                if (
                    self.bird_group.sprites()[0].rect.left
                    > self.pipe_group.sprites()[0].rect.right
                ):
                    # And only if the bird's leftmost point passes the
                    # rightmost point of a pipe, one point is added to the score
                    self.score += 1

                    # The bird is not within the range of the extreme
                    # points of a particular pipe
                    self.within_pipe = False

        self.draw_text(
            str(self.score), self.font1, self.font_color, self.screen_width / 2, 12
        )

        # ? Collision handling
        # bird_collided_pipe = pg.sprite.groupcollide(
        #     self.bird_group, self.pipe_group, False, False
        # )
        bird_collided_pipe = pg.sprite.spritecollideany(self.bird, self.pipe_group)
        bird_touched_screen_top = self.bird.rect.top < 0
        if bird_collided_pipe or bird_touched_screen_top:
            self.game_is_over = True

        if self.bird.rect.bottom >= 384:
            self.game_is_over = True
            self.bird.flying = False

        if not self.game_is_over and self.bird.flying:
            logger.trace("Generating new pipes")
            current_time = pg.time.get_ticks()

            # Enough time has passed -> creating new pipes:
            if current_time - self.leftmost_pipe > self.pipe_freq:
                # Pipes are randomly generated within the range of 100 pixels:
                pipe_distance = random.randint(-50, 50)
                pipe_down = Pipe(
                    self.screen_width,
                    round(self.screen_height / 2 + pipe_distance),
                    1,
                    self.gap_btw_pipes,
                    self.scroll_speed,
                )
                pipe_up = Pipe(
                    self.screen_width,
                    round(self.screen_height / 2 + pipe_distance),
                    -1,
                    self.gap_btw_pipes,
                    self.scroll_speed,
                )
                self.pipe_group.add(pipe_down)
                self.pipe_group.add(pipe_up)
                self.leftmost_pipe = current_time

            # Making the road scroll:
            self.road_scroll -= self.scroll_speed
            if abs(self.road_scroll) > 17:
                self.road_scroll = 0
            self.pipe_group.update()

        if self.game_is_over:
            self.bird.hidden(True)
            self.girl.draw(self.display)
            if self.button.draw(self.display):
                self.game_is_over = False
                self.reset_game()

        for event in pg.event.get():
            if event.type == l.QUIT:
                self.running = False

            if (
                event.type == pg.MOUSEBUTTONDOWN
                and not self.bird.flying
                and not self.game_is_over
            ):
                self.bird.flying = True

        # pg.display.update() # ? Unnecessary
        pg.display.flip()  # update the contents of the entire display

    def run(self):
        logger.info("Running game loop")
        self.running = True
        frame_count = 1
        while self.running:
            logger.trace("-> Frame {} begins", frame_count)

            self.display.blit(self.background, (0, 0))
            self.process_input()
            # self.update_state()
            self.render()
            self.clock.tick(self.fps)

            logger.trace("-> Frame {} ends", frame_count)
            frame_count += 1
        pg.quit()


class GameFactory:
    pass
