"""
Defines settings for the Asteroids Game / AI.
"""

import os

##################################################
#                  AI SETTINGS
##################################################

# Whether we are playing the game or
# starting / continuing an experiment
[GAME, EXPERIMENT] = range(2)
RUN_MODE = GAME

# Who (or what) is playing the game
[HUMAN, AI] = range(2)
PLAYER_MODE = HUMAN

# Algorithm to use when an AI is playing the game
[SIMPLE] = range(1)
GAME_ALGORITHM_ID = SIMPLE

# Path to the AI brain to use when playing the game
GAME_AI_BRAIN = os.path.join("experiments", "simple", "_best.brn")

# Algorithm to use for the next experiment that is started
EXPERIMENT_ALGORITHM_ID = SIMPLE

# Path to the directory used by the experiment:
# If the directory contains the work of a previous experiment,
# it will be continued; otherwise a new experiment is started
EXPERIMENT_DIRECTORY = os.path.join("experiments", "simple")

# Whether to echo messages written to the
# experiment log to the console as well
EXPERIMENT_ECHO_LOGS = True

# Maximum number of generations to run the
# experiment for, if it doesn't get ended early
MAX_GENERATIONS = 100

# Minimum improvement in fitness needed between
# generations for us to consider it "progress"
PROGRESS_IMPROVEMENT_THRESHOLD = 50

# Maximum number of generations to wait without
# progress before ending the experiment early
MAX_GENERATIONS_WITHOUT_PROGRESS = 5

# Number of brains in each generation
GENERATION_POPULATION = 100

# Rate of chromosome mutations when
# breeding to create the next generation
MUTATION_RATE = 0.05

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
