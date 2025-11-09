"""
Defines settings for the Asteroids Game / AI.
"""

import json
import multiprocessing
import os
import sys

import click


class Settings:
    """
    Holds the settings for the current game or experiment.

    Supports loading values from a variety of sources.
    """

    # Run Modes
    GAME = "game"
    EXPERIMENT = "experiment"

    # Player Modes
    HUMAN = "human"
    AI = "ai"

    # Algorithm IDs
    SIMPLE = "simple"
    NN = "nn"

    # Champion Selection Schemes
    # Static - a predetermined number of champions are chosen
    # Performance - choose members whose fitness >> the mean
    STATIC = "static"
    PERFORMANCE = "performance"

    # Sensor IDs
    NDIR = "ndir"

    # Sensor Output Shapes
    LINEAR = "linear"
    HYPERBOLIC = "hyperbolic"

    # Activation Functions
    LOG = "log"
    RELU = "relu"
    SIGMOID = "sigmoid"
    SOFTPLUS = "softplus"

    # Crossover Mechanisms
    RANDOM = "random"
    SPLIT = "split"

    def __init__(self):
        """
        Initialize settings with sane defaults
        """
        ##################################################
        #                  AI SETTINGS
        ##################################################

        # Whether we are playing the game or
        # starting / continuing an experiment
        self.RUN_MODE = Settings.GAME

        # Who (or what) is playing the game
        self.PLAYER_MODE = Settings.HUMAN

        # Algorithm to use when AI is training or playing the game
        self.ALGORITHM_ID = Settings.SIMPLE

        # Path to the AI brain to use when playing the game
        self.GAME_AI_BRAIN = os.path.join("experiments", "simple", "_best.brn")

        # Path to the directory used by the experiment:
        # If the directory contains the work of a previous experiment,
        # it will be continued; otherwise a new experiment is started
        self.EXPERIMENT_DIRECTORY = os.path.join("experiments", "default")

        # Whether to echo messages written to the
        # experiment log to the console as well
        self.EXPERIMENT_ECHO_LOGS = True

        # Number of concurrent processes to use for multithreaded
        # operations (e.g. evaluating fitnesses)
        self.NUM_THREADS = multiprocessing.cpu_count()

        # Maximum number of generations to run the
        # experiment for, if it doesn't get ended early
        self.MAX_GENERATIONS = 200

        # Minimum improvement in fitness needed between
        # generations for us to consider it "progress"
        self.PROGRESS_IMPROVEMENT_THRESHOLD = 1

        # Maximum number of generations to wait without
        # progress before ending the experiment early
        self.MAX_GENERATIONS_WITHOUT_PROGRESS = 20

        # Number of brains in each generation
        self.GENERATION_POPULATION = 200

        # Percentage of the current generation to
        # keep when breeding the next generation
        self.GENERATION_SURVIVOR_RATE = 0.25

        # Rate of chromosome mutations when
        # breeding to create the next generation
        self.MUTATION_RATE = 0.05

        # Number of simulations to run when determining fitness
        self.NUM_EVALUATION_SIMULATIONS = 1

        # Weights of each variable in the fitness function
        self.FITNESS_SCORE_WEIGHT = 1.0
        self.FITNESS_RUN_TIME_WEIGHT = 5.0 / 60.0
        self.FITNESS_MISSED_SHOT_PENALTY = 0.5

        # A "champion" is a member of a generation that is preserved
        # unmutated into the next generation:
        self.CHAMPION_SELECTION_SCHEME = Settings.PERFORMANCE

        # Static number of champions to select each round
        self.NUM_CHAMPIONS = 1

        # Performance fitness threshold is the mean multiplied by this value
        self.CHAMPION_THRESHOLD_MULTIPLIER = 2.0

        # Which sensor to use
        self.SENSOR_ID = Settings.NDIR

        # Output shape of the sensor function
        self.SENSOR_OUTPUT_SHAPE = Settings.LINEAR

        # Maximum object sensing distance
        self.MAX_SENSOR_DISTANCE = 400

        # Number of angle regions to divide the sensor space into
        self.NUM_SENSOR_REGIONS = 8

        ##################################################
        #             NEURAL NETWORK SETTINGS
        ##################################################

        # Number of hidden layers in the network
        self.NUM_HIDDEN_LAYERS = 2

        # Number of neurons in each hidden layer
        self.HIDDEN_LAYER_SIZE = 20

        # Which activation function to use between hidden layers
        self.HIDDEN_LAYER_ACTIVATION_FN = Settings.SIGMOID

        # Threshold value for activation in the output layer
        self.OUTPUT_ACTIVATION_THRESHOLD = 0.8

        # Crossover mechanism to use
        self.CROSSOVER_MECHANISM = Settings.SPLIT

        ##################################################
        #               CORE GAME SETTINGS
        ##################################################

        # Screen dimensions
        self.WIDTH = 800
        self.HEIGHT = 600

        # How "thick" the invisible edges of the screen are
        self.SCREEN_EDGE_THICKNESS = 20

        # Minimum distance the player has to be from an edge
        # for an asteroid to potentially spawn from that edge
        self.MIN_SPAWN_EDGE_DISTANCE = 200

        # Time (in milliseconds) between asteroid spawns at game start
        self.INITIAL_SPAWN_PERIOD = 5000

        # How much the spawn period decreases with each spawn
        self.SPAWN_PERIOD_DEC = 200

        # Minimum time (in milliseconds) between asteroid spawns
        self.MIN_SPAWN_PERIOD = 1000

        # Game update speed limit (0 means no limit)
        self.MAX_FPS = 60

        # Whether to load and be able to play sounds
        self.SOUNDS_ENABLED = True

        # Whether to use predetermined random seed(s) for the RNG
        self.USE_PREDETERMINED_SEEDS = False

        # Iterable of predetermined seed(s) to use if specified
        self.PREDETERMINED_SEEDS = []

        ##################################################
        #              SPECIAL CONDITIONS
        ##################################################

        # Forces player ship to keep moving
        self.ALWAYS_BOOSTING = False

        # Prevents player ship from moving
        self.DISABLE_BOOSTING = False

        # Prevents player ship from shooting
        self.DISABLE_SHOOTING = False

        ##################################################
        #               IN-GAME SETTINGS
        ##################################################

        # Whether debug mode is activated (player is invincible)
        self.DEBUG_MODE = False

        # Whether to show the collision boundary for components
        self.SHOW_COLLISION_BOUNDARY = False

        # Whether to show score in top left corner
        self.SHOW_SCORE = True

        # Whether to show FPS in bottom left corner
        self.SHOW_FPS = True

        # Whether to play sound effects
        self.PLAY_SFX = True

    def validate_and_set_dependents(self):
        """
        Sets any settings that are derived from other settings,
        then checks setting combinations for improper configurations.
        """
        # Set settings dependent on other settings
        if self.USE_PREDETERMINED_SEEDS and len(self.PREDETERMINED_SEEDS) == 0:
            self.PREDETERMINED_SEEDS = list(
                range(self.NUM_EVALUATION_SIMULATIONS)
            )

        # Check setting combinations for improper configurations
        if int(self.GENERATION_POPULATION * self.GENERATION_SURVIVOR_RATE) < 2:
            msg = (
                "With GENERATION_POPULATION = {} and "
                "GENERATION_SURVIVOR_RATE = {}, "
                "less than 2 members will survive each generation"
            ).format(self.GENERATION_POPULATION, self.GENERATION_SURVIVOR_RATE)
            raise ValueError(msg)
        if (
            self.RUN_MODE == Settings.EXPERIMENT
            and self.USE_PREDETERMINED_SEEDS
            and len(self.PREDETERMINED_SEEDS) < self.NUM_EVALUATION_SIMULATIONS
        ):
            msg = (
                "NUM_EVALUATION_SIMULATIONS is set to {}, but only {} seeds "
                "were provided"
            ).format(
                self.NUM_EVALUATION_SIMULATIONS, len(self.PREDETERMINED_SEEDS)
            )
            raise ValueError(msg)


