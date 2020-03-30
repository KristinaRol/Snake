import itertools
import time
import pygame 
from enum import Enum
from random import randint

pixel_width = 32

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class DiagDir(Enum):
    NE = 0
    SE = 1
    SW = 2
    NW = 3


class GameEntity:
    def _process(self, delta):
        pass

    def _draw(self, window):
        pass


class Snake(GameEntity):

    snakesquare = pygame.image.load('img\snakeSquare.png')
    snakesquare2 = pygame.image.load('img\snakeSquare2.png')
    head = [pygame.image.load('img\headU.png'),pygame.image.load('img\headR.png'),pygame.image.load('img\headD.png'),pygame.image.load('img\headL.png')]
    head2 = [pygame.image.load('img\headU2.png'),pygame.image.load('img\headR2.png'),pygame.image.load('img\headD2.png'),pygame.image.load('img\headL2.png')]
    tail = [pygame.image.load('img\\tailU.png'),pygame.image.load('img\\tailR.png'),pygame.image.load('img\\tailD.png'),pygame.image.load('img\\tailL.png')]
    tail2 = [pygame.image.load('img\\tailU2.png'),pygame.image.load('img\\tailR2.png'),pygame.image.load('img\\tailD2.png'),pygame.image.load('img\\tailL2.png')]
    corner = [pygame.image.load('img\cornerNE.png'),pygame.image.load('img\cornerSE.png'),pygame.image.load('img\cornerSW.png'),pygame.image.load('img\cornerNW.png')]
    corner2 = [pygame.image.load('img\cornerNE2.png'),pygame.image.load('img\cornerSE2.png'),pygame.image.load('img\cornerSW2.png'),pygame.image.load('img\cornerNW2.png')]
    pygame.mixer.init()
    effect = pygame.mixer.Sound('sound\\eat.ogg')

    def __init__(self):
        self.alive = True
        self.length = 4
        self.direction = Direction.EAST
        self.direction_until_step = Direction.EAST
        self.time_between_move = 200
        self.time_until_move = 200
        self.z_index = 10
        self.all_positions = [(4 * pixel_width, 8 * pixel_width), (5 * pixel_width, 8 * pixel_width), (6 * pixel_width, 8 * pixel_width), (7 * pixel_width, 8 * pixel_width)]
        self.food = 0
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.other_snake = 0
        self.red = False


    def set_letter_keys(self):
        self.key_left = pygame.K_a
        self.key_right = pygame.K_d
        self.key_up = pygame.K_w
        self.key_down = pygame.K_s
        self.red = True


    def _process(self, delta):
        self.check_out_of_bounds()
        keys = pygame.key.get_pressed()

        if keys[self.key_left] and self.direction != Direction.EAST:
            self.direction_until_step = Direction.WEST
        elif keys[self.key_right] and self.direction != Direction.WEST:
            self.direction_until_step = Direction.EAST
        if keys[self.key_up] and self.direction != Direction.SOUTH:
            self.direction_until_step = Direction.NORTH
        elif keys[self.key_down] and self.direction != Direction.NORTH:
            self.direction_until_step = Direction.SOUTH

        self.time_between_move = 200 + self.length * 2.2
        self.time_until_move -= delta

        if self.time_until_move < 0:
            self.direction = self.direction_until_step
            self.move()
            self.time_until_move = self.time_between_move
      

    def _draw(self, window):
        head_dir = self.find_head_dir().value
        tial_dir = self.find_tail_dir().value

        for i in range(1,len(self.all_positions) - 1): # geht körperteil ohne schwanz & kopf durch
          if self.is_corner(i):
            corner_dir = self.find_corner_dir(i).value
            if self.red:
                window.blit(Snake.corner2[corner_dir], self.all_positions[i])
            else:
                window.blit(Snake.corner[corner_dir], self.all_positions[i])
          else:
            if self.red:
                window.blit(Snake.snakesquare2, self.all_positions[i])
            else:
                window.blit(Snake.snakesquare, self.all_positions[i])
        if self.red:
            window.blit(Snake.tail2[tial_dir], self.all_positions[0])
            window.blit(Snake.head2[head_dir], (self.all_positions[len(self.all_positions) - 1][0] - 9, self.all_positions[len(self.all_positions) - 1][1] - 9))
        else:
            window.blit(Snake.tail[tial_dir], self.all_positions[0])
            window.blit(Snake.head[head_dir], (self.all_positions[len(self.all_positions) - 1][0] - 9, self.all_positions[len(self.all_positions) - 1][1] - 9))


    def check_out_of_bounds(self):
        x = self.all_positions[-1][0]
        y = self.all_positions[-1][1]
        if x < 0 or y < 0 or x > 900 or y > 600:
            self.alive = False


    def find_head_dir(self):
        last = len(self.all_positions) - 1
        if self.all_positions[last][0] < self.all_positions[last - 1][0]:
            return Direction.EAST
        elif self.all_positions[last][0] > self.all_positions[last - 1][0]:
            return Direction.WEST
        elif self.all_positions[last][1] > self.all_positions[last - 1][1]:
            return Direction.NORTH
        else:
            return Direction.SOUTH


    def find_tail_dir(self):
        if self.all_positions[0][0] < self.all_positions[1][0]:
            return Direction.EAST
        elif self.all_positions[0][0] > self.all_positions[1][0]:
            return Direction.WEST
        elif self.all_positions[0][1] > self.all_positions[1][1]:
            return Direction.NORTH
        else:
            return Direction.SOUTH


    def is_corner(self, i):
        upper = self.all_positions[i][1] != self.all_positions[i + 1][1]
        lower = self.all_positions[i][1] != self.all_positions[i - 1][1]
        return lower != upper


    def find_corner_dir(self, i):
        upper = self.all_positions[i][1] > self.all_positions[i + 1][1] or self.all_positions[i][1] > self.all_positions[i - 1][1]
        lower = self.all_positions[i][1] < self.all_positions[i - 1][1] or self.all_positions[i][1] < self.all_positions[i + 1][1]
        right = self.all_positions[i][0] < self.all_positions[i + 1][0] or self.all_positions[i][0] < self.all_positions[i - 1][0]
        if right and upper and not(lower):
            return DiagDir.SW
        elif right and lower and not(upper):
            return DiagDir.NW
        elif upper and not(lower) and not(right):
            return DiagDir.SE
        else:
            return DiagDir.NE


    def move(self):
        if(self.ate_food()):
            self.food.move()
            Snake.effect.play()
            self.length+=1
        else:
            self.all_positions.pop(0)

        if self.direction == Direction.EAST:
            pos = (self.all_positions[-1][0] + pixel_width, self.all_positions[-1][1])
            self.check_position(pos)
        elif self.direction == Direction.WEST:
            pos = (self.all_positions[-1][0] - pixel_width, self.all_positions[-1][1])
            self.check_position(pos)
        elif self.direction == Direction.NORTH:
            pos = (self.all_positions[-1][0], self.all_positions[-1][1] - pixel_width)
            self.check_position(pos)
        else:
            pos = (self.all_positions[-1][0], self.all_positions[-1][1] + pixel_width)
            self.check_position(pos)


    def check_position(self, pos): # checks whether snake moved into itself
        if pos in self.all_positions or pos in self.other_snake.all_positions:
            self.alive = False
        else:
            self.all_positions.append(pos)

            
    def set_food(self, food):
        self.food = food


    def ate_food(self):
        # print(str(self.all_positions[-1]) + " " + str(self.food.position))
        return self.all_positions[-1] == self.food.position

        
    def die(self):
        self.alive = False


            


 #-------------------------------------------------------------------------------------------------------------------------------------

