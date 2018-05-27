from ai.ai_player import AI_Player
from asteroids.app import App
import settings

class AI_App(App):
    """
    Defines the main application for the game,
    when the player is an AI controller.
    """

    def _spawn_player(self):
        """
        Creates and returns a new AI_Player in the center of the screen.
        """
        return AI_Player(settings.WIDTH/2, settings.HEIGHT/2, self._ai_brain)

    def _update_player(self):
        """
        Reads the current game state + has the player respond accordingly.
        """
        sensor_data = self.player.sense(self.asteroids, self.bullets)
        self.player.update(self.bullets, sensor_data)

    def _handle_ai_spectator_controls(self, event):
        """
        Checks whether event was an AI Spectator mode
        specific control, and handles it if so.
        """
        pass

    def start_game(self, ai_brain):
        """
        Starts the game using the provided AI controller.
        """
        self._ai_brain = ai_brain
        super(AI_App, self).start_game()

    def run_simulation(self, ai_brain):
        """
        Runs the game to completion in non-graphical mode using
        the provided AI controller, and returns the fitness score.
        """
        self._ai_brain = ai_brain

        # Turn off sounds for the duration of the simulation
        previous_play_sfx = settings.PLAY_SFX
        settings.PLAY_SFX = False

        # Prepare the simulation
        if not self._has_started:
            self._setup(use_screen=False)
        else:
            self._running = True
        self._load_level()

        # Run it until the player dies
        while self._running:
            self._update()

        # Clean up the app for potential reuse
        settings.PLAY_SFX = previous_play_sfx

        # Return the fitness score
        fitness = ((self.score * settings.FITNESS_SCORE_WEIGHT) +
                (self.run_time * settings.FITNESS_RUN_TIME_WEIGHT))
        return fitness

    def cleanup_simulation(self):
        """
        Cleans up the app after all simulations are run.
        """
        self.ai_brain = None
        self._cleanup()
