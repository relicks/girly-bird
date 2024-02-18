from collections.abc import Sequence

from pygame.color import Color
from pygame.math import Vector2
from pygame.rect import Rect

Coordinate = tuple[float, float] | Sequence[float] | Vector2
RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

RectValue = (
    Rect
    | tuple[float | int, float | int, float | int, float | int]
    | tuple[Coordinate, Coordinate]
    | Sequence[float | int]
    | Sequence[Coordinate]
)
