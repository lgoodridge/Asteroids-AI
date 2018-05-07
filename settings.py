"""
Defines settings for the Asteroids Game / AI.
"""

# Who (or what) is playing the game
[HUMAN, AI] = range(2)
PLAYER_MODE = HUMAN

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# How "thick" the invisible edges of the screen are
SCREEN_EDGE_THICKNESS = 20

# Game update speed limit (0 means no limit)
MAX_FPS = 60

# Whether debug mode is activated (player is invincible)
DEBUG_MODE = False

# Whether to show FPS in bottom left corner
SHOW_FPS = True

# Whether to show the collision boundary for components
SHOW_COLLISION_BOUNDARY = False
