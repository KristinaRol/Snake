import itertools
import time
import pygame 
from enum import Enum
from random import randint

pixel_width = 32

IMG_PATH = 'Snake\\img\\'
SOUND_PATH = 'Snake\\sound\\'

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

# Generel purpouse GameEntity class provided to the Game screen
class GameEntity:
    def __init__(self, entity_name, reload_on_restart = True):
        # Collision queue and detection values
        self.col = False
        self.colliding_with = 0

        self.z_index = 0
        self.name = entity_name

        # all positions for this entity.
        # if no collision has to be checked this should be empty
        # when no all_positions was defined this is empty by default
        if not hasattr(self, 'all_positions'):
            self.all_positions = []
    

        # determines whether this entity should be removed from the
        # process queue when not used
        self.reload_on_restart = reload_on_restart

        # All events currently in this game entity
        # An event may be accessed from this map via its name
        self.all_events = {}
    
    # adds an event to the entity.
    # this is a method of event handling within an entity, although not nessecery
    def add_event(self, event):
        self.all_events[event.name] = event

    # Called every frame to move the entity
    def _process(self, delta):
        pass

    # Called every frame to draw the entity
    def _draw(self, window):
        pass

    # Called whenever this object intersects with another at some point
    # An object can also intersect withit self
    # the object that it intersects with is given in the 'obj' parameter
    # When no objects is empty no collision occured
    #
    # !!! DISCLAIMER !!!
    # This method should ALWAYS BE OVERRIDEN
    #
    def _collide(self, objects):
        if len(objects) == 0:
            self.col = False
        else:
            self.col = True
        self.colliding_with = objects

    # Returns whether this object collided with something this frame
    def colliding(self):
        return self.col

    # Removes one element of the currently pending colliding queue 
    def get_collision_object(self):
        obj = self.colliding_with[0]
        self.colliding_with.remove(obj)
        return obj
    
    # Gets all detected collision objects and removes them from the queue
    def get_all_collisions(self):
        obj = self.colliding_with
        self.colliding_with.clear()
        return obj
        

# Abstractation class for event processing that takes place between different entities
class Event:
    # All ids of currently registered events
    all_events = {}

    # initializes an event with a set goal function and the next id
    # you can receive the id just via its property "id"
    # when triggered the event will be called on all goal_entities
    def __init__(self, goal_func, name = "", goal_entities = []):
        self.goal_func = goal_func
        if name == "":
            self.name = "id_" + self.id
        else:
            self.name = name
        self.goal_entities = goal_entities
        Event.all_events[self.name] = self

    # Triggers this event with given params on all goal entities
    def trigger(self, *args):
        l = list(args)
        if self.goal_entities == []:
            self.goal_func(*l)
        else:
            for e in self.goal_entities:
                self.goal_func(e, *l)
        
    # Triggers the event with given id and given parameters
    def trigger_event(name, *params):
        Event.all_events[name].trigger(*params)

