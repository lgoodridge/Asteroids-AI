"""
Defines utility function for the Asteroids game.
"""

import math

import pygame

from settings import get_settings

# Commonly used colors
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)
GREEN = (20, 200, 20)
RED = (200, 20, 20)
WHITE = (220, 220, 220)


def angle_to(comp1, comp2, handle_looping=True):
    """
    Returns the angle comp1 would have to face to move toward comp2.
    """
    return angle_to_xy(comp1.x, comp1.y, comp2.x, comp2.y, handle_looping)


def angle_to_xy(x1, y1, x2, y2, handle_looping=True):
    """
    Returns the angle between the pair of points.
    """
    if handle_looping:
        (x2, y2) = get_looped_point(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dx, -dy)


def distance_between(comp1, comp2, handle_looping=True):
    """
    Returns the distance between the two components.
    """
    return distance_between_xy(
        comp1.x, comp1.y, comp2.x, comp2.y, handle_looping
    )


def distance_between_xy(x1, y1, x2, y2, handle_looping=True):
    """
    Returns the distance between the pair of points.
    """
    if handle_looping:
        (x2, y2) = get_looped_point(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt((dx * dx) + (dy * dy))


def get_looped_point(x1, y1, x2, y2):
    """
    Returns the looped values of x2 and y2 relative to x1 and y1.
    """
    settings = get_settings()
    (looped_x2, looped_y2) = (x2, y2)
    screen_width = settings.WIDTH + (2.0 * settings.SCREEN_EDGE_THICKNESS)
    screen_height = settings.HEIGHT + (2.0 * settings.SCREEN_EDGE_THICKNESS)
    if (x2 - x1) > (screen_width / 2.0):
        looped_x2 = x2 - screen_width
    elif (x2 - x1) < -(screen_width / 2.0):
        looped_x2 = x2 + screen_width
    if (y2 - y1) > (screen_height / 2.0):
        looped_y2 = y2 - screen_height
    elif (y2 - y1) < -(screen_height / 2.0):
        looped_y2 = y2 - screen_height
    return (looped_x2, looped_y2)


def get_render_rect(x, y, radius):
    """
    Returns the screen rectangle that needs to be
    re-rendered, given a component's position and radius.
    """
    return pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)


def get_rotated_vertices(angles, x, y, radius, rotation):
    """
    Accepts a list of angles (in radians) corresponding to points
    on a circle, and returns a list of vertices derived from
    rotating and scaling that circle, and getting the points at
    those angles, with the circle centered on x, y.
    """
    return [
        (
            x + radius * math.sin(angle + rotation),
            y - radius * math.cos(angle + rotation),
        )
        for angle in angles
    ]


def has_collided(comp1, comp2):
    """
    Returns whether the two components have collided.
    """
    return distance_between(comp1, comp2) <= (comp1.radius + comp2.radius)


def render_on(foreground, background, x, y):
    """
    Draws the foreground surface onto the background
    surface, centered at position x, y. Returns the
    render rect of the surface.
    """
    render_rect = foreground.get_rect()
    render_rect = render_rect.move(
        x - render_rect.width / 2, y - render_rect.height / 2
    )
    background.blit(foreground, render_rect)
