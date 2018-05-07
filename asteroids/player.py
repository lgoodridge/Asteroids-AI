from asteroids.component import Component
import math
import pygame

class Player(Component):
    """
    Defines the player ship.
    """

    # Radius of the player ship
    RADIUS = 14

    # Maximum speed of the player ship
    MAX_SPEED = 10

    # How much boosters will increase speed per step
    BOOSTER_ACCELERATION = 0.1

    # How much speed decreases per step when not boosting
    DRAG_DECELERATION = 0.02

    # How many degrees (in radians) the ship rotates per step
    ROTATE_SPEED = 0.05

    # Possible spin directions
    COUNTER_CLOCKWISE, NO_SPIN, CLOCKWISE = [-1, 0, 1]

    def __init__(self, x, y):
        super(Player, self).__init__(Player.RADIUS, x, y, 0, 0)
        self.boosting = False
        self.spin = Player.NO_SPIN

    def move(self):
        """
        Moves the player ship, and accounts for acceleration + rotation.
        """
        super(Player, self).move()
        if self.boosting:
            new_speed = self.speed + Player.BOOSTER_ACCELERATION
        else:
            new_speed = self.speed - Player.DRAG_DECELERATION
        self.speed = max(min(new_speed, Player.MAX_SPEED), 0)
        self.angle = (self.angle + self.spin * Player.ROTATE_SPEED) % (2*math.pi)

    def draw(self, screen):
        """
        Draws the player ship at its current location.
        """
        super(Player, self).draw(screen)
        unrotated_angles = [0, (3 * math.pi / 4), (5 * math.pi / 4)]
        vertices = [(self.x + self.radius * math.sin(p + self.angle),
                self.y - self.radius * math.cos(p + self.angle))
                for p in unrotated_angles]
        vertices = vertices[:2] + [(self.x, self.y)] + vertices[2:]
        pygame.draw.polygon(screen, (255, 255, 255), vertices, 1)

    def shoot(self, bullets):
        """
        Shoots a bullet in the current direction if possible.
        """
        raise NotImplementedError()

    def check_for_collisions(self, asteroids):
        """
        Checks for collisions with any asteroids,
        destoying the player ship if one occurs.
        """
        raise NotImplementedError()