##################################################
#        SETTINGS MODULE PUBLIC INTERFACE
##################################################

# Shared singleton Settings instance used by the settings
# util functions. Must be set with load_* before usage
_SETTINGS_INSTANCE = None


def get_settings():
    """
    Returns the singleton Settings instance.
    Throws an exception if the instance hasn't been loaded yet
    """
    global _SETTINGS_INSTANCE
    if _SETTINGS_INSTANCE is None:
        raise RuntimeError(
            "Settings must be initialized before use. "
            "Call a load_from_* function as appropriate."
        )
    return _SETTINGS_INSTANCE


def load_settings_from_settings(settings_obj):
    """
    Loads settings from another settings object.
    Used to copy settings data between multiprocessing workers.
    """
    global _SETTINGS_INSTANCE
    _SETTINGS_INSTANCE = settings_obj


def load_settings_from_dict(settings_dict):
    """
    Loads settings from a dictionary.
    Normalizes key names to upper snake case, and converts
    booleans passed as strings where appropriate.
    Keys that aren't present will use their default values.
    """
    global _SETTINGS_INSTANCE
    settings = Settings()

    for key, value in settings_dict.items():
        if value is None:
            continue

        # Normalize key names to upper snake case
        setting_name = key.upper().replace("-", "_")

        if hasattr(settings, setting_name):
            setting_type = type(getattr(settings, setting_name))

            # Ignore list settings with empty iterable values
            # (click's default for these is an empty tuple instead of None)
            if setting_type is list and len(value) == 0:
                continue
            # Handle list settings passed as tuples
            # e.g. click passes "multiple" args as tuples
            elif setting_type is list and isinstance(value, tuple):
                setattr(settings, setting_name, list(value))
            # Handle boolean settings passed as strings
            elif setting_type is bool and isinstance(value, str):
                setattr(
                    settings,
                    setting_name,
                    {"true": True, "false": False}[value],
                )
            # Handle simple settings (strings, ints, floats)
            else:
                setattr(settings, setting_name, value)

    settings.validate_and_set_dependents()
    _SETTINGS_INSTANCE = settings


