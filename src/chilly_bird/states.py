from abc import ABC, abstractmethod
from collections.abc import Mapping
from random import randint

import pygame as pg
from loguru import logger
from pygame.event import Event
from pygame.sprite import AbstractGroup

from chilly_bird.configs import MainConfig
from chilly_bird.objects.bird import Bird
from chilly_bird.objects.buttons import BUTTON_PRESSED, RestartButton
from chilly_bird.objects.girls import Girl
from chilly_bird.objects.pipes import Pipe
from chilly_bird.objects.road import Road
from chilly_bird.objects.textboxes import TextSprite


class BaseState(ABC):
    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        self.done = False
        self.next_state = next_state
        self.screen_rect = pg.display.get_surface().get_rect()
        self.groups: dict[str, pg.sprite.AbstractGroup] = {}

    def handle_event(self, event: pg.event.Event) -> None:
        return None

    def update(self, dt: int) -> None:
        for group in self.groups.values():
            group.update()

    def draw(self, surface: pg.Surface) -> None:
        for group in self.groups.values():
            group.draw(surface)

    @abstractmethod
    def on_enter(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        pass

    def on_exit(self) -> dict[str, pg.sprite.AbstractGroup]:
        return self.groups


class StartScreen(BaseState):
    def __init__(self, cfg: MainConfig | None = None, next_state: str | None = None):
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")
        # self.bird = Bird(50, self.screen_rect.height / 2)
        self.font = pg.font.Font(cfg.fonts.text_font, cfg.fonts.text_font_size)
        self.font_color = (235, 221, 190)
        self.texts = [
            TextSprite(
                "    ".join("press left mouse button to start the game".split()),
                font=self.font,
                color=self.font_color,
                pos=(20, 275),
            ),
            TextSprite(
                "    ".join("press mouse wheel to mute the music".split()),
                font=self.font,
                color=self.font_color,
                pos=(45, 290),
            ),
            TextSprite(
                "    ".join("press right mouse button to unmute the music".split()),
                font=self.font,
                color=self.font_color,
                pos=(5, 305),
            ),
        ]
        self.groups.update(
            {
                "text": pg.sprite.Group(*self.texts),
                "bird": pg.sprite.GroupSingle(Bird(50, self.screen_rect.height / 2)),
                "road": pg.sprite.GroupSingle(Road(cfg)),
            }
        )

    def on_enter(self, passed_groups: Mapping[str, pg.sprite.AbstractGroup]) -> None:
        return super().on_enter(passed_groups)

    def handle_event(self, event: Event) -> None:
        if event.type == pg.constants.MOUSEBUTTONDOWN:
            match event.button:
                case 1:  # LMB
                    self.done = True


class Flying(BaseState):
    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")

        # ? Init params
        self.score = 0
        self.game_is_over = False
        self.road_scroll = 0
        self.within_pipe = False

        self.scroll_speed = 2
        self.pipe_freq = 1250  # New pipes appear every 1.25 seconds
        self.gap_btw_pipes = 100
        self.leftmost_pipe = pg.time.get_ticks() - self.pipe_freq

        self.groups.update(
            {
                "pipes": pg.sprite.Group(),
                "score": pg.sprite.GroupSingle(
                    TextSprite(
                        str(self.score),
                        pg.font.Font(cfg.fonts.score_font, cfg.fonts.score_font_size),
                        cfg.fonts.color,
                        (self.screen_rect.width / 2, 12),  # type: ignore
                    )
                ),
            }
        )

    def on_enter(self, passed_groups: dict[str, AbstractGroup]) -> None:
        self.score = 0
        self.game_is_over = False
        self.road_scroll = 0

        self.groups["pipes"].empty()

        bird_group: pg.sprite.GroupSingle[Bird] = passed_groups["bird"]  # type: ignore
        bird_group.sprite.flying = True
        self.groups.update({"bird": bird_group, "road": passed_groups["road"]})
        self.groups["pipes"].update(scroll_speed=self.scroll_speed)

    def update(self, dt: int) -> None:
        current_score = self.inc_score()
        self.groups["score"].update(text=str(current_score))
        self.handle_collision()
        self.generate_pipes()
        super().update(dt)

    def draw(self, surface: pg.Surface) -> None:
        return super().draw(surface)

    def on_exit(self):
        return self.groups

    def inc_score(self) -> int:
        if len(self.groups["pipes"]) > 0:  # Some pipes had been created
            leftmost_pipe = self.groups["pipes"].sprites()[0]
            bird = self.groups["bird"].sprites()[0]
            # The leftmost point of the bird has passed the leftmost point of a pipe
            leftmost_passed = bird.rect.left > leftmost_pipe.rect.left
            # But the bird's rightmost point has not passed
            # the rightmost point of the pipe
            rightmost_not_passed = bird.rect.right < leftmost_pipe.rect.right
            if leftmost_passed and rightmost_not_passed and not self.within_pipe:
                # The bird is within the range of the leftmost
                # and rightmost points of the pipe
                self.within_pipe = True

            if self.within_pipe:
                logger.trace("Bird within pipe")
                if bird.rect.left > leftmost_pipe.rect.right:
                    # And only if the bird's leftmost point passes the
                    # rightmost point of a pipe, one point is added to the score
                    self.score += 1

                    # The bird is not within the range of the extreme
                    # points of a particular pipe
                    self.within_pipe = False
        return self.score

    def handle_collision(self):
        # ? Collision handling
        # bird_collided_pipe = pg.sprite.groupcollide(
        #     self.bird_group, self.pipe_group, False, False
        # )
        bird = self.groups["bird"].sprites()[0]
        pipe_group = self.groups["pipes"]
        bird_collided_pipe = pg.sprite.spritecollideany(bird, pipe_group)
        bird_touched_screen_top = bird.rect.top < 0
        if bird_collided_pipe or bird_touched_screen_top:
            self.game_is_over = True
            self.done = True
            bird.visible = False

        if bird.rect.bottom >= 384:
            self.game_is_over = True
            self.done = True
            bird.flying = False
            bird.visible = False

    def generate_pipes(self):
        bird = self.groups["bird"].sprites()[0]
        pipe_group = self.groups["pipes"]
        if not self.game_is_over and bird.flying:
            logger.trace("Generating new pipes")
            current_time = pg.time.get_ticks()

            # Enough time has passed -> creating new pipes:
            if current_time - self.leftmost_pipe > self.pipe_freq:
                # Pipes are randomly generated within the range of 100 pixels:
                pipe_distance = randint(-50, 50)
                pipe_down = Pipe(
                    self.screen_rect.width,
                    round(self.screen_rect.height / 2 + pipe_distance),
                    1,
                    self.gap_btw_pipes,
                    self.scroll_speed,
                )
                pipe_up = Pipe(
                    self.screen_rect.width,
                    round(self.screen_rect.height / 2 + pipe_distance),
                    -1,
                    self.gap_btw_pipes,
                    self.scroll_speed,
                )
                pipe_group.add([pipe_down, pipe_up])
                self.leftmost_pipe = current_time

            # Making the road scroll:
            self.road_scroll -= self.scroll_speed
            max_scroll_speed = 17
            if abs(self.road_scroll) > max_scroll_speed:
                self.road_scroll = 0


class GameOver(BaseState):
    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")

        self.groups.update(
            {
                "girl": pg.sprite.GroupSingle(
                    Girl(
                        x=140,
                        y=200,
                        image=pg.image.load(
                            cfg.main_scene.disappointed_girl_img
                        ).convert_alpha(),
                    )
                ),
                "restart_button": pg.sprite.GroupSingle(
                    RestartButton(
                        x=self.screen_rect.width // 2 - 40,
                        y=self.screen_rect.height // 2 - 80,
                        image=pg.image.load(
                            cfg.main_scene.restart_button_img
                        ).convert_alpha(),
                    )
                ),
            }
        )

    def on_enter(self, passed_groups: Mapping[str, AbstractGroup]) -> None:
        carry_over = ["bird", "pipes", "road", "score"]
        for group_name in carry_over:
            self.groups[group_name] = passed_groups[group_name]
        self.groups["pipes"].update(scroll_speed=0)

        # ? swapping girl sprite to the end, so it would be drawn on the front
        girl = self.groups["girl"]
        del self.groups["girl"]
        self.groups["girl"] = girl

        restart_button = self.groups["restart_button"]
        del self.groups["restart_button"]
        self.groups["restart_button"] = restart_button

    def on_exit(self) -> dict[str, AbstractGroup]:
        self.groups["bird"].sprites()[0].reset()
        self.groups["pipes"].empty()
        # self.groups["score"].update(text="0")
        return super().on_exit()

    def handle_event(self, event: Event) -> None:
        if event.type == BUTTON_PRESSED and event.button == "restart":
            self.done = True
