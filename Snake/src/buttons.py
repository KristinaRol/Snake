import gamedef
import pygame

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
        super(Button, self).__init__("button", False)

    def _process(self, delta):
        pass

    # Is called before the event is called
    def _press(self):
        pass

    # Called whenever the mouse button is pressed
    def mouse_pressed(self, mouse_pos):
        if (self.contains(mouse_pos)):
            self._press()
            self.event()
            self.pressed = True

    # Called whenever the mouse button is released
    def mouse_released(self):
        if self.pressed:
            self.pressed = False

    def _draw(self, window):
        # drawing texture if there was set one
        if hasattr(self, "texture"):
            window.blit(self.texture, (self.x, self.y) )
        else:
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


class Switch(Button):
    def __init__(self, x, y, width, height, str, amount_of_states):
        self.state = 0
        self.amount_of_states = amount_of_states
        super().__init__(x, y, width, height, str)

    def set_colors(self, *colors):
        assert(self.amount_of_states == len(colors))
        self.colors = colors

    def _draw(self, window):
        if hasattr(self, "texture"):
            window.blit(self.texture, (self.x, self.y), (0, self.height * self.state, self.width, self.height))
        else:
            pygame.draw.rect(window, self.colors[self.state], (self.x, self.y, self.width, self.height))
        window.blit(self.label, (self.x+5, self.y+15))

    def _press(self):
        self.state += 1
        if self.state == self.amount_of_states:
            self.state = 0