"""Contains various utilities that are used throughout the library."""

from tkinter import filedialog

import pygame as pg

from chilly_bird import graph_editor
from chilly_bird.types import Coordinate


def scale_keep_ratio(img: pg.Surface, max_size_box: tuple[float, float]) -> pg.Surface:
    """Scales the `img` down to fit into `max_size_box`, keeping the aspect ratio.

    Args:
    ----
        img: image to scale down
        max_size_box: the size `(w, h)` of the box to fit the `img` in, in px

    Returns:
    -------
        Scaled down `pygame.Surface`. If the given `img` is smaller

    """
    rect = img.get_rect()
    w, h = rect.w, rect.h
    max_w, max_h = max_size_box
    if w <= max_w and h <= max_h:
        return img
    aspect_x = max_w / w
    aspect_y = max_h / h
    ratio = min(aspect_x, aspect_y)
    max_size_box = w * ratio, h * ratio
    return pg.transform.scale(img, max_size_box)


def create_rect(point1: Coordinate, point2: Coordinate) -> pg.Rect:
    """Create a Pygame Rect object from two points.

    This function takes two points, each represented as a tuple of (x, y)
    coordinates, and returns a Pygame Rect object that encompasses the area between
    these two points. The Rect object is defined by its top-left corner (left, top)
    and its width and height.

    Args:
    ----
        point1: The first point, defined as a tuple of (x, y) coordinates.
        point2: The second point, defined as a tuple of (x, y) coordinates.

    Returns:
    -------
        A Pygame Rect object that represents the rectangle defined by the two points.

    Example:
    -------
        >>> create_rect((10, 20), (30, 40))
        <rect(10, 20, 20, 20)>

    """
    x1, y1 = point1
    x2, y2 = point2
    left = min(x1, x2)
    top = min(y1, y2)
    w = max(x1, x2) - left
    h = max(y1, y2) - top
    return pg.Rect(left, top, w, h)


def open_image(max_size_box: tuple[int, int]) -> pg.Surface | None:
    """Open an image using tkinter `filedialog` and return the pg.Surface object.

    Args:
    ----
        max_size_box: the size `(w, h)` of the box to fit the returned surface in, in px

    Returns:
    -------
        A pg.Surface object no larger than `max_size_box`

    """
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if filename:
        img = pg.image.load(filename).convert_alpha()
        return scale_keep_ratio(img, max_size_box)
    return None


def open_editor(max_size_box: tuple[int, int]) -> pg.Surface | None:
    """Open the skin editor in a new game loop and return the user-specified new skin.

    Args:
    ----
        max_size_box: the size `(w, h)` of the box to fit the new skin in, in px

    Returns:
    -------
        A new skin, no larger than `max_size_box`

    """
    with graph_editor.GraphEditor() as editor:
        if img := editor.run():
            return pg.transform.scale(img, max_size_box)
    return None
