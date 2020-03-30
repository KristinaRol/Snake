import pygame
import classes
import time
pygame.init()
pygame.mixer.init()

EVENT_FIRST_SONG_END = pygame.USEREVENT + 1
pixel_width = 32

# All entities that are processed within one frame of the game,
# that is that they all implement the _process method
snake = classes.Snake()
snake2 = classes.Snake()
snake2.visible = False
stats = classes.Stats(snake, snake2)
food = classes.Food(snake, snake2)
snake.set_food(food)
snake2.set_food(food)
snake.other_snake = snake2
snake2.other_snake = snake
all_entities = [snake, food, stats]

replay_button = classes.Button(940,260,90,50, "replay")
replay_button.set_color((200,10,80))
two_player_button = classes.Button(940,200,90,50, "2 player")
single_player = True
buttons = [two_player_button, replay_button]

screenWidth = 1088
screenHeight = int(screenWidth * 9 / 16) # height 612
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake")

maximumFps = 60
gamestart = False

event_on_eat = classes.event(move, "on_eat", [food])

def gameLoop():
    global snake
    global snake2
    global stats
    global food
    global all_entities
    global buttons
    global single_player
    global gamestart
    run = True
    background = pygame.image.load('img\\background.png')
    last = pygame.time.get_ticks()

    pygame.mixer.music.load('sound\\music_start.ogg')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.set_endevent(EVENT_FIRST_SONG_END)
    pygame.mixer.music.queue('sound\\music_main.ogg')

    while run:
        pygame.time.wait(int(1000 / maximumFps))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == EVENT_FIRST_SONG_END:
                pygame.mixer.music.load('sound\\music_main.ogg')
                pygame.mixer.music.play(-1)
        
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
    global snake
    global single_player
    global snake2
    if single_player:
        return snake.alive
    else:
        return snake.alive and snake2.alive


def replay():
    global gamestart
    global snake
    global snake2
    global stats
    global food
    global all_entities
    gamestart = False
    snake = classes.Snake()
    snake2.visible = False
    stats = classes.Stats(snake, snake2)
    food = classes.Food(snake, snake2)
    snake.set_food(food)
    snake.other_snake = snake2
    snake2.other_snake = snake
    all_entities = [snake, food, stats]


def replay_two_player():
    global gamestart
    global snake
    global snake2
    global stats
    global food
    global all_entities
    gamestart = False
    snake = classes.Snake()
    snake2 = classes.Snake()
    snake2.visible = True
    snake2.set_letter_keys()
    snake2.all_positions = [(4 * pixel_width, 10 * pixel_width), (5 * pixel_width, 10 * pixel_width), (6 * pixel_width, 10 * pixel_width), (7 * pixel_width, 10 * pixel_width)]
    stats = classes.Stats(snake, snake2)
    food = classes.Food(snake, snake2)
    snake.set_food(food)
    snake2.set_food(food)
    snake.other_snake = snake2
    snake2.other_snake = snake
    all_entities = [snake, snake2, food, stats]

def set_multiplayer():
    global two_player_button 
    two_player_button.pressed = True
  
two_player_button.set_event(set_multiplayer)

def replay_func():
    global replay_button
    replay_button.pressed = True

replay_button.set_event(replay_func)



gameLoop()
pygame.quit()