class Food(GameEntity):

    food = [pygame.image.load('img\\food1.png'),pygame.image.load('img\\food2.png'),pygame.image.load('img\\food3.png')]
    possible_positions = list(itertools.product(range(0,868,32), range(0,580,32)))


    def __init__(self, snake, snake2):
        self.snake = snake
        self.snake2 = snake2
        self.position = self.get_new_pos()
        self.fruit_sort = randint(0, 2)
        self.z_index = 8


    def _process(self, delta):
        pass


    def _draw(self, window):
        window.blit(Food.food[self.fruit_sort], self.position)


    def get_new_pos(self):
        valid_pos = list(itertools.filterfalse(lambda x: x in self.snake.all_positions or x in self.snake2.all_positions, Food.possible_positions))
        i = randint(0, len(valid_pos) - 1)
        return valid_pos[i]


    def move(self):
        self.position = self.get_new_pos()
        self.fruit_sort = randint(0, 2)

                 


 #-------------------------------------------------------------------------------------------------------------------------------------


class Stats(GameEntity):

    busch = pygame.image.load('img\\busch.png')
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    start_time = 0
    current_time = 0


    def __init__(self, snake, snake2):
        self.snake = snake
        self.snake2 = snake2
        self.length_snake = self.font.render("length 4", True, (0, 0, 0))
        self.length_snake2 = self.font.render("length 4", True, (0, 0, 0))
        self.z_index = 12


    def _process(self, delta):
        self.length_snake = self.font.render("length " + str(self.snake.length), True, (0, 0, 0))
        self.length_snake2 = self.font.render("length " + str(self.snake2.length), True, (0, 0, 0))


    def _draw(self, window):
        pygame.draw.rect(window,([99,154,103]),(900,0,1088 - 900,612))
        window.blit(Stats.busch, (880,0))
        window.blit(self.font.render("snake 1", True, (0, 0, 0)), (940, 40))
        window.blit(self.length_snake, (940, 60))
        if self.snake2.visible:
            window.blit(self.font.render("snake 2", True, (0, 0, 0)), (940, 100))
            window.blit(self.length_snake2, (940, 120))
        self.draw_time(window)


    def draw_time(self, window):
        if self.start_time == 0:
            window.blit(self.font.render("time: " + str(0.0), True, (0, 0, 0)), (940, 160))
        elif not(self.snake.alive) or not(self.snake2.alive):
            window.blit(self.font.render("time: " + ("%.2f" % (self.current_time - self.start_time)), True, (0, 0, 0)), (940, 160))
        else:
            self.current_time = time.time()
            window.blit(self.font.render("time: " + ("%.2f" % (self.current_time - self.start_time)), True, (0, 0, 0)), (940, 160))




class Button(GameEntity):

    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

    def __init__(self, x, y, width, height, str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.z_index = 20
        self.event = 0
        self.label = self.font.render(str, True, (0, 0, 0))
        self.color = (200,0,0)
        self.pressed = False
        self.visible = True

    def _process(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.contains(event.pos):
                    self.event()

    def _draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        window.blit(self.label, (self.x+5, self.y+15))

    def set_event(self, f):
        self.event = f

    def set_color(self,c):
        self.color = c

    def set_label(self, str):
        self.label = self.font.render(str, True, (0, 0, 0))

    def contains(self, pos):
        return pos[0] > self.x and pos[0] < self.x + self.width and pos[1] < self.y + self.height and pos[1] > self.y
            