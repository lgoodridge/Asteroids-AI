from asteroids.player import Player
from asteroids.utils import render_on
import math
import pygame
import settings

class App(object):
    """
    Defines the main application logic for the Asteroids game.
    """

    # Game states
    SETUP, SPLASH, RUNNING = range(3)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._has_started = False
        self._running = False

    def _setup(self):
        """
        Perform initial setup for all game components.
        """
        if self._has_started:
            raise RuntimeError("Programmer Error: App._setup() called twice.")
        self._has_started = True

        # Set up the game screen
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        # Load the game font's (uses system's default font)
        self._big_font = pygame.font.SysFont(None, 100)
        self._medium_font = pygame.font.SysFont(None, 50)
        self._small_font = pygame.font.SysFont(None, 25)

        # Initialize game component variables
        self.player = None
        self.bullets = []
        self.asteroids = []

        # Set the initial game state
        self._state = App.SETUP
        self._running = True

    def _cleanup(self):
        """
        Cleanup all game components.
        """
        pygame.quit()
        pygame.mixer.quit()

    def _load_splash(self):
        """
        Loads the splash page for human players.
        """
        self._state = App.SPLASH
        self._splash_title = self._big_font.render("Asteroids",
                True, (220, 220, 220))
        self._splash_text = self._medium_font.render(
                "Click or press Enter to begin.", True, (140, 140, 140))
        render_on(self._splash_title, self.screen, settings.WIDTH/2,
                settings.HEIGHT/2 - self._splash_title.get_height())
        render_on(self._splash_text, self.screen, settings.WIDTH/2,
                settings.HEIGHT/2 + self._splash_text.get_height())
        pygame.display.flip()

    def _load_level(self):
        """
        Loads the initial game components for the level.
        """
        self._state = App.RUNNING
        self.player = Player(settings.WIDTH/2, settings.HEIGHT/2)
        self.bullets = []
        self.asteroids = []     # TODO: Load initial asteroids
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def _update(self):
        """
        Performs one step of the execution loop for all game components.
        """
        if self._state != App.RUNNING:
            return

        # Move all game components
        self.player.move()
        for bullet in self.bullets:
            bullet.move()
        for asteroid in self.asteroids:
            asteroid.move()

    def _render(self):
        """
        Re-renders all game components.
        """
        if self._state != App.RUNNING:
            return

        # Reset the screen
        self.screen.fill((0, 0, 0))

        # Redraw all game components
        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        # Actually re-render the current and previous component render rects
        render_rects = []
        self.player.add_render_rects(render_rects)
        for bullet in self.bullets:
            bullet.add_render_rects(render_rects)
        for asteroid in self.asteroids:
            asteroid.add_render_rects(render_rects)
        pygame.display.update(render_rects)

    def _handle_event(self, event):
        """
        Interprets and handles an asynchronous event.
        """
        # Stop running when the close button is pressed
        if event.type == pygame.QUIT:
            self._running = False

        # Check if user clicked or pressed enter to begin
        elif self._state == App.SPLASH:
            if (event.type == pygame.MOUSEBUTTONDOWN) or \
                    (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_RETURN):
                self._load_level()

        # Manage player controls
        elif self._state == App.RUNNING:

            # Manage general running state controls
            if pygame.key.get_pressed()[pygame.K_f]:
                pass    # TODO: Toggle FPS display

            # Manage player controls
            elif settings.PLAYER_MODE == settings.HUMAN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.boosting = True
                    elif event.key == pygame.K_LEFT:
                        self.player.spin = Player.COUNTER_CLOCKWISE
                    elif event.key == pygame.K_RIGHT:
                        self.player.spin = Player.CLOCKWISE
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player.boosting = False
                    elif event.key == pygame.K_LEFT:
                        self.player.spin = Player.NO_SPIN
                    elif event.key == pygame.K_RIGHT:
                        self.player.spin = Player.NO_SPIN

            # Manage AI spectator controls
            elif settings.PLAYER_MODE == settings.AI:
                raise NotImplementedError()

        # Unhandled event
        else:
            return

    def start_game(self):
        """
        Sets up the game and begins the main execution loop.
        """
        self._setup()

        # Load the splash page if a human is playing,
        # otherwise, load directly into the level
        if settings.PLAYER_MODE == settings.HUMAN:
            self._load_splash()
        else:
            self._load_level()

        # Run the main execution loop
        while self._running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._update()
            self._render()
        self._cleanup()

