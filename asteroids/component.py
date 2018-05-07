import math
import settings

class Component(object):
    """
    Base class for all Game Components that appear on screen.
    """

    def __init__(self, radius, x, y, speed, angle):
        self.radius = radius
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.speed = speed
        self.angle = angle
        self.destroyed = False

    def move(self):
        """
        Updates the component's position according to its speed and angle.
        """
        self.prevX = self.x
        self.prevY = self.y
        self.x = self.speed * math.sin(angle)
        self.y = self.speed * math.cos(angle)
        self._wrap_screen_bounds()

    def draw(self):
        """
        Draws the component at its current position.
        """
        pass

    def _wrap_screen_bounds(self):
        """
        If the component is out of the screen bounds, wrap it to other side.
        """
        if self.x < -settings.SCREEN_EDGE_THICKNESS:
            self.x = settings.WIDTH + settings.SCREEN_EDGE_THICKNESS
        if self.x > settings.WIDTH + settings.SCREEN_EDGE_THICKNESS:
            self.x = -settings.SCREEN_EDGE_THICKNESS
        if self.y < -settings.SCREEN_EDGE_THICKNESS:
            self.y = settings.HEIGHT + settings.SCREEN_EDGE_THICKNESS
        if self.y > settings.HEIGHT + settings.SCREEN_EDGE_THICKNESS:
            self.y = -settings.SCREEN_EDGE_THICKNESS
