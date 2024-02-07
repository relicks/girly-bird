from tkinter import filedialog
from typing import TypeAlias

import pygame as pg

Coordinate: TypeAlias = tuple[float, float] | pg.Vector2


def get_img_path() -> str:
    return filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )


def open_image(scale: tuple[int, int]) -> pg.Surface | None:
    filename = get_img_path()
    if filename:
        img = pg.image.load(filename)
        return pg.transform.scale(img, scale)


class Rect2P(pg.Rect):
    def __init__(self, topleft: Coordinate, bottomright: Coordinate) -> None:
        super().__init__(
            topleft, (bottomright[0] - topleft[0], bottomright[1] - topleft[1])
        )
