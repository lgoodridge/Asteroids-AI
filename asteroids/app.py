from asteroids.player import Player
import pygame
import settings

class App(object):
    """
    Defines the main application logic for the Asteroids game.
    """

    # Game states
    SPLASH, RUNNING, PAUSED = range(3)

    def __init__(self):
        pygame.init()
        self._has_started = False
        self._running = False
        self._screen = None
        self.player = None
        self.bullets = []
        self.asteroids = []

    def _setup(self):
        """
        Perform initial setup for all game components.
        """
        if self._has_started:
            raise RuntimeError("Programmer Error: App._setup() called twice.")
        self._has_started = True

        # Initialize pygame modules
        pygame.init()
        pygame.mixer.init()

        # Set up the game screen
        self._screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self._screen.fill((0, 0, 0))
        pygame.display.flip()

        # Set the initial game state
        self._state = App.SPLASH
        self._running = True

    def _cleanup(self):
        """
        Cleanup all game components.
        """
        pygame.quit()
        pygame.mixer.quit()

    def _load_level(self):
        """
        Loads the initial game components for the level.
        """
        self.player = Player(settings.WIDTH/2, settings.HEIGHT/2)
        self.bullets = []
        self.asteroids = []     # TODO: Load initial asteroids

    def _update(self):
        """
        Performs one step of the execution loop for all game components.
        """
        pass

    def _render(self):
        """
        Re-renders all game components.
        """
        pass

    def _handle_event(self, event):
        """
        Interprets and handles an asynchronous event.
        """
        if event.type == pygame.QUIT:
            self._running = False

    def start_game(self):
        """
        Sets up the game and begins the main execution loop.
        """
        self._setup()
        while self._running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._update()
            self._render()
        self._cleanup()

