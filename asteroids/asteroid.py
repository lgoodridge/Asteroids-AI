from asteroids.component import Component
import pygame

class Asteroid(Component):
    """
    Defines an in-game asteroid.
    """

    # The component radiuses for each asteroid size
    SIZE_TO_RADIUS = [0, 10, 20, 40]

    def __init__(self, size, x, y, speed, angle):
        super(Asteroid, self).__init__(Asteroid.SIZE_TO_RADIUS[size],
                x, y, speed, angle)
        self._size = size

    def draw(self, screen):
        """
        Draws the asteroid at its current location.
        """
        super(Asteroid, self).draw(screen)
        raise NotImplementedError()

    def split(self):
        """
        Splits the asteroid into two smaller asteroids if possible.
        Destroys the asteroid if its at the minimum size.
        """
        raise NotImplementedError()
