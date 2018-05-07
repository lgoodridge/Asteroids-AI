from asteroids.component import Component
import pygame

class Bullet(Component):
    """
    Defines an in-game bullet, shot by the player ship.
    """

    # The component characteristics of each bullet
    RADIUS = 3
    SPEED = 10

    # Maximum number of bullets that may be onscreen at once
    MAX_ONSCREEN_BULLETS = 4

    # Maximum number of steps a bullet will stay on screen
    MAX_LIFESPAN = 60

    def __init__(self, x, y, angle):
        super(Bullet, self).__init__(Bullet.RADIUS, x, y, Bullet.SPEED, angle)
        self._age = 0

    def draw(self, screen):
        """
        Draws the bullet at its current location.
        """
        super(Bullet, self).draw(screen)
        raise NotImplementedError()

    def increase_age(self):
        """
        Increments the bullet's age, destroying it
        if its reached its maximum lifespan.
        """
        raise NotImplementedError()

    def check_for_collisions(self, asteroids):
        """
        Checks for collisions with any asteroids, splitting the
        asteroid and destroying the bullet if one occurs.
        """
        raise NotImplementedError()
