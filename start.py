"""
Entry point for the Asteroids Game / AI.

Usage: python start.py [--help]
"""

from ai.ai_app import AI_App
from ai.experiment import run_experiment
from ai.utils import algorithm_id_to_ai_brain_class
from asteroids.app import App
import settings

if __name__ == "__main__":

    # Configure settings according to command line arguments
    settings.configure_settings()

    # Start the game if specified
    if settings.RUN_MODE == settings.GAME:
        if settings.USE_PREDETERMINED_SEEDS:
            seed = settings.PREDETERMINED_SEEDS[0]
        else:
            seed = None

        if settings.PLAYER_MODE == settings.HUMAN:
            App().start_game(seed=seed)
        else:
            ai_brain_class = algorithm_id_to_ai_brain_class(
                    settings.GAME_ALGORITHM_ID)
            ai_brain = ai_brain_class.load(settings.GAME_AI_BRAIN)
            AI_App().start_game(ai_brain, seed=seed)

    # Start experiment if specified
    elif settings.RUN_MODE == settings.EXPERIMENT:
        run_experiment()
