from tkinter import filedialog

import pygame as pg


def get_img_path() -> str:
    return filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )


def open_image(scale: tuple[int, int]) -> pg.Surface | None:
    filename = get_img_path()
    if filename:
        img = pg.image.load(filename)
        return pg.transform.scale(img, scale)
