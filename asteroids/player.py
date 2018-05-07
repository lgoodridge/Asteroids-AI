from asteroids.component import Component

class Player(Component):
    """
    Defines the player ship.
    """

    # Radius of the player ship
    RADIUS = 10

    # Maximum speed of the player ship
    MAX_SPEED = 10

    # How much boosters will increase speed per step
    BOOSTER_ACCELERATION = 0.1

    # How many degrees (in radians) the ship rotates per step
    ROTATE_SPEED = 0.05

    # Possible spin directions
    COUNTER_CLOCKWISE, NO_SPIN, CLOCKWISE = [-1, 0, 1]

    def __init__(self, x, y):
        super(Player, self).__init__(Player.RADIUS, x, y, 0, 0)
        self.boosting = False
        self.spin = NO_SPIN

    def move(self):
        """
        Moves the player ship, and accounts for acceleration + rotation.
        """
        super(Player, self).move()
        new_speed = self.speed + BOOSTER_ACCELERATION * int(self.boosting)
        self.speed = min(new_speed, Player.MAX_SPEED)
        self.angle = self.spin * Player.ROTATE_SPEED

    def draw(self):
        """
        Draws the player ship at its current location.
        """
        super(Player, self).draw()
        raise NotImplementedError()

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
