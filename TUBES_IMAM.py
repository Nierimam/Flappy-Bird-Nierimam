import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Define Font
font = pygame.font.SysFont("Bauhaus 93", 30)

# Define Colour
white = (255, 255, 255)

# define Game Variable
ground_scroll = 0
scroll_speed = 5
flying = False
game_over = False
pipe_gap = 250
pipe_frequency = 2500  # miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


# load IMAGES
bg = pygame.image.load("d:/GithubProject/Flappy-Bird-Nierimam/gambar/bg7-01.png")
ground = pygame.image.load("d:/GithubProject/Flappy-Bird-Nierimam/gambar/ground.png")
button_restart = pygame.image.load(
    "d:/GithubProject/Flappy-Bird-Nierimam/gambar/restart.png"
)


def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))


# def highest_text(text, font, text_colour, x, y):
#     img = font.render(text, True, text_colour)
#     screen.blit(img, (x,y))


def getHighestScore():
    with open("d:/GithubProject/Flappy-Bird-Nierimam/highest score.rtf", "r") as f:
        return f.read()


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(
                f"d:/GithubProject/Flappy-Bird-Nierimam/gambar/bird{num}.png"
            )
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 716:
                self.rect.y += int(self.vel)

        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked == True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked == False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "d:/GithubProject/Flappy-Bird-Nierimam/gambar/pipe.png"
        )
        self.rect = self.image.get_rect()

        # POSITION 1 IS FROM THE TOP, -1 IS FROM THE BOTTOM
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()  # DISAPPEAR PIPE THAT HAVE BEEN THROUGH


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        # GET MOUSE POSITION
        # get_post[0=x],[1=y]
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Draw Button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# CREATE RESTART BUTTON
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_restart)

try:
    highestScore = int(getHighestScore())
except:
    highestScore = 0

run = True
while run:
    clock.tick(fps)

    # memunculkan gambar dalam pygame
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground, (ground_scroll, 716))

    # check the score
    if len(pipe_group) > 0:
        if (
            bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right
            and pass_pipe == False
        ):
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    if highestScore < score:
        highestScore = score
    with open("d:/GithubProject/Flappy-Bird-Nierimam/highest score.rtf", "w") as f:
        f.write(str(highestScore))
    draw_text(f"highest score: {highestScore}", font, white, int(screen_width / 8), 20)

    # Look for collision, Burung menabrak pipa
    if (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy.rect.top < 0
    ):
        game_over = True

    # check if the bird has hit the ground
    if flappy.rect.bottom >= 716:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        # generate new pipe/ PENGATURAN PIPE
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    # CHECK FOR GAME OVER AND RESET
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and flying == False
            and game_over == False
        ):
            flying = True

    # memunculkan gambar dalam pygame
    pygame.display.update()
pygame.quit()
