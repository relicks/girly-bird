from tkinter import filedialog

import pygame as pg

from chilly_bird import graph_editor

from .types import Coordinate


def scale_keep_ratio(img: pg.Surface, scale: tuple[float, float]) -> pg.Surface:
    rect = img.get_rect()
    w, h = rect.w, rect.h
    max_w, max_h = scale
    if w <= max_w and h <= max_h:
        return img
    aspect_x = max_w / w
    aspect_y = max_h / h
    ratio = min(aspect_x, aspect_y)
    scale = w * ratio, h * ratio
    return pg.transform.scale(img, scale)


def create_rect(point1: Coordinate, point2: Coordinate) -> pg.Rect:
    x1, y1 = point1
    x2, y2 = point2
    left = min(x1, x2)
    top = min(y1, y2)
    w = max(x1, x2) - left
    h = max(y1, y2) - top
    return pg.Rect(left, top, w, h)


def open_image(scale: tuple[int, int]) -> pg.Surface | None:
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if filename:
        img = pg.image.load(filename).convert_alpha()
        return scale_keep_ratio(img, scale)


def open_editor(scale: tuple[int, int]) -> pg.Surface | None:
    with graph_editor.GraphEditor() as editor:
        if img := editor.run():
            return pg.transform.scale(img, scale)


class Rect2P(pg.Rect):
    def __init__(self, topleft: Coordinate, bottomright: Coordinate) -> None:
        super().__init__(
            topleft, (bottomright[0] - topleft[0], bottomright[1] - topleft[1])
        )
