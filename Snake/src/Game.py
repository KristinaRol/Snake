import pygame
import time
import random

import gamedef
import classes
import snake
import buttons
from enum import Enum

pygame.init()
pygame.mixer.init()


class Playmode(Enum):
    SINGLEPLAYER = 0
    MULT_SERVER = 1
    MULT_CLIENT = 2

# difficulty things
#---------------------------------------------
class Difstats:
    def __init__(self, b, m, f):
        self.base_speed = b
        self.modifier = m
        self.foods = f

class Difficulty(Enum):
    WARMUP = Difstats(200, 0.2, 1)
    EASY = Difstats(150, 0.4, 2)
    HARD = Difstats(100, 0.65, 3)
    CHAOTIC = Difstats(60, 0.9, 4)


# the setup
# --------------------------------------------------
difficulty = Difficulty.EASY
current_mode = Playmode.SINGLEPLAYER

pixel_width = 32
MUSIC_VOLUME = 0.1
snakes = []
foods = []
all_entities = []
btns = []
stats = classes.Stats(snakes)
screenWidth = 1088
screenHeight = int(screenWidth * 9 / 16)
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake")


def replay():
    start_game(len(snakes), len(foods))

def replay_two_player():
    start_game(2, len(foods))

def set_multiplayer():
    global snakes
    global foods
    if len(snakes) == 1:
        start_game(2, len(foods))
    else:
        start_game(1, len(foods))

def change_difficulty():
    global difficulty_button
    global difficulty
    global snakes

    if difficulty_button.state == 0:
        difficulty = Difficulty.WARMUP
    if difficulty_button.state == 1:
        difficulty = Difficulty.EASY
    if difficulty_button.state == 2:
        difficulty = Difficulty.HARD
    if difficulty_button.state == 3:
        difficulty = Difficulty.CHAOTIC

    play_music()
    start_game(len(snakes), difficulty.value.foods)

def setup():
    global current_mode
    global difficulty
    global MUSIC_VOLUME
    global pixel_width
    global snakes
    global foods
    global btns
    global maximumFps
    global all_entities
    global gamestart
    global stats
    global window
    global difficulty_button
    global two_player_button
    global replay_button 

    pixel_width = 32
    MUSIC_VOLUME = 0.1
    maximumFps = 120
    gamestart = False

    difficulty = Difficulty.EASY
    snakes = []
    foods = []
    all_entities = []
    stats = classes.Stats(snakes)

    replay_button = buttons.Button(940,260,90,50, "replay")
    replay_button.set_color((200,10,80))
    two_player_button = buttons.Switch(940,200,90,50, "2 player", 2)
    two_player_button.set_colors((200, 0, 0), (0, 200, 0))
    difficulty_button = buttons.Switch(940, 400, 96, 32, "", 4)
    difficulty_button.texture = pygame.image.load(gamedef.IMG_PATH + 'difficulty_buttons.png')
    difficulty_button.state = 1
    btns = [replay_button, two_player_button, difficulty_button]
    
    if current_mode == Playmode.SINGLEPLAYER:
        replay_button.set_event(replay)
        two_player_button.set_event(set_multiplayer)
        difficulty_button.set_event(change_difficulty)
      

def play_music():
    global difficulty

    pygame.mixer.music.stop()
    if difficulty == Difficulty.WARMUP:
        pygame.mixer.music.load(gamedef.SOUND_PATH + 'warmup_music.ogg')
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    if difficulty == Difficulty.EASY:
        pygame.mixer.music.load(gamedef.SOUND_PATH + 'music_main.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
    if difficulty == Difficulty.CHAOTIC:
        pygame.mixer.music.load(gamedef.SOUND_PATH + 'chaos_music.ogg')
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    if difficulty == Difficulty.HARD:
        pygame.mixer.music.load(gamedef.SOUND_PATH + 'hard_music.ogg')
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)


play_music()

# Resets the game with fiven snake num and food num
def start_game(snake_num, food_num):
    # setting globals
    global stats
    global snakes
    global foods
    global all_entities
    global gamestart
    global difficulty

    gamestart = False

    
    # setting game entities
    snakes.clear()
    for i in range(snake_num):
        snakes.append(snake.Snake())
    for s in snakes:
        s.current_sprite = random.randint(0,3)
        s.speed_base = difficulty.value.base_speed
        s.speed_modifier = difficulty.value.modifier
    
    foods.clear()
    for i in range(food_num):
        foods.append(classes.Food(snakes))
    

    # special setting for two player mode
    if snake_num == 2:
        snakes[1].all_positions = [(4 * pixel_width, 10 * pixel_width), (5 * pixel_width, 10 * pixel_width), (6 * pixel_width, 10 * pixel_width), (7 * pixel_width, 10 * pixel_width)]
        snakes[1].set_letter_keys()

    all_entities.clear()
    all_entities.extend(snakes)
    all_entities.extend(foods)

    # Make it so that food avoids every entitiy
    # that has collision enables
    for f in foods:
        f.entities = all_entities

    # setting stats
    stats = classes.Stats(snakes)
    all_entities.append(stats)


# checks whether the two game entities are colldiding
# and return True if so
def colliding(e, x):
    for i in range(len(e.all_positions)):
        for j in range(len(x.all_positions)):
        # When colliding with itself and the length of both obj is one
        # no collision shall be detected
            if (e == x and i == j and len(x.all_positions) > 1 and len(x.all_positions) > 1):
                continue;
        # if positions are equal then collision shall be detected
            if (e.all_positions[i] == x.all_positions[j]):
                return True

    return False


def gameLoop():
    global stats
    global food
    global all_entities
    global btns
    global gamestart
    run = True
    background = pygame.image.load(classes.IMG_PATH + 'background.png')
    
    now = pygame.time.get_ticks()
    last = pygame.time.get_ticks()

    

    while run:

        # framerate stabilization
        # makes the framerate now near to constant
        if last - now < int(1000 / maximumFps):
            pygame.time.wait(int(1000 / maximumFps) - (now - last))

       

        # Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for b in btns:
                    b.mouse_pressed(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for b in btns:
                    b.mouse_released()
        

        # when game is not started, get every key and start it when one is pressed
        if not gamestart:
            keys = pygame.key.get_pressed()
            for k in keys:
                if k:
                    gamestart = True
                    stats.start_time = time.time()
           
        # drawing background
        window.blit(background, (0,0))

        now = pygame.time.get_ticks()

        # Collision algorithm
        for e in all_entities:
            cols = []
            for x in all_entities:
                if colliding(x, e):
                    cols.append(x)
            e._collide(cols)

        
        if snake_alive() and gamestart == True:
            for entity in all_entities:
                entity._process(now - last)
        if not(snake_alive()):
            window.fill([255,0,0])

        for button in btns:
            button._process(now - last)

        all_entities = sorted(all_entities, key = lambda x: x.z_index)
        for entity in all_entities:
            entity._draw(window)
        for button in btns:
            button._draw(window)

        pygame.display.update()
        last = pygame.time.get_ticks()


def snake_alive():
    global snakes

    tmp = True
    for s in snakes:
        tmp = tmp and s.alive
    return tmp

setup()
start_game(1, 1)
gameLoop()
pygame.quit()