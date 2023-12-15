import pygame as pg
import pygame.locals as l
import random
from pygame import mixer

pg.init()

'''Setting the game's timeframe'''
FPS = 60
clock = pg.time.Clock()

'''Naming the game, setting the screen size, game icon and music'''
SCREEN_WIDTH = 432
SCREEN_HEIGHT = 468
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Chilly Bird")
pg.display.set_icon(pg.image.load("game_files/game.icon.png"))
mixer.music.load("game_files/game.music.mp3")

'''Defining the fonts and their color'''
color = (235, 221, 190)
font1 = pg.font.Font("game_files/arcadeclassic.ttf", 30) # For displaying the score
font2 = pg.font.Font("game_files/arcadeclassic.ttf", 18) # For instructing a player

'''Loading the images'''
background = pg.image.load("game_files/background.png").convert() # Convert() enables faster blitting -> improves performance
road = pg.image.load("game_files/road.png").convert()
restart_button = pg.image.load("game_files/restart.button.png").convert()
disappointed_girl = pg.image.load("game_files/disappointed.girl.png").convert_alpha() #transparent background

'''Setting the game's parameters (values)'''
road_scroll = 0
speed_scroll = 2
pipe_freq = 1250 # New pipes appear every 1.25 seconds
gap_btw_pipes = 100
leftmost_pipe = pg.time.get_ticks() - pipe_freq # First pipe appears right when the game starts (i.e. without a 1.25 seconds delay unlike the subsequent ones)
within_pipe = False
score = 0
is_flying = False
game_is_over = False


def draw_text(text, font, text_col, x, y): # Instructs a player and displays score
    global screen
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))


def reset_game(): # Returns everything to its pre-launched position
    global pipe_group, chilly_bird, score
    pipe_group.empty()
    chilly_bird.rect.x = 50
    chilly_bird.rect.y = SCREEN_HEIGHT / 2
    score = 0
    return score


class Bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self) # Constructor for the sprite class
        self.images = [
            pg.image.load(f"game_files/bird/bird{num}.png") for num in range(1, 4) # Creates the bird animation
        ]
        self.i = 0 # Index of the image in the self.images list
        self.anim_spd = 0  # Speed at which the animation runs
        self.image = self.images[self.i]
        self.rect = self.image.get_rect(center=(x, y))
        self.gravity = 0
        self.clicked = False

    def update(self):
        if is_flying:
            '''Creating the force that constantly pulls the bird down (essentially gravity)'''
            self.gravity += 0.17
            self.gravity = min(self.gravity, 2.6)
            if self.rect.bottom < 384:
                self.rect.y += int(self.gravity)

        if not game_is_over:
            '''Creating the bird's ability to jump'''
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.gravity = -3.5
            if not pg.mouse.get_pressed()[0] == 1:
                self.clicked = False

            '''Flapping animation'''
            self.anim_spd += 1
            anim_spd_limit = 5 # The greater this value, the slower the bird flaps its wings
            if self.anim_spd > anim_spd_limit:
                self.anim_spd = 0 # Otherwise the speed of the wings flapping would be indefinitely increasing
                self.i += 1
                if self.i >= len(self.images):
                    self.i = 0 # In order to create an endless loop of animation and the bird would not stop flapping its wings right after the first iteration of the list
            self.image = pg.transform.rotate(self.images[self.i], self.gravity * -1.25) # Improving the animation of jumping
        else:
            self.image = pg.transform.rotate(self.images[self.i], -75) # Animaton of the bird falling
            self.gravity = 10


class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("game_files/pipe.png")
        self.rect = self.image.get_rect()
        if location == 1: # Pipe pointing up
            self.rect.topleft = [x, y + gap_btw_pipes / 2] # +35 pixels in order to create a gap
        if location == -1: # Pipe pointing down
            self.image = pg.transform.flip(self.image, False, True) # Fliping not by the x-axis (False), but by the y-axis (True)
            self.rect.bottomleft = [x, y - gap_btw_pipes / 2]# -35 pixels in order to create a gap (70 pixels overall)

    def update(self):
        self.rect.x -= speed_scroll # Forces pipes to constantly move to the left
        if self.rect.right < 0: # As soon as the rightmost point of a pipe disappears from the screen, it deletes
            self.kill() # Otherwise disappeared pipes remain in the game memory


class RestartButton:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, self.rect)
        return action


class Girl:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        global screen
        screen.blit(self.image, self.rect)


bird_group = pg.sprite.Group()
chilly_bird = Bird(50, SCREEN_HEIGHT / 2)
bird_group.add(chilly_bird)

pipe_group = pg.sprite.Group()

button = RestartButton(SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT / 2 - 80, restart_button)
girl = Girl(140, 200, disappointed_girl)

pg.mixer.music.play(-1) # Infinite music loop

game_is_running = True
while game_is_running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    if pg. mouse.get_pressed()[1]:
        pg.mixer.music.fadeout(1000) # Stops the music if mouse wheel is pressed with the 1 second delay
    if pg.mouse.get_pressed()[2]:
        pg.mixer.music.play(-1) # Unmutes the music if right mouse button is pressed

    if is_flying == False and game_is_over == False:
        draw_text(
            "    ".join("press left mouse button to start the game".split()),
            font2,
            color,
            20,
            275,
            )
        draw_text(
            "    ".join("press mouse wheel to mute the music".split()),
            font2,
            color,
            45,
            290,
            )
        draw_text(
            "    ".join("press right mouse button to unmute the music".split()),
            font2,
            color,
            5,
            305,
            )
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(road, (road_scroll, 384))

    '''Counting player's score'''
    if len(pipe_group) > 0: # Some pipes had been created
        if (
            bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left # The leftmost point of the bird has passed the leftmost point of a pipe
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right # But the bird's rightmost point has not passed the rihtmost point of the pipe
            and not within_pipe
            ):
            within_pipe = True # The bird is within the range of the leftmost and rightmost points of the pipe

        if within_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right: # And only if the bird's leftmost point passes the rightmost point of a pipe, one point is added to the score
                score += 1
                within_pipe = False # The bird is not within the range of the extreme points of a particular pipe

    draw_text(str(score), font1, color, SCREEN_WIDTH / 2, 12)

    if (
        pg.sprite.groupcollide(bird_group, pipe_group, False, False)
        or chilly_bird.rect.top < 0 # The bird hits the top of the screen
        ):
        game_is_over = True

    if chilly_bird.rect.bottom >= 384:
        game_is_over = True
        is_flying = False

    if not game_is_over and is_flying:
        '''Generating new pipes'''
        current_time = pg.time.get_ticks()
        if current_time - leftmost_pipe > pipe_freq: # Enough time has passed -> creating new pipes
            pipe_distance = random.randint(-50, 50) # Pipes are randomly generated within the range of 100 pixels
            pipe_down = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 + pipe_distance, 1)
            pipe_up = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 + pipe_distance, -1)
            pipe_group.add(pipe_down)
            pipe_group.add(pipe_up)
            leftmost_pipe = current_time
        '''Making the road scrolling'''
        road_scroll -= speed_scroll
        if abs(road_scroll) > 17:
            road_scroll = 0
        pipe_group.update()

    if game_is_over:
        girl.draw()
        if button.draw():
            game_is_over = False
            score = reset_game()

    for event in pg.event.get():
        if event.type == l.QUIT:
            game_is_running = False

    if event.type == pg.MOUSEBUTTONDOWN and not is_flying and not game_is_over:
        is_flying = True
    pg.display.update()

pg.quit()