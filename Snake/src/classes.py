import pygame
import itertools
import random
import time
from enum import Enum

import gamedef

IMG_PATH = gamedef.IMG_PATH

# The rarity is a tuple where the first entry is the image y position
# and the sendond entry is the amount of food obtainable in this category
class Rarity(Enum):
    COMMON = (0, 3)
    UNCOMMON = (1, 1)
    SHINY = (2, 3)

class Food(gamedef.GameEntity):

    food = pygame.image.load(IMG_PATH + 'food.png')
    possible_positions = list(itertools.product(range(0,868,32), range(0,580,32)))


    def __init__(self, entities, rarity = Rarity.COMMON):
        # self.entities provides all entities that this food will avoid when spawned.
        # enteties with no collision will automatically be ignored
        self.entities = entities

        # positioning
        self.position = self.get_new_pos()
        self.all_positions = [self.position]

        # select food sort
        self.current_rarity = rarity
        self.fruit_sort = random.randint(0, rarity.value[1] - 1)

        self.z_index = 8
        super(Food, self).__init__("food")

    def _process(self, delta):
        pass


    def _draw(self, window):
        window.blit(Food.food, self.position, (self.fruit_sort * 32, self.current_rarity.value[0] * 32, 32, 32))

    def get_new_pos(self):
        all_pos = []
        for e in self.entities:
            all_pos.extend(e.all_positions)
        valid_pos = list(itertools.filterfalse(lambda x: x in all_pos, Food.possible_positions))
        i = random.randint(0, len(valid_pos) - 1)
        return valid_pos[i]

    def move(self):
        self.position = self.get_new_pos()
        self.all_positions = [self.position]
        self.fruit_sort = random.randint(0, self.current_rarity.value[1] - 1)

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
            window.blit(self.font.render("score " + str(self.snakes[i].score), True, (0, 0, 0)), (940, 60))
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


            