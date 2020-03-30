import pygame
import itertools
import random
import time

import gamedef

IMG_PATH = gamedef.IMG_PATH

class Food(gamedef.GameEntity):

    food = [pygame.image.load(IMG_PATH + 'food1.png'),pygame.image.load(IMG_PATH + 'food2.png'),pygame.image.load(IMG_PATH + 'food3.png')]
    possible_positions = list(itertools.product(range(0,868,32), range(0,580,32)))


    def __init__(self, snakes):
        self.snakes = snakes
        self.position = self.get_new_pos()
        self.all_positions = [self.position]
        self.fruit_sort = random.randint(0, 2)
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
        i = random.randint(0, len(valid_pos) - 1)
        return valid_pos[i]

    def move(self):
        self.position = self.get_new_pos()
        self.all_positions = [self.position]
        self.fruit_sort = random.randint(0, 2)

class Stats(gamedef.GameEntity):

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
            window.blit(self.font.render("snake " + str(i + 1), True, (0, 0, 0)), (940, 40 + i * 60))
            window.blit(self.font.render("length " + str(self.snakes[i].length), True, (0, 0, 0)), (940, 60))
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

class Button(gamedef.GameEntity):

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
            