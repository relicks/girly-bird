import pygame as pg

from chilly_bird.objects.textboxes import TextSprite

pg.init()

pg.display.set_caption("Quick Start")
window_surface = pg.display.set_mode((800, 600))
font = pg.font.SysFont("Arial", 20)

text_box = TextSprite("hyht! aaa", font, pg.color.Color("white"), (500, 500))
text_box2 = TextSprite("FAST!", font, pg.color.Color("red"), (200, 300))
text_group = pg.sprite.Group()
text_group.add([text_box, text_box2])

background = pg.Surface((800, 600))
background.fill(pg.Color("#000000"))

is_running = True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))
    text_group.draw(window_surface)
    pg.display.update()
