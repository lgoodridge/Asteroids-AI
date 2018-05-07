"""
Defines utility function for the Asteroids game.
"""

import pygame

# Commonly used colors
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)
WHITE = (220, 220, 220)

def render_on(foreground, background, x, y):
    """
    Draws the foreground surface onto the background
    surface, centered at position x, y. Returns the
    render rect of the surface.
    """
    render_rect = foreground.get_rect()
    render_rect = render_rect.move(x - render_rect.width/2,
            y - render_rect.height/2)
    background.blit(foreground, render_rect)

def get_render_rect(x, y, radius):
    """
    Returns the screen rectangle that needs to be
    re-rendered, given a component's position and radius.
    """
    return pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
