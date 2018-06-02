from asteroids.component import Component
from asteroids.utils import has_collided, WHITE
import pygame

class Bullet(Component):
    """
    Defines an in-game bullet, shot by the player ship.
    """

    # The component characteristics of each bullet
    RADIUS = 3
    SPEED = 10

    # Maximum number of steps a bullet will stay on screen
    MAX_LIFESPAN = 40

    def __init__(self, x, y, angle):
        super(Bullet, self).__init__(Bullet.RADIUS, x, y, Bullet.SPEED, angle)
        self._age = 0

    def draw(self, screen):
        """
        Draws the bullet at its current location.
        """
        super(Bullet, self).draw(screen)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)),
                self.radius, 0)

    def increase_age(self):
        """
        Increments the bullet's age, destroying it
        if its reached its maximum lifespan.
        """
        self._age += 1
        if self._age > Bullet.MAX_LIFESPAN:
            self.destroyed = True

    def check_for_collisions(self, asteroids):
        """
        Checks whether the bullet has collided with any asteroids,
        splitting the asteroid, destroying the bullet, and returning
        the associated score if a collision occurs. Returns 0 otherwise.
        """
        if self.destroyed:
            return 0
        for asteroid in asteroids:
            if has_collided(self, asteroid):
                self.destroyed = True
                asteroid.split(asteroids)
                return asteroid.get_score()
        return 0
