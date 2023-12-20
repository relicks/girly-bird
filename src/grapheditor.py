"""
Задачи:
 - открыть изображение (клавиша "open")
 - на картинке позволить выбирать круги
    (нажать левую кнопка мыши - начать новый круг,
    движение мыши с нажатой клавишей - изменять размеры круга,
    отпустить левую кнопку - закончить круг
    клик правой клавишей - удалить круг)
 - сгенерировать картинки из исходной (клавиша "save")
"""
from tkinter import filedialog

import pygame as pg


def create_rect(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    left = min(x1, x2)
    top = min(y1, y2)
    w = max(x1, x2) - left
    h = max(y1, y2) - top
    return pg.Rect(left, top, w, h)


class CircleNode:
    def __init__(self, point1, point2):
        self.rect = create_rect(point1, point2)


def get_graphic_filename():
    return filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )


class GraphEditor:
    def __init__(self):
        self.open_key = pg.K_o  # открыть - буква "o"
        self.save_key = pg.K_s  # сохранить - буква "s"
        self.FPS = 24  # частота обновления
        self.circle_color = (0, 0, 0)
        self.curr_color = (200, 0, 0)
        self.min_circle_size = 10
        self.width, self.height = 800, 600  # размеры окна
        self.back_image = None
        self.circles = []
        self.curr_start = None
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Face Selector")

    def open_image(self):
        filename = get_graphic_filename()
        if filename:
            img = pg.image.load(filename)
            self.back_image = pg.transform.scale(img, (self.width, self.height))

    def start_circle(self, pos):
        self.curr_start = pos

    def remove_circle(self, pos):
        i = len(self.circles) - 1
        while i >= 0:
            c = self.circles[i]
            if c.rect.collidepoint(pos):
                self.circles.pop(i)
            i -= 1

    def add_circle(self, pos):
        if pg.math.Vector2(self.curr_start).distance_to(pos) >= self.min_circle_size:
            self.circles.append(CircleNode(self.curr_start, pos))

    def draw_circle(self, color, rect, width=1):
        pg.draw.ellipse(self.screen, color, rect, width=width)

    def draw_circles(self):
        for c in self.circles:
            self.draw_circle(self.circle_color, c.rect)

    def draw_current(self, pos):
        rect = create_rect(self.curr_start, pos)
        self.draw_circle(self.curr_color, rect)

    def draw_back(self):
        if self.back_image:
            self.screen.blit(self.back_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))

    def mainloop(self):
        clock = pg.time.Clock()
        game = True
        drawing = False
        while game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game = False
                elif event.type == pg.KEYDOWN:
                    if event.key == self.open_key:
                        self.open_image()
                    elif event.key == self.save_key:
                        self.save_images()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if event.button == 1:  # Левая клавиша
                        self.start_circle(pos)
                        drawing = True
                    elif event.button == 3:  # Правая клавиша
                        self.remove_circle(pos)
                elif event.type == pg.MOUSEMOTION:
                    if drawing:
                        pos = pg.mouse.get_pos()
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:  # Левая клавиша
                        self.add_circle(pg.mouse.get_pos())
                        drawing = False

            self.draw_back()
            if drawing:
                self.draw_current(pos)
            self.draw_circles()
            pg.display.update()
            clock.tick(self.FPS)


if __name__ == "__main__":
    GraphEditor().mainloop()
