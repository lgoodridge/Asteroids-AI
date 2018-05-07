from asteroids.component import Component
from asteroids.utils import get_rotated_vertices, WHITE
import math
import pygame
import random

class Asteroid(Component):
    """
    Defines an in-game asteroid.
    """

    # The component radiuses for each asteroid size
    SIZE_TO_RADIUS = [0, 10, 20, 40]

    # The maximum speed for each asteroid size
    SIZE_TO_MAX_SPEED = [0, 1, 1.5, 2]

    # The maximum absolute rotation speed for an asteroid
    MAX_ROTATION_SPEED = 0.05

    # Possible asteroid shapes
    ASTEROID_SHAPES = [
       [math.pi/6, math.pi/3, 5*math.pi/8, 7*math.pi/8,
           5*math.pi/4, 3*math.pi/2, 7*math.pi/4],
       [math.pi/8, 3*math.pi/4, 7*math.pi/9, math.pi,
           3*math.pi/2, 13*math.pi/8, 15*math.pi/8],
       [0, math.pi/3, 7*math.pi/16, 3*math.pi/4, 15*math.pi/16,
           5*math.pi/4, 3*math.pi/2, 27*math.pi/16, 11*math.pi/6],
    ]

    def __init__(self, size, x, y, speed, angle,
            spin=None, shape=None, divot=None):
        super(Asteroid, self).__init__(Asteroid.SIZE_TO_RADIUS[size],
                x, y, speed, angle)
        self.speed = min(self.speed, Asteroid.SIZE_TO_MAX_SPEED[size])
        self._size = size
        self._rotation = 0
        self._spin = spin if spin is not None else random.uniform(
                -Asteroid.MAX_ROTATION_SPEED, Asteroid.MAX_ROTATION_SPEED)
        self._shape = shape if shape is not None else \
                random.randint(0, len(Asteroid.ASTEROID_SHAPES) - 1)
        self._divot = divot if divot is not None else \
                random.randint(-2, len(Asteroid.ASTEROID_SHAPES[self._shape]) - 1)

    def move(self):
        """
        Moves the asteroid, and accounts for rotation.
        """
        super(Asteroid, self).move()
        self._rotation = (self._rotation + self._spin) % (2 * math.pi)

    def draw(self, screen):
        """
        Draws the asteroid at its current location.
        """
        super(Asteroid, self).draw(screen)
        unrotated_angles = Asteroid.ASTEROID_SHAPES[self._shape]
        vertices = get_rotated_vertices(unrotated_angles,
                self.x, self.y, self.radius, self._rotation)
        if self._divot > 0:
            vertices = vertices[:self._divot] + [(self.x, self.y)] + \
                    vertices[self._divot:]
        pygame.draw.polygon(screen, WHITE, vertices, 1)

    def split(self, asteroids):
        """
        Splits the asteroid into two smaller asteroids if possible.
        Just destroys the asteroid if its at the minimum size.
        """
        self.destroyed = True
        if self._size > 1:
            asteroids.append(Asteroid(self._size-1, self.x, self.y, random.uniform(
                    self.speed, Asteroid.SIZE_TO_MAX_SPEED[self._size-1]),
                    (self.angle - random.uniform(0, math.pi/6)) % 2*math.pi))
            asteroids.append(Asteroid(self._size-1, self.x, self.y, random.uniform(
                    self.speed, Asteroid.SIZE_TO_MAX_SPEED[self._size-1]),
                    (self.angle + random.uniform(0, math.pi/6)) % 2*math.pi))
