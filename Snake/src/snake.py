import gamedef
import pygame

IMG_PATH = gamedef.IMG_PATH
SOUND_PATH = gamedef.SOUND_PATH
pixel_width = gamedef.pixel_width

class Snake(gamedef.GameEntity):

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
        self.direction = gamedef.Direction.EAST
        self.direction_until_step = gamedef.Direction.EAST
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
        head_dir = self.find_head_dir().value
        tial_dir = self.find_tail_dir().value

        for i in range(1,len(self.all_positions) - 1): # geht k�rperteil ohne schwanz & kopf durch
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
            return gamedef.Direction.EAST
        elif self.all_positions[last][0] > self.all_positions[last - 1][0]:
            return gamedef.Direction.WEST
        elif self.all_positions[last][1] > self.all_positions[last - 1][1]:
            return gamedef.Direction.NORTH
        else:
            return gamedef.Direction.SOUTH


    def find_tail_dir(self):
        if self.all_positions[0][0] < self.all_positions[1][0]:
            return gamedef.Direction.EAST
        elif self.all_positions[0][0] > self.all_positions[1][0]:
            return gamedef.Direction.WEST
        elif self.all_positions[0][1] > self.all_positions[1][1]:
            return gamedef.Direction.NORTH
        else:
            return gamedef.Direction.SOUTH


    def is_corner(self, i):
        upper = self.all_positions[i][1] != self.all_positions[i + 1][1]
        lower = self.all_positions[i][1] != self.all_positions[i - 1][1]
        return lower != upper


    def find_corner_dir(self, i):
        upper = self.all_positions[i][1] > self.all_positions[i + 1][1] or self.all_positions[i][1] > self.all_positions[i - 1][1]
        lower = self.all_positions[i][1] < self.all_positions[i - 1][1] or self.all_positions[i][1] < self.all_positions[i + 1][1]
        right = self.all_positions[i][0] < self.all_positions[i + 1][0] or self.all_positions[i][0] < self.all_positions[i - 1][0]
        if right and upper and not(lower):
            return gamedef.DiagDir.SW
        elif right and lower and not(upper):
            return gamedef.DiagDir.NW
        elif upper and not(lower) and not(right):
            return gamedef.DiagDir.SE
        else:
            return gamedef.DiagDir.NE

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
        
    def set_food(self, food):
        self.food = food


    def die(self):
        self.alive = False