"""
Defines asteroid sensing functions to be used by AI players.
"""

from asteroids.utils import angle_to_xy, \
        distance_between_xy, LINEAR, HYPERBOLIC
import math

def sense_eight_dir(player, asteroids, max_distance, shape=LINEAR):
    """
    Looks in eight directions and returns an array containing
    how close the nearest asteroid is for each direction.

    The returned array contains values between 0 and 1, with
    0 indicating there are no asteroids within max_distance,
    and 1 indicating that the asteroid has collided with the
    player ship.

    shape dictates the shape of output response vs. distance:
        LINEAR: Increases linearly with decreasing distance
        HYPERBOLIC: Output has shape 1/distance
    """
    distances = [0.0] * 8
    for asteroid in asteroids:
        distance = distance_between_xy(player.x, player.y, asteroid.x,
                asteroid.y) - (asteroid.radius + player.radius)
        if distance > max_distance:
            continue
        distance = max(distance, 1.0)
        angle = (angle_to_xy(player.x, player.y, asteroid.x,
                asteroid.y) - player.rotation) % (2 * math.pi)
        closest_direction = int((angle + (math.pi / 8.0)) / (math.pi / 4.0)) % 8
        if shape == LINEAR:
            distances[closest_direction] = max(1 - distance/max_distance,
                    distances[closest_direction])
        elif shape == HYPERBOLIC:
            distances[closest_direction] = max(1.0/distance,
                    distances[closest_direction])
        else:
            raise RuntimeError("Programmer Error: Unsupported shape %d" % shape)
    return distances
