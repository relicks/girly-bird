import pygame as pg

from chilly_bird import photoeditor

win_size = (432, 468)
bird_size = (100, 100)

pg.init()
screen = pg.display.set_mode(win_size)
screen.fill((120, 15, 180))
img = None
FPS = 60
clock = pg.time.Clock()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_o:
                img = photoeditor.GraphEditor().run()
                if img:
                    img = photoeditor.scale_keep_ratio(img, bird_size)
                screen = pg.display.set_mode(win_size)

    screen.fill((120, 15, 180))
    if img:
        screen.blit(img, (50, 50))
    pg.display.update()
    clock.tick(FPS)
