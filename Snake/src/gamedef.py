import itertools
import time
import pygame 
from enum import Enum
from random import randint

pixel_width = 32

IMG_PATH ='img\\'  #'Snake\\img\\'
SOUND_PATH = 'sound\\'

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