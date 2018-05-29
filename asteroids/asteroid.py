from asteroids.component import Component
from asteroids.utils import angle_to_xy, get_rotated_vertices, WHITE
from asteroids.sound import play_sound
import math
import pygame
import random
import settings

class Asteroid(Component):
    """
    Defines an in-game asteroid.
    """

    # The component radiuses for each asteroid size
    SIZE_TO_RADIUS = [0, 10, 20, 40]

    # The maximum speed for each asteroid size
    SIZE_TO_MAX_SPEED = [0, 2, 1.5, 1]

    # The score for each asteroid size
    SIZE_TO_SCORE = [0, 4, 2, 1]

    # The "bang" sound for each asteroid size
    SIZE_TO_BANG_SOUND = ["", "bangSmall", "bangMedium", "bangLarge"]

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

    @staticmethod
    def spawn(asteroids, player, aimed, speed=None):
        """
        Spawns a new asteroid and adds it to the asteroids list.
        If aimed is True, the asteroid spawns moving in the
        direction of the player ship.
        """
        [NORTH, EAST, SOUTH, WEST] = range(4)

        # Get the possible spawn edges
        possible_spawn_edges = [NORTH, EAST, SOUTH, WEST]
        if player.y < settings.MIN_SPAWN_EDGE_DISTANCE:
            possible_spawn_edges.remove(NORTH)
        if player.y > settings.HEIGHT - settings.MIN_SPAWN_EDGE_DISTANCE:
            possible_spawn_edges.remove(SOUTH)
        if player.x < settings.MIN_SPAWN_EDGE_DISTANCE:
            possible_spawn_edges.remove(WEST)
        if player.x > settings.WIDTH - settings.MIN_SPAWN_EDGE_DISTANCE:
            possible_spawn_edges.remove(EAST)

        # Choose one of them, and a location on that edge
        spawn_edge = random.choice(possible_spawn_edges)
        if spawn_edge == NORTH:
            new_x = random.randint(0, settings.WIDTH)
            new_y = -settings.SCREEN_EDGE_THICKNESS
        elif spawn_edge == SOUTH:
            new_x = random.randint(0, settings.WIDTH)
            new_y = settings.HEIGHT + settings.SCREEN_EDGE_THICKNESS
        elif spawn_edge == WEST:
            new_x = -settings.SCREEN_EDGE_THICKNESS
            new_y = random.randint(0, settings.HEIGHT)
        elif spawn_edge == EAST:
            new_x = settings.WIDTH + settings.SCREEN_EDGE_THICKNESS
            new_y = random.randint(0, settings.HEIGHT)

        # Choose the angle (set toward the player if aimed)
        angle = angle_to_xy(new_x, new_y, player.x, player.y,
                handle_looping=False)
        if not aimed:
            angle += random.uniform(-math.pi/2, math.pi/2)

        # Choose the speed (set reasonably high if aimed)
        if speed is None:
            max_speed = Asteroid.SIZE_TO_MAX_SPEED[3]
            min_speed = 3 * max_speed / 4.0 if aimed else max_speed / 2.0
            speed = random.uniform(min_speed, max_speed)

        # Create the asteroid and add it to the provided list
        spawned_asteroid = Asteroid(3, new_x, new_y, speed, angle)
        asteroids.append(spawned_asteroid)

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
        play_sound(Asteroid.SIZE_TO_BANG_SOUND[self._size])

    def get_score(self):
        """
        Returns the score associated with shooting an asteroid.
        """
        return Asteroid.SIZE_TO_SCORE[self._size]
