# updated_escape_dragon.py
# By elizabethkushelevsky

# Worked with Charlotte Recktenwald and Chris Schneider


import sys, time, random, math, pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape The Dragon Game")
font = pygame.font.SysFont("hiraginosansgb", 18)
framerate = pygame.time.Clock()

class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    # X property
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        # update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
            keys = pygame.key.get_pressed()
            if keys[K_c]:
                player.first_frame = 11
            else:
                player.first_frame = 1

        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)

def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

def reset_arrow():
    y = random.randint(250, 350)
    arrow.position = 800, y

def draw_lives(lives):
    lives_surf = font.render('Lives: %s' % (lives), True, (255, 255, 255))
    lives_rect = lives_surf.get_rect()
    lives_rect.topright = (100, 10)
    screen.blit(lives_surf, lives_rect)

def draw_score(score):
    score_surf = font.render('Score: %s' % (score), True, (255, 255, 255))
    score_rect = score_surf.get_rect()
    score_rect.topright = (755, 10)
    screen.blit(score_surf, score_rect)

def play_again():
    print_text(display_font, 145, 168, "PRESS ANY KEY TO PLAY AGAIN")
    for event in pygame.event.get():
        if event.type == KEYUP:
            run_game()
            return
        elif event.type == QUIT:
            sys.exit()


def run_game():

    global lives, score, arrow, player, display_font

    # load bitmaps
    bg = pygame.image.load("background.png").convert_alpha()

    # create a sprite group
    group = pygame.sprite.Group()

    # create the dragon sprite
    dragon = MySprite(screen)
    dragon.load("dragon.png", 260, 150, 3)
    dragon.position = 100, 230
    group.add(dragon)

    # create the player sprite
    player = MySprite(screen)
    player.load("caveman.png", 50, 64, 8)
    player.first_frame = 1
    player.last_frame = 7
    player.position = 400, 303
    group.add(player)

    # create the arrow sprite
    arrow = MySprite(screen)
    arrow.load("flame.png", 40, 16, 1)
    arrow.position = 800, 320
    group.add(arrow)

    arrow_vel = 8.0
    game_over = False
    you_win = False
    display_font = pygame.font.SysFont("hiraginosansgb", 30) #https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font
    jumping = False
    crouching = False
    jump_vel = 0.0
    player_start_y = player.Y
    lives = 5
    score = 0

    while True:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not jumping:
                        jumping = True
                        crouching = False
                        jump_vel = -8.0
                    elif jumping and player.Y > 200:
                        jump_vel = -8.0
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if jumping:
                        jumping = False
                        crouching = False
                        jump_vel = 8.0

        # update the arrow
        if not game_over:
            arrow.X -= arrow_vel
            if arrow.X < -40: reset_arrow()

        # did arrow hit player?
        if pygame.sprite.collide_rect(arrow, player):
            reset_arrow()
            player.X -= 10

            lives -= 1
            if lives == 0:
                game_over = True

        # did arrow hit dragon?
        if pygame.sprite.collide_rect(arrow, dragon):
            score += 1
            reset_arrow()
            dragon.X -= 10

        # did dragon eat the player?
        if pygame.sprite.collide_rect(player, dragon):
            game_over= True

        # did you reach a score of 20?
        elif score == 20:
            you_win = True
            game_over = True

        # is the player jumping?
        if jumping:
            crouching = False
            player.Y += jump_vel
            jump_vel += 0.5
            if player.Y > player_start_y:
                jumping = False
                player.Y = player_start_y
                jump_vel = 0.0

        if crouching:
            jumping = False
            jump_vel = -8.0

        # draw the background
        screen.blit(bg, (0, 0))

        # update sprites
        if game_over == False:
            group.update(ticks, 50)

        # draw sprites
        group.draw(screen)

        draw_lives(lives)

        draw_score(score)

        print_text(font, 150, 510, "Press space to jump, and press midair to double jump!")
        print_text(font, 300, 540, "Press and hold C to crouch!")

        if game_over == True:
            print_text(display_font, 300, 100, "GAME OVER")
            if you_win:
                print_text(font, 280, 140, "YOU BEAT THE DRAGON!")
                play_again()
            else:
                print_text(font, 340, 140, "YOU LOST!")
                play_again()

        pygame.display.update()

while True:
    run_game()
