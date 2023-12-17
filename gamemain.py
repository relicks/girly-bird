# flake8: noqa: PLR0912, PLR0913
import random
import sys
from pathlib import Path

import pygame as pg
import pygame.locals as l
from loguru import logger
from pygame import mixer

from chilly_bird.configs import load_config


class Bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # ? Creates the bird animation frames:
        self.images = [
            pg.image.load(f"game_files/bird/bird{num}.png") for num in range(1, 4)
        ]
        self.i = 0  # Index of the image in the self.images list
        self.anim_spd = 0  # Speed at which the animation runs
        self.image = self.images[self.i]
        self.rect = self.image.get_rect(center=(x, y))
        self.jump_sound = pg.mixer.Sound("./assets/sound/jump_sound.mp3")
        self.gravity = 0
        self.clicked = False
        self.flying = False
        self.visible = True
        logger.info("Bird initialized")

    def update(self):
        logger.trace("Bird updating")
        if self.flying:
            logger.trace("Bird is flying down")
            # Creating the force that constantly pulls
            # the bird down (essentially gravity)
            self.gravity += 0.17
            self.gravity = min(self.gravity, 2.6)
            if self.rect.bottom < 384:
                self.rect.y += int(self.gravity)

        if self.visible:
            """Creating the bird's ability to jump"""
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                logger.trace("Fly key pressed")
                self.clicked = True
                self.gravity = -3.5
                self.jump_sound.play()
            if not pg.mouse.get_pressed()[0] == 1:
                self.clicked = False

            """Flapping animation"""
            self.anim_spd += 1
            anim_spd_limit = 5  # flapping animation speed
            if self.anim_spd > anim_spd_limit:
                # Otherwise the speed of the wings flapping
                # would be indefinitely increasing
                self.anim_spd = 0
                self.i += 1
                if self.i >= len(self.images):
                    # In order to create an endless loop of animation and
                    # the bird would not stop flapping its wings right after
                    # the first iteration of the list
                    self.i = 0
            # Improving the animation of jumping:
            self.image = pg.transform.rotate(self.images[self.i], self.gravity * -1.25)
        else:
            # Animaton of the bird falling:
            self.image = pg.transform.rotate(self.images[self.i], -75)
            self.gravity = 10

    def hidden(self, b: bool):
        self.visible = b


class Pipe(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, location: int, pipe_gap: int, scroll_speed: int):
        super().__init__()
        self.image = pg.image.load("game_files/pipe.png")
        self.rect = self.image.get_rect()
        self.pipe_gap = pipe_gap
        self.scroll_speed = scroll_speed
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
        if self.rect.right < 0:
            logger.debug("Pipe moved out of screen, killing it")
            # As soon as the rightmost point of a pipe disappears
            # from the screen, it is deleted. Otherwise disappeared
            # pipes remain in the game memory
            self.kill()


class RestartButton:
    def __init__(self, x, y, image):
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
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pg.Surface):
        logger.trace("Drawing Girl")
        surface.blit(self.image, self.rect)


class GameState:
    def __init__(self) -> None:
        raise NotImplementedError


