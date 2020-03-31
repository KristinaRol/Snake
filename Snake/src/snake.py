import gamedef
import pygame

IMG_PATH = gamedef.IMG_PATH
SOUND_PATH = gamedef.SOUND_PATH
pixel_width = gamedef.pixel_width

class Snake(gamedef.GameEntity):

    tiles_snake1 = pygame.image.load(IMG_PATH + 'snake.png')

    last_renderered_tile = -1

    pygame.mixer.init()
    effect = pygame.mixer.Sound(SOUND_PATH + 'eat.ogg')

    def __init__(self):
        Snake.last_renderered_tile += 1
        if (Snake.last_renderered_tile == 4):
            Snake.last_renderered_tile = 0
        self.current_sprite = Snake.last_renderered_tile

        self.alive = True
        self.length = 4
        self.direction = gamedef.Direction.EAST
        self.direction_until_step = gamedef.Direction.EAST
        self.time_between_move = 200
        self.time_until_move = 200
        self.z_index = 10
        self.has_eaten = False

        # the current sprite set to select
        self.current_sprite = 0

        # initializing position
        self.all_positions = [(4 * pixel_width, 8 * pixel_width), (5 * pixel_width, 8 * pixel_width), (6 * pixel_width, 8 * pixel_width), (7 * pixel_width, 8 * pixel_width)]

        # Setting keys
        self.keys = [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]

        # Calling super constructor
        super(Snake, self).__init__("snake")

    def set_letter_keys(self):
        self.keys[gamedef.Direction.WEST.value] = pygame.K_a
        self.keys[gamedef.Direction.EAST.value] = pygame.K_d
        self.keys[gamedef.Direction.NORTH.value] = pygame.K_w
        self.keys[gamedef.Direction.SOUTH.value] = pygame.K_s
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

        if keys[self.keys[gamedef.Direction.WEST.value]] and self.direction != gamedef.Direction.EAST:
            self.direction_until_step = gamedef.Direction.WEST
        elif keys[self.keys[gamedef.Direction.EAST.value]] and self.direction != gamedef.Direction.WEST:
            self.direction_until_step = gamedef.Direction.EAST
        if keys[self.keys[gamedef.Direction.NORTH.value]] and self.direction != gamedef.Direction.SOUTH:
            self.direction_until_step = gamedef.Direction.NORTH
        elif keys[self.keys[gamedef.Direction.SOUTH.value]] and self.direction != gamedef.Direction.NORTH:
            self.direction_until_step = gamedef.Direction.SOUTH

        self.time_between_move = 200 + self.length * 2.2
        self.time_until_move -= delta

        if self.time_until_move < 0:
            self.direction = self.direction_until_step
            self.move()
            self.time_until_move = self.time_between_move
      

    def _draw(self, window):      
        for i in range(len(self.all_positions)):
            self.draw_tile(i, window)     

    #drawm the tile ad index idx to the window
    def draw_tile(self, idx, window):

        # the coordinates within the picture
        x = 0
        y = 0

        # we are at the tail
        if idx == 0:
            if self.all_positions[1][0] > self.all_positions[idx][0]:
                x = 7
                y =  2 * self.current_sprite
            elif self.all_positions[1][0] < self.all_positions[idx][0]:
                x = 6
                y = 2 * self.current_sprite
            elif self.all_positions[1][1] > self.all_positions[idx][1]:
                x = 7
                y = 2 * self.current_sprite + 1
            elif self.all_positions[1][1] < self.all_positions[idx][1]:
                x = 6
                y = 2 * self.current_sprite + 1
        # we are at the head
        elif idx == len(self.all_positions) - 1:
            if self.all_positions[idx - 1][0] > self.all_positions[idx][0]:
                x = 5
                y = 2 * self.current_sprite
            elif self.all_positions[idx - 1][0] < self.all_positions[idx][0]:
                x = 5
                y = 2 * self.current_sprite + 1
            elif self.all_positions[idx - 1][1] > self.all_positions[idx][1]:
                x = 4
                y = 2 * self.current_sprite + 1
            elif self.all_positions[idx - 1][1] < self.all_positions[idx][1]:
                x = 4
                y = 2 * self.current_sprite
        else:
            # if we are in the middle
            if self.all_positions[idx][0] > self.all_positions[idx - 1][0]:
                if self.all_positions[idx + 1][0] > self.all_positions[idx][0]:
                    x = 0
                    y = 2 * self.current_sprite
                elif self.all_positions[idx + 1][1] > self.all_positions[idx][1]:
                    x = 2
                    y = 2 * self.current_sprite
                elif self.all_positions[idx + 1][1] < self.all_positions[idx][1]:
                    x = 3
                    y = 1 + 2 * self.current_sprite
            elif self.all_positions[idx][0] < self.all_positions[idx - 1][0]:
                if self.all_positions[idx + 1][0] < self.all_positions[idx][0]:
                    x = 1
                    y = 2 * self.current_sprite
                elif self.all_positions[idx + 1][1] > self.all_positions[idx][1]:
                    x = 3
                    y = 2 * self.current_sprite
                elif self.all_positions[idx + 1][1] < self.all_positions[idx][1]:
                    x = 2
                    y = 1 + 2 * self.current_sprite
            else:
                if self.all_positions[idx][1] > self.all_positions[idx - 1][1]:
                    if self.all_positions[idx][0] > self.all_positions[idx+1][0]:
                        x = 3
                        y = 2 * self.current_sprite + 1
                    elif self.all_positions[idx][0] < self.all_positions[idx+1][0]:
                        x = 2
                        y = 2 * self.current_sprite + 1
                    else:
                        x = 0
                        y = 1 + 2 * self.current_sprite
                else:
                   if self.all_positions[idx][0] > self.all_positions[idx+1][0]:
                        x = 2
                        y = 2 * self.current_sprite
                   elif self.all_positions[idx][0] < self.all_positions[idx+1][0]:
                       x = 3
                       y = 2 * self.current_sprite 
                       
                   else:
                        x = 1
                        y = 1 + 2 * self.current_sprite

        window.blit(self.tiles_snake1, self.all_positions[idx], (x * pixel_width, y * pixel_width, pixel_width, pixel_width))

    def check_out_of_bounds(self):
        x = self.all_positions[-1][0]
        y = self.all_positions[-1][1]
        if x < 0 or y < 0 or x > 900 or y > 600:
            self.alive = False

    # Called when the snake should move
    def move(self):
        if self.direction == gamedef.Direction.EAST:
            pos = (self.all_positions[-1][0] + pixel_width, self.all_positions[-1][1])
            self.all_positions.append(pos)
        elif self.direction == gamedef.Direction.WEST:
            pos = (self.all_positions[-1][0] - pixel_width, self.all_positions[-1][1])
            self.all_positions.append(pos)
        elif self.direction == gamedef.Direction.NORTH:
            pos = (self.all_positions[-1][0], self.all_positions[-1][1] - pixel_width)
            self.all_positions.append(pos)
        else:
            pos = (self.all_positions[-1][0], self.all_positions[-1][1] + pixel_width)
            self.all_positions.append(pos)

        
        if not self.has_eaten:
            self.all_positions.pop(0)
        else:
            self.has_eaten = False

    def die(self):
        self.alive = False