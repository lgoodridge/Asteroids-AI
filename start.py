"""
Entry point for the Asteroids Game / AI.

Usage: python start.py
"""

from asteroids.app import App

if __name__ == "__main__":
    asteroids_app = App()
    asteroids_app.start_game()