def load_settings_from_cli():
    """
    Loads settings from command line arguments.
    """
    try:
        _click_load_settings_from_cli(standalone_mode=False)
    except click.exceptions.ClickException as e:
        e.show()
        sys.exit(e.exit_code)


def load_settings_from_json(json_filepath):
    """
    Loads settings from a JSON file.
    """
    settings_dict = _parse_json_as_dict(json_filepath)
    load_settings_from_dict(settings_dict)


##################################################
#            SETTINGS LOADER HELPERS
##################################################


@click.command(context_settings=dict(allow_extra_args=True))
@click.option(
    "--settings-file",
    type=click.Path(exists=True),
    default=None,
    help=(
        "Path to a settings JSON file. "
        "Other CLI args will override values from the JSON"
    ),
)
@click.option(
    "--run-mode",
    type=click.Choice([Settings.GAME, Settings.EXPERIMENT]),
    default=None,
    help="Whether to play the game, or run an experiment.",
)
@click.option(
    "--player-mode",
    type=click.Choice([Settings.HUMAN, Settings.AI]),
    default=None,
    help="Who (or what) is playing the game.",
)
@click.option(
    "--algorithm-id",
    type=click.Choice([Settings.SIMPLE, Settings.NN]),
    default=None,
    help="Algorithm to use when AI is training or playing the game.",
)
@click.option(
    "--game-ai-brain",
    type=click.Path(exists=True),
    default=None,
    help="Path to AI brain to use when playing the game.",
)
@click.option(
    "--num-threads",
    type=int,
    default=None,
    help="Number of workers to use for concurrent operations.",
)
@click.option(
    "--experiment-directory",
    type=click.Path(exists=False),
    default=None,
    help="Path to the directory used by the experiment.",
)
@click.option(
    "--experiment-echo-logs",
    type=click.Choice(["true", "false"]),
    default=None,
    help="Whether to echo messages for the log to console.",
)
@click.option(
    "--max-generations",
    type=int,
    default=None,
    help="Max # generations to run the experiment for.",
)
@click.option(
    "--progress-improvement-threshold",
    type=int,
    default=None,
    help="Minimum fitness improvement needed for progress.",
)
@click.option(
    "--max-generations-without-progress",
    type=int,
    default=None,
    help="Max # generations to wait without progress.",
)
@click.option(
    "--generation-population",
    type=int,
    default=None,
    help="Number of brains in each generation.",
)
@click.option(
    "--mutation-rate",
    type=float,
    default=None,
    help="Mutation rate when breeding generations.",
)
@click.option(
    "--num-evaluation-simulations",
    type=int,
    default=None,
    help="Number of simulations to run during evaluation.",
)
@click.option(
    "--fitness-score-weight",
    type=float,
    default=None,
    help="Weight of score in the fitness function.",
)
@click.option(
    "--fitness-runtime-weight",
    type=float,
    default=None,
    help="Weight of runtime in the fitness function.",
)
@click.option(
    "--fitness-missed-shot-penalty",
    type=float,
    default=None,
    help="Fitness penalty for each missed shot.",
)
@click.option(
    "--champion-selection-scheme",
    type=click.Choice([Settings.STATIC, Settings.PERFORMANCE]),
    default=None,
    help="How to champions are selected each generation.",
)
@click.option(
    "--num-champions",
    type=int,
    default=None,
    help="Number of champions to select each round.",
)
@click.option(
    "--champion-threshold-multiplier",
    type=float,
    default=None,
    help="Factor above the mean fitness required for champions.",
)
@click.option(
    "--sensor-id",
    type=click.Choice([Settings.NDIR]),
    default=None,
    help="Which sensor to use.",
)
@click.option(
    "--sensor-output-shape",
    type=click.Choice([Settings.LINEAR, Settings.HYPERBOLIC]),
    default=None,
    help="Output shape of the sensor function.",
)
@click.option(
    "--max-sensor-distance",
    type=int,
    default=None,
    help="Maximum object sensing distance.",
)
@click.option(
    "--num-sensor-regions",
    type=int,
    default=None,
    help="Number of sensor angle regions to use.",
)
@click.option(
    "--num-hidden-layers",
    type=int,
    default=None,
    help="Number of hidden layers in the neural network.",
)
@click.option(
    "--hidden-layer-size",
    type=int,
    default=None,
    help="Number of neurons in each hidden layer.",
)
@click.option(
    "--hidden-layer-activation-fn",
    type=click.Choice(
        [Settings.LOG, Settings.RELU, Settings.SIGMOID, Settings.SOFTPLUS]
    ),
    default=None,
    help="Which activation function to use between hidden layers.",
)
@click.option(
    "--output-activation-threshold",
    type=float,
    default=None,
    help="Activation threshold value for output layer.",
)
@click.option(
    "--crossover-mechanism",
    type=click.Choice([Settings.RANDOM, Settings.SPLIT]),
    default=None,
    help="Crossover mechanism to use.",
)
@click.option(
    "--use-predetermined-seeds",
    type=click.Choice(["true", "false"]),
    default=None,
    help="Whether to use predetermined RNG seeds.",
)
@click.option(
    "--predetermined-seeds",
    "-s",
    type=int,
    multiple=True,
    default=None,
    help="Predetermined seeds to use if specified.",
)
@click.option(
    "--always-boosting",
    type=click.Choice(["true", "false"]),
    default=None,
    help="Forces player ship to keep moving.",
)
@click.option(
    "--disable-boosting",
    type=click.Choice(["true", "false"]),
    default=None,
    help="Prevents player ship from moving.",
)
@click.option(
    "--disable-shooting",
    type=click.Choice(["true", "false"]),
    default=None,
    help="Prevents player ship from shooting.",
)
def _click_load_settings_from_cli(**kwargs):
    """
    Parses the CLI arguments with click, and loads them as a dict.

    If a settings JSON file is provided, loads values from that first,
    then overrides with other CLI arguments.
    """
    settings_dict = {}
    settings_file = kwargs.pop("settings_file", None)
    if settings_file:
        settings_dict = _parse_json_as_dict(settings_file)
    settings_dict.update(kwargs)
    load_settings_from_dict(settings_dict)


def _parse_json_as_dict(json_filepath):
    """
    Parses a JSON file and returns its contents as a dictionary.
    """
    if not os.path.exists(json_filepath):
        raise FileNotFoundError(f"JSON file not found: {json_filepath}")
    with open(json_filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON file ({json_filepath}): {e}"
            )
