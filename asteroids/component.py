from asteroids.utils import get_render_rect, GREEN, RED
import math
import pygame
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
        self.x += self.speed * math.sin(self.angle)
        self.y += self.speed * -math.cos(self.angle)
        self._wrap_screen_bounds()

    def draw(self, screen):
        """
        Draws the component at its current position.
        Draws a circle around the collision boundary
        of the component if specified in settings.
        """
        if settings.DEBUG_MODE:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)),
                    self.radius, 1)
        elif settings.SHOW_COLLISION_BOUNDARY:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)),
                    self.radius, 1)

    def add_render_rects(self, rects):
        """
        Adds the render rects for the component's current and
        previous positions to the provided rectangle list.
        """
        rects.append(get_render_rect(self.x, self.y, self.radius))
        rects.append(get_render_rect(self.prevX, self.prevY, self.radius))

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
