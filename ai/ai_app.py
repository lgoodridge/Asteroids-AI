from ai.ai_player import AI_Player
from asteroids.app import App
from asteroids.utils import render_on, WHITE
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

    def _render_ai_spectator_overlay(self):
        """
        Renders overlay components used in AI Spectator mode.
        Returns a list of rectangles to be re-rendered.
        """
        render_rects = []

        # Show fitness stats in top-left, under Score, if necessary
        if settings.SHOW_SCORE:
            run_time_text = self._small_font.render("Runtime: %ds (%d)" %
                    (self.run_time/60, self.run_time), True, WHITE)
            run_time_rect = render_on(run_time_text, self.screen,
                    run_time_text.get_width()/2, run_time_text.get_height()*3/2)
            render_rects.append(run_time_rect)

            accuracy_text = self._small_font.render("Accuracy: %.2f" %
                    self._get_accuracy(), True, WHITE)
            accuracy_rect = render_on(accuracy_text, self.screen,
                    accuracy_text.get_width()/2, accuracy_text.get_height()*5/2)
            render_rects.append(accuracy_rect)

            fitness_text = self._small_font.render("Fitness: %d" %
                    self._get_fitness(), True, WHITE)
            fitness_rect = render_on(fitness_text, self.screen,
                    fitness_text.get_width()/2, fitness_text.get_height()*7/2)
            render_rects.append(fitness_rect)

        # Return the rects to be re-rendered
        return render_rects

    def _handle_ai_spectator_controls(self, event):
        """
        Checks whether event was an AI Spectator mode
        specific control, and handles it if so.
        """
        pass

    def _get_accuracy(self):
        """
        Returns the player's current accuracy.
        """
        if self.player.num_bullets_fired == 0:
            return 0.0
        return 1.0 * self.asteroids_hit / self.player.num_bullets_fired

    def _get_fitness(self):
        """
        Returns the current fitness score.
        """
        return ((self.score * settings.FITNESS_SCORE_WEIGHT) +
                (self.run_time * settings.FITNESS_RUN_TIME_WEIGHT) +
                (self._get_accuracy() * settings.FITNESS_ACCURACY_WEIGHT))

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
        return self._get_fitness()

    def cleanup_simulation(self):
        """
        Cleans up the app after all simulations are run.
        """
        self.ai_brain = None
        self._cleanup()
