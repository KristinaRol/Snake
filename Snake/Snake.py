import pygame
import time

import classes

pygame.init()
pygame.mixer.init()

EVENT_FIRST_SONG_END = pygame.USEREVENT + 1
pixel_width = 32

MUSIC_VOLUME = 0.0

# All entities that are processed within one frame of the game,
# that is that they all implement the _process method

# List of all participating snakes
snakes = []
# List of all currently registered foods
foods = []

all_entities = []

replay_button = classes.Button(940,260,90,50, "replay")
replay_button.set_color((200,10,80))
two_player_button = classes.Button(940,200,90,50, "2 player")
buttons = [replay_button, two_player_button]
single_player = True
buttons = [two_player_button, replay_button]

stats = classes.Stats(snakes)

screenWidth = 1088
screenHeight = int(screenWidth * 9 / 16) # height 612
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake")

maximumFps = 60
gamestart = False

event_on_eat = classes.Event(classes.Food.move, "on_eat", foods)

def replay():
    start_game(1, 1)

def replay_two_player():
    start_game(2, 1)

# Resets the game with fiven snake num and food num
def start_game(snake_num, food_num):
    # setting globals
    global stats
    global snakes
    global foods
    global all_entities
    global gamestart

    gamestart = False

    
    # setting game entities
    snakes.clear()
    for i in range(snake_num):
        snakes.append(classes.Snake())
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

    # setting stats
    stats = classes.Stats(snakes)


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
    global buttons
    global single_player
    global gamestart
    run = True
    background = pygame.image.load(classes.IMG_PATH + 'background.png')
    last = pygame.time.get_ticks()

    pygame.mixer.music.load(classes.SOUND_PATH + 'music_start.ogg')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.set_endevent(EVENT_FIRST_SONG_END)
    pygame.mixer.music.queue(classes.SOUND_PATH + 'music_main.ogg')

    while run:
        pygame.time.wait(int(1000 / maximumFps))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == EVENT_FIRST_SONG_END:
                pygame.mixer.music.load(classes.SOUND_PATH + 'music_main.ogg')
                pygame.mixer.music.play(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    b.mouse_pressed(event.pos)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gamestart = True
            stats.start_time = time.time()
        if keys[pygame.K_r]:
            replay()
        if two_player_button.pressed:
            if single_player:
                replay_two_player()
                single_player = False
                two_player_button.set_color((0,200,0))
            else:
                replay()
                single_player = True
                two_player_button.set_color((200,0,0))
            two_player_button.pressed = False
        if replay_button.pressed:
            two_player_button.pressed = True
            replay_button.pressed = False
           

        window.blit(background, (0,0))

        # Collision algorithm
        for e in all_entities:
            cols = []
            for x in all_entities:
                if colliding(x, e):
                    cols.append(x)
            e._collide(cols)

        now = pygame.time.get_ticks()
        if snake_alive() and gamestart == True:
            for entity in all_entities:
                entity._process(now - last)
        if not(snake_alive()):
            window.fill([255,0,0])

        for button in buttons:
            button._process(now - last)


        all_entities = sorted(all_entities, key = lambda x: x.z_index)
        for entity in all_entities:
            entity._draw(window)
        for button in buttons:
            button._draw(window)

        pygame.display.update()
        last = pygame.time.get_ticks()


def snake_alive():
    global snakes

    tmp = True
    for s in snakes:
        tmp = tmp and s.alive
    return tmp

def set_multiplayer():
    global two_player_button 
    two_player_button.pressed = True
  
two_player_button.set_event(set_multiplayer)

def replay_func():
    global replay_button
    replay_button.pressed = True

replay_button.set_event(replay_func)


start_game(1, 1)
gameLoop()
pygame.quit()