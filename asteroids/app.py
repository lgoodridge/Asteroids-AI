from asteroids.asteroid import Asteroid
from asteroids.bullet import Bullet
from asteroids.player import Player
from asteroids.utils import render_on, BLACK, GRAY, WHITE
import math
import pygame
import settings

class App(object):
    """
    Defines the main application logic for the Asteroids game.
    """

    # Game states
    SETUP, SPLASH, RUNNING, GAME_OVER = range(4)

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

        # Set up the game clock
        self._clock = pygame.time.Clock()

        # Set up the game screen
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.screen.fill(BLACK)
        pygame.display.flip()

        # Load the game font's (uses system's default font)
        self._big_font = pygame.font.SysFont(None, 100)
        self._medium_font = pygame.font.SysFont(None, 50)
        self._small_font = pygame.font.SysFont(None, 24)

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
                True, WHITE)
        self._splash_text = self._medium_font.render(
                "Click or press Enter to begin.", True, GRAY)
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
        self.asteroids = [Asteroid(3, 200, 100, 0, 0, shape=2), Asteroid(2, 400, 600, 2, math.pi/3, shape=2)]
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def _load_game_over(self):
        """
        Hides the player and loads the Game Over screen.
        """
        self._state = App.GAME_OVER
        self.player.x = -self.player.radius
        self.player.y = -self.player.radius
        self.player.speed = 0
        self.player.boosting = False

    def _update(self):
        """
        Performs one step of the execution loop for all game components.
        """
        if self._state != App.RUNNING and self._state != App.GAME_OVER:
            return

        # If the player is destroyed, transition to Game Over state or quit
        if self._state == App.RUNNING and self.player.destroyed:
            if settings.PLAYER_MODE == settings.HUMAN:
                self._load_game_over()
            else:
                raise NotImplementedError()

        # Remove destroyed components
        self.bullets = filter(lambda x: not x.destroyed, self.bullets)
        self.asteroids = filter(lambda x: not x.destroyed, self.asteroids)

        # Move all game components
        self.player.move()
        for bullet in self.bullets:
            bullet.move()
        for asteroid in self.asteroids:
            asteroid.move()

        # Check for player collisions with asteroids:
        self.player.check_for_collisions(self.asteroids)

        # Age and check for bullet collisions with asteroids
        for bullet in self.bullets:
            bullet.check_for_collisions(aself.steroids)
            bullet.increase_age()

    def _render(self):
        """
        Re-renders all game components.
        """
        if self._state != App.RUNNING and self._state != App.GAME_OVER:
            return

        # Reset the screen
        self.screen.fill((0, 0, 0))

        # Redraw all non-destroyed game components
        if not self.player.destroyed:
            self.player.draw(self.screen)
        for bullet in self.bullets:
            if not bullet.destroyed:
                bullet.draw(self.screen)
        for asteroid in self.asteroids:
            if not asteroid.destroyed:
                asteroid.draw(self.screen)

        # Add render rects for the components current and previous positions
        render_rects = []
        self.player.add_render_rects(render_rects)
        for bullet in self.bullets:
            bullet.add_render_rects(render_rects)
        for asteroid in self.asteroids:
            asteroid.add_render_rects(render_rects)

        # Show FPS text in bottom left if necessary
        if settings.SHOW_FPS:
            current_fps = 0 if math.isinf(self._clock.get_fps()) \
                    else int(self._clock.get_fps())
            fps_text = self._small_font.render(
                    "FPS: %d" % current_fps, True, WHITE)
            fps_rect = render_on(fps_text, self.screen, fps_text.get_width() / 2,
                    settings.HEIGHT - fps_text.get_height() / 2)
            render_rects.append(fps_rect)

        # If the game is over, display game over text
        if self._state == App.GAME_OVER:
            game_over_text = self._big_font.render("GAME OVER", True, WHITE)
            game_over_rect = render_on(game_over_text, self.screen,
                    settings.WIDTH/2, settings.HEIGHT/2)
            render_rects.append(game_over_rect)

        # Actually re-render all collected rectangles
        pygame.display.update(render_rects)

    def _handle_event(self, event):
        """
        Interprets and handles an asynchronous event.
        """
        # Stop running when the close button or 'Q' is pressed
        if event.type == pygame.QUIT or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self._running = False

        # Check if user clicked or pressed enter to begin
        elif self._state == App.SPLASH:
            if (event.type == pygame.MOUSEBUTTONDOWN) or \
                    (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_RETURN):
                self._load_level()

        elif self._state == App.RUNNING or self._state == App.GAME_OVER:

            # Handle settings + debugging actions
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                settings.SHOW_COLLISION_BOUNDARY = settings.DEBUG_MODE or \
                        not settings.SHOW_COLLISION_BOUNDARY
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                settings.DEBUG_MODE = not settings.DEBUG_MODE
                settings.SHOW_COLLISION_BOUNDARY = settings.DEBUG_MODE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                settings.SHOW_FPS = not settings.SHOW_FPS
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if len(self.asteroids) > 0:
                    self.asteroids[0].split(self.asteroids)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                self.player.destroyed = True

            # Running state only controls
            if self._state == App.RUNNING:

                # Handle human player controls
                if settings.PLAYER_MODE == settings.HUMAN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.player.boosting = True
                        if event.key == pygame.K_LEFT:
                            self.player.spin = Player.COUNTER_CLOCKWISE
                        if event.key == pygame.K_RIGHT:
                            self.player.spin = Player.CLOCKWISE
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.player.boosting = False
                        if event.key == pygame.K_LEFT:
                            self.player.spin = Player.NO_SPIN
                        if event.key == pygame.K_RIGHT:
                            self.player.spin = Player.NO_SPIN

                # Handle AI spectator controls
                elif settings.PLAYER_MODE == settings.AI:
                    raise NotImplementedError()

        # Don't listen to events in other app states
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
            self._clock.tick(settings.MAX_FPS)
        self._cleanup()

