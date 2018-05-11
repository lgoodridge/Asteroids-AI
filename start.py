"""
Entry point for the Asteroids Game / AI.

Usage: python start.py
"""

from ai.ai_app import AI_App
from asteroids.app import App
import settings

if __name__ == "__main__":
    if settings.PLAYER_MODE == settings.HUMAN:
        App().start_game()
    else:
        if settings.AI_BRAIN == settings.SIMPLE:
            ai_brain = None
        AI_App().start_game(ai_brain)
