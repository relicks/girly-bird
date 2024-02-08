from tkinter import filedialog

import pygame as pg


def get_img_path() -> str:
    return filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )


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


def open_image(scale: tuple[int, int]) -> pg.Surface | None:
    filename = get_img_path()
    if filename:
        img = pg.image.load(filename)
        return scale_keep_ratio(img, scale)


def create_rect(point1: tuple[int, int], point2: tuple[int, int]) -> pg.Rect:
    x1, y1 = point1
    x2, y2 = point2
    left = min(x1, x2)
    top = min(y1, y2)
    w = max(x1, x2) - left
    h = max(y1, y2) - top
    return pg.Rect(left, top, w, h)


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
    def __init__(self, max_screen_w=800, max_screen_h=600):
        self.FPS = 24
        self.circle_color = (0, 0, 0)
        self.curr_color = (200, 0, 0)
        self.min_circle_size = 10
        self.selected_rect = None
        self.curr_start = None

        self.back_image = open_image((max_screen_w, max_screen_h))
        rect = self.back_image.get_rect()
        self.previous_screen_mode = pg.display.get_window_size()
        self.screen = pg.display.set_mode((rect.w, rect.h))

    def start_selection(self, pos):
        self.curr_start = pos

    def new_selection(self, pos):
        if pg.math.Vector2(self.curr_start).distance_to(pos) >= self.min_circle_size:
            self.selected_rect = create_rect(self.curr_start, pos)

    def draw_circle(self, color, rect, width=1):
        pg.draw.ellipse(self.screen, color, rect, width=width)

    def draw_selection(self):
        if self.selected_rect:
            self.draw_circle(self.circle_color, self.selected_rect)

    def draw_current(self, pos):
        rect = create_rect(self.curr_start, pos)
        self.draw_circle(self.curr_color, rect)

    def draw_back(self):
        if self.back_image:
            self.screen.blit(self.back_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))

    def get_image_selected(self):
        if self.selected_rect:
            w, h = self.selected_rect.w, self.selected_rect.h
            img = pg.Surface((w, h)).convert_alpha()
            img.blit(self.back_image, (0, 0), area=self.selected_rect)
            ellipsify(img)
            return img

    def main(self):
        clock = pg.time.Clock()
        # start_time = pg.time.get_ticks()
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

            self.draw_back()
            if drawing:
                self.draw_current(pos)
            self.draw_selection()
            clock.tick(self.FPS)
            pg.display.update()

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        pg.display.set_mode(self.previous_screen_mode)
