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
[SIMPLE, NN] = range(2)
GAME_ALGORITHM_ID = SIMPLE

# Path to the AI brain to use when playing the game
GAME_AI_BRAIN = os.path.join("experiments", "simple", "_best.brn")

# Algorithm to use for the next experiment that is started
EXPERIMENT_ALGORITHM_ID = SIMPLE

# Path to the directory used by the experiment:
# If the directory contains the work of a previous experiment,
# it will be continued; otherwise a new experiment is started
EXPERIMENT_DIRECTORY = os.path.join("experiments", "default")

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

# Percentage of the current generation to
# keep when breeding the next generation
GENERATION_SURVIVOR_RATE = 0.25

# Rate of chromosome mutations when
# breeding to create the next generation
MUTATION_RATE = 0.05

# Weights of each variable in the fitness function
FITNESS_SCORE_WEIGHT = 1.0
FITNESS_ACCURACY_WEIGHT = 0.0
FITNESS_RUN_TIME_WEIGHT = 5.0 / 60.0

##################################################
#             NEURAL NETWORK SETTINGS
##################################################

# Number of hidden layers in the network
NUM_HIDDEN_LAYERS = 2

# Number of neurons in each hidden layer
HIDDEN_LAYER_SIZE = 10

# Which activation function to use between hidden layers
[LOG, RELU, SIGMOID, SOFTPLUS] = range(4)
HIDDEN_LAYER_ACTIVATION_FN = SIGMOID

# Threshold value for activation in the output layer
OUTPUT_ACTIVATION_THRESHOLD = 0.5

# Crossover mechanism to use
[RANDOM, SPLIT] = range(2)
CROSSOVER_MECHANISM = SPLIT

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

# Whether to use a predetermined random seed for the RNG
USE_PREDETERMINED_SEED = False

# Predetermined seed to use if specified
PREDETERMINED_SEED = 0

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
@click.option("--game-algorithm-id", type=click.Choice(["simple", "nn"]),
        default=None, help="Algorithm to use when AI is playing the game.")
@click.option("--game-ai-brain", type=click.Path(exists=True),
        default=None, help="Path to AI brain to use when playing the game.")
@click.option("--experiment-algorithm-id", type=click.Choice(["simple", "nn"]),
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
        default=None, help="Weight of runtime in the fitness function.")
@click.option("--num-hidden-layers", type=int,
        default=None, help="Number of hidden layers in the neural network.")
@click.option("--hidden-layer-size", type=int,
        default=None, help="Number of neurons in each hidden layer.")
@click.option("--hidden-layer-activation-fn", type=click.Choice(["log", "relu",
        "sigmoid", "softplus"]), default=None,
        help="Which activation function to use between hidden layers.")
@click.option("--output-activation-threshold", type=float,
        default=None, help="Activation threshold value for output layer.")
@click.option("--crossover-mechanism", type=click.Choice(["random", "split"]),
        default=None, help="Crossover mechanism to use.")
@click.option("--use-predetermined-seed", type=click.Choice(["true", "false"]),
        default=None, help="Whether to use a predetermined RNG seed.")
@click.option("--predetermined-seed", type=int,
        default=None, help="Predetermined seed to use if specified.")

def cli_configure_settings(run_mode, player_mode, game_algorithm_id,
        game_ai_brain, experiment_algorithm_id, experiment_directory,
        experiment_echo_logs, max_generations, progress_improvement_threshold,
        max_generations_without_progress, generation_population, mutation_rate,
        fitness_score_weight, fitness_runtime_weight, num_hidden_layers,
        hidden_layer_size, hidden_layer_activation_fn,
        output_activation_threshold, crossover_mechanism, use_predetermined_seed,
        predetermined_seed):
    """
    Configures settings according to the command line arguments.
    """
    """
    NOTE: To support a new setting, add it to the click options above,
        the method arguments, the list of global variables, and the
        code block in the method body.

    EXTRA NOTE: Currently investigating other ways of doing this that
        doesn't involve this massive click method...
    """
    global RUN_MODE, PLAYER_MODE, GAME_ALGORITHM_ID, GAME_AI_BRAIN, \
            EXPERIMENT_ALGORITHM_ID, EXPERIMENT_DIRECTORY, EXPERIMENT_ECHO_LOGS, \
            MAX_GENERATIONS, PROGRESS_IMPROVEMENT_THRESHOLD, \
            MAX_GENERATIONS_WITHOUT_PROGRESS, GENERATION_POPULATION, \
            MUTATION_RATE, FITNESS_SCORE_WEIGHT, FITNESS_RUNTIME_WEIGHT, \
            NUM_HIDDEN_LAYERS, HIDDEN_LAYER_SIZE, HIDDEN_LAYER_ACTIVATION_FN, \
            OUTPUT_ACTIVATION_THRESHOLD, CROSSOVER_MECHANISM, \
            USE_PREDETERMINED_SEED, PREDETERMINED_SEED
    if run_mode is not None:
        RUN_MODE = {"game": GAME, "experiment": EXPERIMENT}[run_mode]
    if player_mode is not None:
        PLAYER_MODE = {"human": HUMAN, "ai": AI}[player_mode]
    if game_algorithm_id is not None:
        GAME_ALGORITHM_ID = {"simple": SIMPLE, "nn": NN}[game_algorithm_id]
    if game_ai_brain is not None:
        GAME_AI_BRAIN = game_ai_brain
    if experiment_algorithm_id is not None:
        EXPERIMENT_ALGORITHM_ID = {"simple": SIMPLE, "nn": NN}\
                [experiment_algorithm_id]
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
    if num_hidden_layers is not None:
        NUM_HIDDEN_LAYERS = num_hidden_layers
    if hidden_layer_size is not None:
        HIDDEN_LAYER_SIZE = hidden_layer_size
    if hidden_layer_activation_fn is not None:
        HIDDEN_LAYER_ACTIVATION_FN = {"log": LOG, "relu": RELU, "sigmoid": SIGMOID,
                "softplus": SOFTPLUS}[hidden_layer_activation_fn]
    if output_activation_threshold is not None:
        OUTPUT_ACTIVATION_THRESHOLD = output_activation_threshold
    if crossover_mechanism is not None:
        CROSSOVER_MECHANISM = {"random": RANDOM, "split": SPLIT}\
                [crossover_mechanism]
    if use_predetermined_seed is not None:
        USE_PREDETERMINED_SEED = {"true": True, "false": False}\
                [use_predetermined_seed]
    if predetermined_seed is not None:
        PREDETERMINED_SEED = predetermined_seed
