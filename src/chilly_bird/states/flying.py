from random import randint

import pygame as pg
from loguru import logger
from pygame.sprite import AbstractGroup

from chilly_bird.configs import MainConfig
from chilly_bird.objects.bird import Bird
from chilly_bird.objects.pipes import Pipe
from chilly_bird.objects.textboxes import TextSprite
from chilly_bird.states.base import BaseState


class Flying(BaseState):
    def __init__(
        self, cfg: MainConfig | None = None, next_state: str | None = None
    ) -> None:
        super().__init__(cfg, next_state)
        if cfg is None:
            raise ValueError("cfg argument can't be None")
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

    def on_exit(self):
        return self.groups

    def inc_score(self) -> None:
        if len(self.groups["pipes"]) > 0:  # Some pipes had been created
            current_pipe: Pipe = self.groups["pipes"].sprites()[0]
            bird = self.groups["bird"].sprites()[0]
            if (
                current_pipe != self.passed_leftmost_pipe
                and bird.rect.left > current_pipe.rect.right
            ):
                self.passed_leftmost_pipe = current_pipe
                self.score += 1
            # # The leftmost point of the bird has passed the leftmost point of a pipe
            # leftmost_passed = bird.rect.left > leftmost_pipe.rect.left
            # # But the bird's rightmost point has not passed
            # # the rightmost point of the pipe
            # rightmost_not_passed = bird.rect.right < leftmost_pipe.rect.right
            # if leftmost_passed and rightmost_not_passed and not self.within_pipe:
            #     # The bird is within the range of the leftmost
            #     # and rightmost points of the pipe
            #     self.within_pipe = True

            # if self.within_pipe:
            #     logger.trace("Bird within pipe")
            #     if bird.rect.left > leftmost_pipe.rect.right:
            #         # And only if the bird's leftmost point passes the
            #         # rightmost point of a pipe, one point is added to the score
            #         self.score += 1

            #         # The bird is not within the range of the extreme
            #         # points of a particular pipe
            #         self.within_pipe = False

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

        floor_level = 384
        if bird.rect.bottom >= floor_level:
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
                    self.cfg,
                )
                pipe_up = Pipe(
                    self.screen_rect.width,
                    round(self.screen_rect.height / 2 + pipe_distance),
                    -1,
                    self.gap_btw_pipes,
                    self.scroll_speed,
                    self.cfg,
                )
                pipe_group.add([pipe_down, pipe_up])
                self.leftmost_pipe = current_time

            # Making the road scroll:
            self.road_scroll -= self.scroll_speed
            max_scroll_speed = 17
            if abs(self.road_scroll) > max_scroll_speed:
                self.road_scroll = 0
