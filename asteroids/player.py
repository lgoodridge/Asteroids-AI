import math

import pygame

from asteroids.bullet import Bullet
from asteroids.component import Component
from asteroids.sound import play_sound, stop_sound
from asteroids.utils import WHITE, get_rotated_vertices, has_collided
from settings import get_settings


class Player(Component):
    """
    Defines the player ship.
    """

    # Radius of the player ship
    RADIUS = 14

    # Maximum speed of the player ship
    MAX_SPEED = 10

    # How much boosters affect speed and angle per step
    BOOSTER_ACCELERATION = 0.1

    # How much speed decreases per step when not boosting
    DRAG_DECELERATION = 0.02

    # How many degrees (in radians) the ship rotates per step
    ROTATE_SPEED = 0.08

    # Possible spin directions
    COUNTER_CLOCKWISE, NO_SPIN, CLOCKWISE = [-1, 0, 1]

    # Maximum number of bullets that may be onscreen at once
    MAX_ONSCREEN_BULLETS = 4

    # Minimum number of frames between each shot
    RELOAD_TIME = 10

    def __init__(self, x, y):
        super(Player, self).__init__(Player.RADIUS, x, y, 0, 0)
        self.num_bullets_fired = 0
        self.rotation = 0
        self._boosting = False
        self._spin = Player.NO_SPIN
        self._remaining_reload_time = 0

    def move(self):
        """
        Moves the player ship, and accounts for acceleration + rotation.
        """
        super(Player, self).move()
        if self._boosting:
            new_vx = (self.speed * math.sin(self.angle)) + (
                Player.BOOSTER_ACCELERATION * math.sin(self.rotation)
            )
            new_vy = (self.speed * math.cos(self.angle)) + (
                Player.BOOSTER_ACCELERATION * math.cos(self.rotation)
            )
            new_speed = math.sqrt((new_vx * new_vx) + (new_vy * new_vy))
            new_angle = math.atan2(new_vx, new_vy)
        else:
            new_speed = self.speed - Player.DRAG_DECELERATION
            new_angle = self.angle
        self.speed = max(min(new_speed, Player.MAX_SPEED), 0)
        self.angle = new_angle % (2 * math.pi)
        self.rotation = (self.rotation + self._spin * Player.ROTATE_SPEED) % (
            2 * math.pi
        )

    def draw(self, screen):
        """
        Draws the player ship at its current location.
        """
        super(Player, self).draw(screen)
        unrotated_angles = [0, (3 * math.pi / 4), (5 * math.pi / 4)]
        vertices = get_rotated_vertices(
            unrotated_angles, self.x, self.y, self.radius, self.rotation
        )
        vertices = vertices[:2] + [(self.x, self.y)] + vertices[2:]
        pygame.draw.polygon(screen, WHITE, vertices, 1)

    def start_boosting(self):
        """
        Engages the ships boosters.
        """
        settings = get_settings()
        if not self._boosting and not settings.DISABLE_BOOSTING:
            self._boosting = True
            play_sound("thrust", -1)

    def stop_boosting(self):
        """
        Disengages the ship's boosters.
        """
        settings = get_settings()
        if self._boosting and not settings.ALWAYS_BOOSTING:
            self._boosting = False
            stop_sound("thrust", 400)

    def start_spinning(self, clockwise):
        """
        Starts spinning the ship. Spins clockwise if the
        provided argument is True, counter-clockwise otherwise.
        """
        direction = Player.CLOCKWISE if clockwise else Player.COUNTER_CLOCKWISE
        self._spin = direction

    def stop_spinning(self):
        """
        Stops spinning the ship.
        """
        self._spin = Player.NO_SPIN

    def shoot(self, bullets):
        """
        Shoots a bullet in the current direction if possible.
        """
        settings = get_settings()
        if (
            len(bullets) < Player.MAX_ONSCREEN_BULLETS
            and self._remaining_reload_time == 0
            and not settings.DISABLE_SHOOTING
        ):
            bullets.append(Bullet(self.x, self.y, self.rotation))
            self.num_bullets_fired += 1
            self._remaining_reload_time = Player.RELOAD_TIME
            play_sound("fire")

    def check_for_collisions(self, asteroids):
        """
        Returns whether the player ship has collided with
        any asteroids, destroying the player ship if so.
        """
        settings = get_settings()
        if self.destroyed or settings.DEBUG_MODE:
            return False
        for asteroid in asteroids:
            if has_collided(self, asteroid):
                self.destroyed = True
                stop_sound("thrust")
                play_sound("bangSmall")
                return True
        return False

    ##################################################
    #       TO BE IMPLEMENTED BY AI SUBCLASSES
    ##################################################

    def sense(self, asteroids, bullets):
        """
        Checks the state of the world, and returns a feature
        matrix to be used as input to the AI update function.
        """
        raise NotImplementedError("'sense' should only be called by AI_Player")

    def update(self, bullets, sensor_data):
        """
        Updates any time dependent player state, then runs
        the AI algorithm on sensor_data, and performs the
        appropiate actions in response.
        """
        settings = get_settings()
        if self._remaining_reload_time != 0:
            self._remaining_reload_time -= 1
        if settings.ALWAYS_BOOSTING and not self._boosting:
            self.start_boosting()
