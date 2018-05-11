"""
Defines settings for the Asteroids Game / AI.
"""

##################################################
#                  AI SETTINGS 
##################################################

# Who (or what) is playing the game
[HUMAN, AI] = range(2)
PLAYER_MODE = HUMAN

# Which AI brain to use
[SIMPLE] = range(1)
AI_BRAIN = SIMPLE

# Weights of each variable in the fitness function
FITNESS_SCORE_WEIGHT = 1.0
FITNESS_RUN_TIME_WEIGHT = 0.01

##################################################
#               CORE GAME SETTINGS 
##################################################

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# How "thick" the invisible edges of the screen are
SCREEN_EDGE_THICKNESS = 20

# Minimum distance the player has to be from an edge
# for an asteroid to potentially spawn from that edge
MIN_SPAWN_EDGE_DISTANCE = 200

# Time (in milliseconds) between asteroid spawns at game start
INITIAL_SPAWN_PERIOD = 5000

# How much the spawn period decreases with each spawn
SPAWN_PERIOD_DEC = 200

# Minimum time (in milliseconds) between asteroid spawns
MIN_SPAWN_PERIOD = 1000

# Game update speed limit (0 means no limit)
MAX_FPS = 60

##################################################
#               IN-GAME SETTINGS 
##################################################

# Whether debug mode is activated (player is invincible)
DEBUG_MODE = False

# Whether to show the collision boundary for components
SHOW_COLLISION_BOUNDARY = False

# Whether to show score in top left corner
SHOW_SCORE = True

# Whether to show FPS in bottom left corner
SHOW_FPS = True

# Whether to play sound effects
PLAY_SFX = True
