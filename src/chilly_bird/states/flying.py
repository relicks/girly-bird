"""Contains implemented state of the Flying scene."""

# flake8: noqa: D107, D102
from random import randint
from typing import TYPE_CHECKING

import pygame as pg
from loguru import logger
from pygame.sprite import AbstractGroup

from chilly_bird.configs import MainConfig
from chilly_bird.objects.pipes import Pipe
from chilly_bird.objects.textboxes import TextSprite
from chilly_bird.states.base import BaseState

if TYPE_CHECKING:
    from chilly_bird.objects.bird import Bird


class Flying(BaseState):
    """Flying scene."""

    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        """Initialize the Flying.

        Raises `ValueError` if `cfg` is not passed.
        """
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")  # noqa: TRY003
        self.cfg = cfg
        # ? Init params
        self.score = 0
        self.game_is_over = False
        self.road_scroll = 0
        self.within_pipe = False

        self.scroll_speed = 2
        self.pipe_freq = 1250  # New pipes appear every 1.25 seconds
        self.gap_btw_pipes = 100
        self.leftmost_pipe = pg.time.get_ticks() - self.pipe_freq
        self.passed_leftmost_pipe = None

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
        self.inc_score()
        self.groups["score"].update(text=str(self.score))
        self.handle_collision()
        self.generate_pipes()
        super().update(dt)

    def draw(self, surface: pg.Surface) -> None:
        return super().draw(surface)

    def on_exit(self) -> dict[str, AbstractGroup]:
        return self.groups

    def inc_score(self) -> None:
        """Increments the score when needed."""
        if len(self.groups["pipes"]) > 0:  # Some pipes had been created
            current_pipe: Pipe = self.groups["pipes"].sprites()[0]
            bird = self.groups["bird"].sprites()[0]
            if (
                current_pipe != self.passed_leftmost_pipe
                and bird.rect.left > current_pipe.rect.right
            ):
                self.passed_leftmost_pipe = current_pipe
                self.score += 1

    def handle_collision(self) -> None:
        """Handle collisions between Bird and Pipes."""
        # ? Collision handling
        bird = self.groups["bird"].sprites()[0]
        pipe_group = self.groups["pipes"]
        bird_collided_pipe = pg.sprite.spritecollideany(bird, pipe_group)
        bird_touched_screen_top = bird.rect.top < 0
        if bird_collided_pipe or bird_touched_screen_top:
            self.game_is_over = True
            self.done = True
            bird.visible = False

        floor_level = 384
        if bird.rect.bottom >= floor_level:
            self.game_is_over = True
            self.done = True
            bird.flying = False
            bird.visible = False

    def generate_pipes(self) -> None:
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
                    pos=(
                        self.screen_rect.width,
                        round(self.screen_rect.height / 2 + pipe_distance),
                    ),
                    direction="down",
                    pipe_gap=self.gap_btw_pipes,
                    scroll_speed=self.scroll_speed,
                    cfg=self.cfg,
                )
                pipe_up = Pipe(
                    pos=(
                        self.screen_rect.width,
                        round(self.screen_rect.height / 2 + pipe_distance),
                    ),
                    direction="up",
                    pipe_gap=self.gap_btw_pipes,
                    scroll_speed=self.scroll_speed,
                    cfg=self.cfg,
                )

                pipe_group.add([pipe_down, pipe_up])
                self.leftmost_pipe = current_time

            # Making the road scroll:
            self.road_scroll -= self.scroll_speed
            max_scroll_speed = 17
            if abs(self.road_scroll) > max_scroll_speed:
                self.road_scroll = 0
