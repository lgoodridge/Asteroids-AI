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

##################################################
#         COMMAND LINE INTERFACE SUPPORT
##################################################

import click

@click.command()
@click.option("--run-mode", type=click.Choice(["game", "experiment"]),
        default=None, help="Whether to play the game, or run an experiment.")
@click.option("--player-mode", type=click.Choice(["human", "ai"]),
        default=None, help="Who (or what) is playing the game.")
@click.option("--game-algorithm-id", type=click.Choice(["simple"]),
        default=None, help="Algorithm to use when AI is playing the game.")
@click.option("--game-ai-brain", type=click.Path(exists=True),
        default=None, help="Path to AI brain to use when playing the game.")
@click.option("--experiment-algorithm-id", type=click.Choice(["simple"]),
        default=None, help="Algorithm to use for the next started experiment.")
@click.option("--experiment-directory", type=click.Path(exists=False),
        default=None, help="Path to the directory used by the experiment.")
@click.option("--experiment-echo-logs", type=click.Choice(["true", "false"]),
        default=None, help="Whether to echo messages for the log to console.")
@click.option("--max-generations", type=int,
        default=None, help="Max # generations to run the experiment for.")
@click.option("--progress-improvement-threshold", type=int,
        default=None, help="Minimum fitness improvement needed for progress.")
@click.option("--max-generations-without-progress", type=int,
        default=None, help="Max # generations to wait without progress.")
@click.option("--generation-population", type=int,
        default=None, help="Number of brains in each generation.")
@click.option("--mutation-rate", type=float,
        default=None, help="Mutation rate when breeding generations.")
@click.option("--fitness-score-weight", type=float,
        default=None, help="Weight of score in the fitness function.")
@click.option("--fitness-runtime-weight", type=float,
        default=None, help="Weight of runtime int he fitness function.")

def cli_configure_settings(run_mode, player_mode, game_algorithm_id,
        game_ai_brain, experiment_algorithm_id, experiment_directory,
        experiment_echo_logs, max_generations, progress_improvement_threshold,
        max_generations_without_progress, generation_population, mutation_rate,
        fitness_score_weight, fitness_runtime_weight):
    """
    Configures settings according to the command line arguments.

    NOTE: To support a new setting, add it to the click options above,
        the method arguments, the list of gloval variables, and the
        code block in the method body.

    EXTRA NOTE: Currently investigating other ways of doing this that
        doesn't involve this massive click method...
    """
    global RUN_MODE, PLAYER_MODE, GAME_ALGORITHM_ID, GAME_AI_BRAIN, \
            EXPERIMENT_ALGORITHM_ID, EXPERIMENT_DIRECTORY, EXPERIMENT_ECHO_LOGS, \
            MAX_GENERATIONS, PROGRESS_IMPROVEMENT_THRESHOLD, \
            MAX_GENERATIONS_WITHOUT_PROGRESS, GENERATION_POPULATION, \
            MUTATION_RATE, FITNESS_SCORE_WEIGHT, FITNESS_RUNTIME_WEIGHT
    if run_mode is not None:
        RUN_MODE = {"game": GAME, "experiment": EXPERIMENT}[run_mode]
    if player_mode is not None:
        PLAYER_MODE = {"human": HUMAN, "ai": AI}[player_mode]
    if game_algorithm_id is not None:
        GAME_ALGORITHM_ID = {"simple": SIMPLE}[game_algorithm_id]
    if game_ai_brain is not None:
        GAME_AI_BRAIN = game_ai_brain
    if experiment_algorithm_id is not None:
        EXPERIMENT_ALGORITHM_ID = {"simple": SIMPLE}[experiment_algorithm_id]
    if experiment_directory is not None:
        EXPERIMENT_DIRECTORY = experiment_directory
    if experiment_echo_logs is not None:
        EXPERIMENT_ECHO_LOGS = {"true": True, "false": False}[experiment_echo_logs]
    if max_generations is not None:
        MAX_GENERATIONS = max_generations
    if progress_improvement_threshold is not None:
        PROGRESS_IMPROVEMENT_THRESHOLD = progress_improvement_threshold
    if max_generations_without_progress is not None:
        MAX_GENERATIONS_WITHOUT_PROGRESS = max_generations_without_progress
    if generation_population is not None:
        GENERATION_POPULATION = generation_population
    if mutation_rate is not None:
        MUTATION_RATE = mutation_rate
    if fitness_score_weight is not None:
        FITNESS_SCORE_WEIGHT = fitness_score_weight
    if fitness_runtime_weight is not None:
        FITNESS_RUNTIME_WEIGHT = fitness_runtime_weight