# """Setting the game's parameters (values)"""
# SPEED_SCROLL = 2
# PIPE_FREQ = 1250  # New pipes appear every 1.25 seconds
# GAP_BTW_PIPES = 100


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
        self.background = pg.image.load("game_files/background.png").convert()

        self.road_img = pg.image.load("game_files/road.png").convert()
        self.restart_button_img = pg.image.load(
            "game_files/restart.button.png"
        ).convert()
        self.disappointed_girl_img = pg.image.load(
            "game_files/disappointed.girl.png"
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

    def draw_text(self, text, font, text_col, x, y):
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

        # pg.display.update()
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


def configure_logger(
    logger_level: str = "TRACE",
    log_file_path: str = "./logs/runtime_{time}.log",
    print_stdout: bool = False,
) -> None:
    path = Path(log_file_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    logger.remove(0)
    logger.add(path, level=logger_level, retention=5)

    if print_stdout:
        logger.add(sys.stderr, level="INFO")


if __name__ == "__main__":
    configure_logger(print_stdout=True)
    cfg = load_config()

    logger.info("Initializing Game")
    game = Game(cfg.window.screen_width, cfg.window.screen_height)
    game.run()
# pg.init()


# # ! Naming the game, setting the screen size, game icon and music


# FPS = 60  # ! Setting the game's timeframe
# SCREEN_WIDTH = 432
# SCREEN_HEIGHT = 468
# DISPLAYSURF = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pg.display.set_caption("Chilly Bird")
# pg.display.set_icon(pg.image.load("game_files/game.icon.png"))

# """Defining the fonts and their color"""


# color = (235, 221, 190)
# font1 = pg.font.Font("game_files/arcadeclassic.ttf", 30)  # For displaying the score
# font2 = pg.font.Font("game_files/arcadeclassic.ttf", 18)  # For instructing a player

# """Loading the images"""


# background = pg.image.load(
#     "game_files/background.png"
# ).convert()  # Convert() enables faster blitting -> improves performance
# road = pg.image.load("game_files/road.png").convert()
# restart_button = pg.image.load("game_files/restart.button.png").convert()
# disappointed_girl = pg.image.load(
#     "game_files/disappointed.girl.png"
# ).convert_alpha()  # transparent background
# mixer.music.load("game_files/game.music.mp3")


# def draw_text(text, font, text_col, x, y):  # Instructs a player and displays score
#     global DISPLAYSURF
#     image = font.render(text, True, text_col)
#     DISPLAYSURF.blit(image, (x, y))


# def reset_game():  # Returns everything to its pre-launched position
#     global pipe_group, chilly_bird, score
#     pipe_group.empty()
#     chilly_bird.rect.x = 50
#     chilly_bird.rect.y = round(SCREEN_HEIGHT / 2)
#     score = 0
#     return score


# # ? Setting initial flags
# initial_road_scroll = 0
# within_pipe = False
# score = 0
# is_flying = False
# game_is_over = False

# # ? Setting objects
# bird_group = pg.sprite.Group()
# chilly_bird = Bird(50, SCREEN_HEIGHT / 2)
# bird_group.add(chilly_bird)

# pipe_group = pg.sprite.Group()
# # First pipe appears right when the game starts
# # (i.e. without a 1.25 seconds delay unlike the subsequent ones)
# leftmost_pipe = pg.time.get_ticks() - PIPE_FREQ


# button = RestartButton(SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT / 2 - 80, restart_button)
# girl = Girl(140, 200, disappointed_girl)

# pg.mixer.music.play(-1)  # Infinite music loop
# clock = pg.time.Clock()

# game_is_running = True
# while game_is_running:
# clock.tick(FPS)
# DISPLAYSURF.blit(background, (0, 0))

# if pg.mouse.get_pressed()[1]:
#     pg.mixer.music.fadeout(
#         1000
#     )  # Stops the music if mouse wheel is pressed with the 1 second delay
# if pg.mouse.get_pressed()[2]:
#     pg.mixer.music.play(-1)  # Unmutes the music if right mouse button is pressed

# if is_flying is False and game_is_over is False:
#     draw_text(
#         "    ".join("press left mouse button to start the game".split()),
#         font2,
#         color,
#         20,
#         275,
#     )
#     draw_text(
#         "    ".join("press mouse wheel to mute the music".split()),
#         font2,
#         color,
#         45,
#         290,
#     )
#     draw_text(
#         "    ".join("press right mouse button to unmute the music".split()),
#         font2,
#         color,
#         5,
#         305,
#     )
# bird_group.draw(DISPLAYSURF)
# bird_group.update()
# pipe_group.draw(DISPLAYSURF)
# DISPLAYSURF.blit(road, (initial_road_scroll, 384))

# """Counting player's score"""
# if len(pipe_group) > 0:  # Some pipes had been created
#     if (
#         bird_group.sprites()[0].rect.left
#         > pipe_group.sprites()[
#             0
#         ].rect.left  # The leftmost point of the bird has passed the leftmost point of a pipe
#         and bird_group.sprites()[0].rect.right
#         < pipe_group.sprites()[
#             0
#         ].rect.right  # But the bird's rightmost point has not passed the rightmost point of the pipe
#         and not within_pipe
#     ):
#         within_pipe = True  # The bird is within the range of the leftmost and rightmost points of the pipe

#     if within_pipe:
#         if (
#             bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right
#         ):  # And only if the bird's leftmost point passes the rightmost point of a pipe, one point is added to the score
#             score += 1
#             within_pipe = False  # The bird is not within the range of the extreme points of a particular pipe

# draw_text(str(score), font1, color, SCREEN_WIDTH / 2, 12)

# if (
#     pg.sprite.groupcollide(bird_group, pipe_group, False, False)
#     or chilly_bird.rect.top < 0  # The bird hits the top of the screen
# ):
#     game_is_over = True

# if chilly_bird.rect.bottom >= 384:
#     game_is_over = True
#     is_flying = False

# if not game_is_over and is_flying:
#     """Generating new pipes"""
#     current_time = pg.time.get_ticks()
#     if (
#         current_time - leftmost_pipe > PIPE_FREQ
#     ):  # Enough time has passed -> creating new pipes
#         pipe_distance = random.randint(
#             -50, 50
#         )  # Pipes are randomly generated within the range of 100 pixels
#         pipe_down = Pipe(SCREEN_WIDTH, round(SCREEN_HEIGHT / 2 + pipe_distance), 1)
#         pipe_up = Pipe(SCREEN_WIDTH, round(SCREEN_HEIGHT / 2 + pipe_distance), -1)
#         pipe_group.add(pipe_down)
#         pipe_group.add(pipe_up)
#         leftmost_pipe = current_time
#     """Making the road scrolling"""
#     initial_road_scroll -= SPEED_SCROLL
#     if abs(initial_road_scroll) > 17:
#         initial_road_scroll = 0
#     pipe_group.update()

# if game_is_over:
#     girl.draw()
#     if button.draw():
#         game_is_over = False
#         score = reset_game()

# for event in pg.event.get():
#     if event.type == l.QUIT:
#         game_is_running = False

#     if event.type == pg.MOUSEBUTTONDOWN and not is_flying and not game_is_over:
#         is_flying = True
# pg.display.update()
