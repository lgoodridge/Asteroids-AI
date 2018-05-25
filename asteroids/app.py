from asteroids.asteroid import Asteroid
from asteroids.bullet import Bullet
from asteroids.player import Player
from asteroids.sound import load_sounds, play_sound, stop_sound, stop_all_sounds
from asteroids.utils import render_on, BLACK, GRAY, WHITE
import math
import pygame
import settings
from ai.sensor import sense_eight_dir

class App(object):
    """
    Defines the main application logic for the Asteroids game.
    """

    # Game states
    SETUP, SPLASH, RUNNING, GAME_OVER = range(4)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        load_sounds()
        self._has_started = False
        self._running = False

    def _setup(self, use_screen=True):
        """
        Perform initial setup for all game components.
        If use_screen is True, sets up the game screen for use as well.
        """
        if self._has_started:
            raise RuntimeError("Programmer Error: App._setup() called twice.")
        self._has_started = True

        # Set up the game clock
        self._clock = pygame.time.Clock()

        # Set up the game screen, if necessary
        self._use_screen = use_screen
        if use_screen:
            self.screen = pygame.display.set_mode(
                    (settings.WIDTH, settings.HEIGHT))
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

        # Iniitialize performance trackers
        self.score = 0
        self.run_time = 0

        # Initialize score and time trackers
        self._start_time = 0
        self._last_spawn_time = 0
        self._spawn_period = 0

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

        # Load initial game components
        self.player = self._spawn_player()
        self.bullets = []
        self.asteroids = []
        for i in range(4):
            Asteroid.spawn(self.asteroids, self.player, False)
        Asteroid.spawn(self.asteroids, self.player, True)

        # Initialize performance trackers
        self.score = 0
        self.run_time = 0

        # Load initial time tracker state
        self._start_time = pygame.time.get_ticks()
        self._last_spawn_time = pygame.time.get_ticks()
        self._spawn_period = settings.INITIAL_SPAWN_PERIOD

        # Reset sounds and start the BGM
        stop_all_sounds()
        play_sound("bgm", -1)

        # Reset the screen, if necessary
        if self._use_screen:
            self.screen.fill(BLACK)
            pygame.display.flip()

    def _load_game_over(self):
        """
        Hides the player and loads the Game Over screen.
        """
        self._state = App.GAME_OVER
        self.player.x = -self.player.radius
        self.player.y = -self.player.radius
        self.player.speed = 0
        self.player.stop_boosting()
        self.player.stop_spinning()
        stop_sound("bgm")

    def _update(self):
        """
        Performs one step of the execution loop for all game components.
        """
        if self._state != App.RUNNING and self._state != App.GAME_OVER:
            return

        # If the player is destroyed, transition to Game Over state or quit.
        if self._state == App.RUNNING and self.player.destroyed:
            if self._use_screen:
                self._load_game_over()
            else:
                self._running = False

        # Remove destroyed components
        self.bullets = filter(lambda x: not x.destroyed, self.bullets)
        self.asteroids = filter(lambda x: not x.destroyed, self.asteroids)

        # If the spawn period has expired, spawn a new aimed Asteroid
        time_since_last_spawn = pygame.time.get_ticks() - self._last_spawn_time
        if time_since_last_spawn > self._spawn_period:
            new_spawn_period = self._spawn_period - settings.SPAWN_PERIOD_DEC
            self._spawn_period = max(new_spawn_period, settings.MIN_SPAWN_PERIOD)
            self._last_spawn_time = pygame.time.get_ticks()
            Asteroid.spawn(self.asteroids, self.player, True)

        # Update the player with the current game state
        self._update_player()

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
            self.score += int(bullet.check_for_collisions(self.asteroids))
            bullet.increase_age()

        # Increment run time if the player is still alive
        if not self.player.destroyed:
            self.run_time += 1

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

        # Show score in top left if necessary
        if settings.SHOW_SCORE:
            score_text = self._small_font.render(
                    "Score: %d" % self.score, True, WHITE)
            score_rect = render_on(score_text, self.screen,
                    score_text.get_width() / 2, score_text.get_height()/2)
            render_rects.append(score_rect)

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

            # B: Toggle collision boundary display
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                settings.SHOW_COLLISION_BOUNDARY = settings.DEBUG_MODE or \
                        not settings.SHOW_COLLISION_BOUNDARY
            # C: Toggle score display
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                settings.SHOW_SCORE = not settings.SHOW_SCORE
            # D: Toggle debug (invincible) mode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                settings.DEBUG_MODE = not settings.DEBUG_MODE
                settings.SHOW_COLLISION_BOUNDARY = settings.DEBUG_MODE
            # F: Toggle FPS display
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                settings.SHOW_FPS = not settings.SHOW_FPS
            # N: Spawn a new aimed asteroid
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                Asteroid.spawn(self.asteroids, self.player, True)
            # R: Resets the level
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._load_level()
            # S: Toggles sound effects
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                settings.PLAY_SFX = not settings.PLAY_SFX
                if settings.PLAY_SFX:
                    play_sound("bgm", -1)
                else:
                    stop_all_sounds()
            # X: Splits the first asteroid on the asteroid list
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                if len(self.asteroids) > 0:
                    self.asteroids[0].split(self.asteroids)

            # Running state only controls
            if self._state == App.RUNNING:

                # Handle human player controls
                if settings.PLAYER_MODE == settings.HUMAN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.player.start_boosting()
                        if event.key == pygame.K_LEFT:
                            self.player.start_spinning(False)
                        if event.key == pygame.K_RIGHT:
                            self.player.start_spinning(True)
                        if event.key == pygame.K_SPACE:
                            self.player.shoot(self.bullets)
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.player.stop_boosting()
                        if event.key == pygame.K_LEFT:
                            self.player.stop_spinning()
                        if event.key == pygame.K_RIGHT:
                            self.player.stop_spinning()

                # Handle AI spectator controls
                elif settings.PLAYER_MODE == settings.AI:
                    self._handle_ai_spectator_controls(event)

        # Don't listen to events in other app states
        else:
            return

    def start_game(self):
        """
        Sets up the game and begins the main execution loop.
        """
        self._setup()

        # Load the splash page, and wait for input to continue
        self._load_splash()

        # Run the main execution loop
        while self._running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._update()
            self._render()
            self._clock.tick(settings.MAX_FPS)
        self._cleanup()

    ##################################################
    #       TO BE IMPLEMENTED BY AI SUBCLASSES
    ##################################################

    def _spawn_player(self):
        """
        Creates and returns a new Player in the center of the screen.
        """
        return Player(settings.WIDTH/2, settings.HEIGHT/2)

    def _update_player(self):
        """
        Reads the current game state + has the player respond accordingly.
        """
        pass

    def _handle_ai_spectator_controls(self, event):
        """
        Checks whether event was an AI Spectator mode
        specific control, and handles it if so.
        """
        raise NotImplementedError("'_handle_ai_spectator_controls' "
                "should only be called by AI_App")

