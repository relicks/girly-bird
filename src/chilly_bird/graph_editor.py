import pygame as pg
from typing_extensions import Self

from . import utils
from .types import ColorValue, Coordinate, RectValue


def ellipsify(image: pg.Surface) -> None:
    rect = image.get_rect()
    w, h = rect.w, rect.h
    mask_surface = pg.Surface((w, h), pg.SRCALPHA)
    pg.draw.ellipse(mask_surface, (255, 255, 255, 255), rect, 0)
    ellipse_mask = pg.mask.from_surface(mask_surface)
    for y in range(h):
        for x in range(w):
            if not ellipse_mask.get_at((x, y)):
                image.set_at((x, y), (0, 0, 0, 0))


class GraphEditor:
    def __init__(self, max_screen_w: int = 800, max_screen_h: int = 600) -> None:
        self.FPS = 24
        self.circle_color = pg.color.Color("black")
        self.curr_color = pg.color.Color("orangered2")
        self.min_circle_size = 10
        self.selected_rect = None
        self.curr_start = (0, 0)

        self.user_image = utils.open_image((max_screen_w, max_screen_h))
        if self.user_image is None:
            return

        rect = self.user_image.get_rect()
        self.previous_screen_mode = pg.display.get_window_size()
        self.screen = pg.display.set_mode((rect.w, rect.h))
        self.background = self.create_checkered_background(10)

    def create_checkered_background(self, tile_size: int = 20) -> pg.Surface:
        color1 = pg.Color(128, 128, 128)  # Grey color  1
        color2 = pg.Color(64, 64, 64)  # Grey color  2

        # Create a new surface for the checkered pattern
        checkered_background = pg.Surface(self.screen.get_size())

        # Draw the checkered pattern
        for y in range(0, checkered_background.get_height(), tile_size):
            for x in range(0, checkered_background.get_width(), tile_size):
                # Choose the color based on the position
                if (x // tile_size + y // tile_size) % 2 == 0:
                    checkered_background.fill(color1, (x, y, tile_size, tile_size))
                else:
                    checkered_background.fill(color2, (x, y, tile_size, tile_size))

        return checkered_background

    def start_selection(self, pos: Coordinate) -> None:
        self.curr_start = pos

    def new_selection(self, pos: Coordinate) -> None:
        if pg.math.Vector2(self.curr_start).distance_to(pos) >= self.min_circle_size:
            self.selected_rect = utils.create_rect(self.curr_start, pos)

    def draw_circle(self, color: ColorValue, rect: RectValue, width: int = 1) -> None:
        pg.draw.ellipse(self.screen, color, rect, width=width)

    def draw_selection(self) -> None:
        if self.selected_rect:
            self.draw_circle(self.circle_color, self.selected_rect)

    def draw_current(self, pos: Coordinate) -> None:
        rect = utils.create_rect(self.curr_start, pos)
        self.draw_circle(self.curr_color, rect)

    def draw_user_image(self) -> None:
        if self.user_image:
            self.screen.blit(self.user_image, (0, 0))
        else:
            self.screen.fill(pg.color.Color("white"))

    def draw_background(self) -> None:
        # Blit the background onto the screen
        self.screen.blit(self.background, (0, 0))

    def get_image_selected(self) -> pg.Surface | None:
        if self.selected_rect and self.user_image:
            img = pg.Surface(
                (self.selected_rect.w, self.selected_rect.h)
            ).convert_alpha()
            img.blit(self.user_image, (0, 0), area=self.selected_rect)
            ellipsify(img)
            return img

    def run(self) -> pg.Surface | None:
        if self.user_image is None:
            return
        clock = pg.time.Clock()
        pg.time.wait(300)
        pg.event.clear()
        drawing = False
        pos = (0, 0)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return self.get_image_selected()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pg.mouse.get_pos()
                    self.start_selection(pos)
                    drawing = True
                elif event.type == pg.MOUSEMOTION:
                    if drawing:
                        pos = pg.mouse.get_pos()
                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.new_selection(pg.mouse.get_pos())
                    drawing = False

            self.draw_background()
            self.draw_user_image()
            if drawing:
                self.draw_current(pos)
            self.draw_selection()
            clock.tick(self.FPS)
            pg.display.update()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_details) -> None:
        pg.display.set_mode(self.previous_screen_mode)