class Snake(GameEntity):

    snakesquare = pygame.image.load(IMG_PATH + 'snakeSquare.png')
    snakesquare2 = pygame.image.load(IMG_PATH + 'snakeSquare2.png')
    head = [pygame.image.load(IMG_PATH + 'headU.png'),pygame.image.load(IMG_PATH + 'headR.png'),pygame.image.load(IMG_PATH + 'headD.png'),pygame.image.load(IMG_PATH + 'headL.png')]
    head2 = [pygame.image.load(IMG_PATH + 'headU2.png'),pygame.image.load(IMG_PATH + 'headR2.png'),pygame.image.load(IMG_PATH + 'headD2.png'),pygame.image.load(IMG_PATH + 'headL2.png')]
    tail = [pygame.image.load(IMG_PATH + 'tailU.png'),pygame.image.load(IMG_PATH + 'tailR.png'),pygame.image.load(IMG_PATH + 'tailD.png'),pygame.image.load(IMG_PATH + 'tailL.png')]
    tail2 = [pygame.image.load(IMG_PATH + 'tailU2.png'),pygame.image.load(IMG_PATH + 'tailR2.png'),pygame.image.load(IMG_PATH + 'tailD2.png'),pygame.image.load(IMG_PATH + 'tailL2.png')]
    corner = [pygame.image.load(IMG_PATH + 'cornerNE.png'),pygame.image.load(IMG_PATH + 'cornerSE.png'),pygame.image.load(IMG_PATH + 'cornerSW.png'),pygame.image.load(IMG_PATH + 'cornerNW.png')]
    corner2 = [pygame.image.load(IMG_PATH + 'cornerNE2.png'),pygame.image.load(IMG_PATH + 'cornerSE2.png'),pygame.image.load(IMG_PATH + 'cornerSW2.png'),pygame.image.load(IMG_PATH + 'cornerNW2.png')]
    pygame.mixer.init()
    effect = pygame.mixer.Sound(SOUND_PATH + 'eat.ogg')

    def __init__(self):
        self.alive = True
        self.length = 4
        self.direction = Direction.EAST
        self.direction_until_step = Direction.EAST
        self.time_between_move = 200
        self.time_until_move = 200
        self.z_index = 10
        self.has_eaten = False

        # initializing position
        self.all_positions = [(4 * pixel_width, 8 * pixel_width), (5 * pixel_width, 8 * pixel_width), (6 * pixel_width, 8 * pixel_width), (7 * pixel_width, 8 * pixel_width)]

        # Setting keys
        self.keys = [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]

        #whatever this is, i figured it out it will fall like sparta
        self.red = False

        # Calling super constructor
        super(Snake, self).__init__("snake")

    def set_letter_keys(self):
        self.keys[Direction.WEST] = pygame.K_a
        self.keys[Direction.EAST] = pygame.K_d
        self.keys[Direction.NORTH] = pygame.K_w
        self.keys[Direction.SOUTH] = pygame.K_s
        self.red = True


    def _process(self, delta):

        # assuming only one collision took place
        # when collided with snake die,
        # when collided with food eat
        if self.colliding():
            col = self.get_collision_object()
            if col.name == "snake":
                self.die()
            if col.name == "food":
                col.move()
                Snake.effect.play()
                self.length+=1
                self.has_eaten = True


        self.check_out_of_bounds()
        keys = pygame.key.get_pressed()

        if keys[self.keys[Direction.WEST.value]] and self.direction != Direction.EAST:
            self.direction_until_step = Direction.WEST
        elif keys[self.keys[Direction.EAST.value]] and self.direction != Direction.WEST:
            self.direction_until_step = Direction.EAST
        if keys[self.keys[Direction.NORTH.value]] and self.direction != Direction.SOUTH:
            self.direction_until_step = Direction.NORTH
        elif keys[self.keys[Direction.SOUTH.value]] and self.direction != Direction.NORTH:
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

    # Called when the snake should move
    def move(self):
        if self.direction == Direction.EAST:
            pos = (self.all_positions[-1][0] + pixel_width, self.all_positions[-1][1])
            self.all_positions.append(pos)
        elif self.direction == Direction.WEST:
            pos = (self.all_positions[-1][0] - pixel_width, self.all_positions[-1][1])
            self.all_positions.append(pos)
        elif self.direction == Direction.NORTH:
            pos = (self.all_positions[-1][0], self.all_positions[-1][1] - pixel_width)
            self.all_positions.append(pos)
        else:
            pos = (self.all_positions[-1][0], self.all_positions[-1][1] + pixel_width)
            self.all_positions.append(pos)

        
        if not self.has_eaten:
            self.all_positions.pop(0)
        else:
            self.has_eaten = False
        
    def set_food(self, food):
        self.food = food


    def die(self):
        self.alive = False


 #-------------------------------------------------------------------------------------------------------------------------------------

class Food(GameEntity):

    food = [pygame.image.load(IMG_PATH + 'food1.png'),pygame.image.load(IMG_PATH + 'food2.png'),pygame.image.load(IMG_PATH + 'food3.png')]
    possible_positions = list(itertools.product(range(0,868,32), range(0,580,32)))


    def __init__(self, snakes):
        self.snakes = snakes
        self.position = self.get_new_pos()
        self.all_positions = [self.position]
        self.fruit_sort = randint(0, 2)
        self.z_index = 8
        super(Food, self).__init__("food")


    def _process(self, delta):
        pass


    def _draw(self, window):
        window.blit(Food.food[self.fruit_sort], self.position, (0, 0, 32, 32))


    def get_new_pos(self):
        all_pos = []
        for s in self.snakes:
            all_pos.extend(s.all_positions)
        valid_pos = list(itertools.filterfalse(lambda x: x in all_pos, Food.possible_positions))
        i = randint(0, len(valid_pos) - 1)
        return valid_pos[i]

    def move(self):
        self.position = self.get_new_pos()
        self.all_positions = [self.position]
        self.fruit_sort = randint(0, 2)

                 


 #-------------------------------------------------------------------------------------------------------------------------------------


class Stats(GameEntity):

    busch = pygame.image.load(IMG_PATH + 'busch.png')
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    start_time = 0
    current_time = 0

    def __init__(self, snakes):
        self.snakes = snakes
        self.length_snake = self.font.render("length 4", True, (0, 0, 0))
        self.length_snake2 = self.font.render("length 4", True, (0, 0, 0))
        self.z_index = 12
        super(Stats, self).__init__("stats", False)

    def _process(self, delta):
        pass


    def _draw(self, window):
        pygame.draw.rect(window,([99,154,103]),(900,0,1088 - 900,612))
        window.blit(Stats.busch, (880,0))
        for i in range(len(self.snakes)):
            window.blit(self.font.render("snake " + (i + 1), True, (0, 0, 0)), (940, 40 + i * 60))
            window.blit(self.font.render("length " + str(self.snake[i].length), True, (0, 0, 0)), (940, 60))
        self.draw_time(window)


    def draw_time(self, window):
        tmp = True
        for s in self.snakes:
            tmp = tmp and s.alive
        if self.start_time == 0:
            window.blit(self.font.render("time: " + str(0.0), True, (0, 0, 0)), (940, 160))
        elif not tmp:
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
        super(Button, self).__init__("button", False)

    def _process(self, delta):
        pass

    def mouse_pressed(self, mouse_pos):
        if (self.contains(mouse_pos)):
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
            