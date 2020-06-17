"""
Handles BGM and sound effects for the Asteroids game.
"""

import os
import pygame
import settings

# Whether the sound module has been initialized
_is_initialized = False

# Relates sound names to their loaded sound effect
_sound_library = {}

def load_sounds():
    """
    Loads all sounds from the designated director into the sound library.
    """
    global _is_initialized, _sound_library

    # Ensure we don't double initialize the sound module
    if _is_initialized:
        raise RuntimeError("Programmer Error: load_sounds called twice.")
    _is_initialized = True

    # Ensure the sounds directory actually exists
    sounds_directory = os.path.join("asteroids", "sounds")
    if not os.path.exists(sounds_directory):
        raise RuntimeError("Sounds directory (expected at asteroids/sounds/) " +
                "not found!")

    # Load all .wav files found within the sounds directory
    for filename in os.listdir(sounds_directory):
        if filename.endswith(".wav"):
            _sound_library[filename.split(".")[0]] = pygame.mixer.Sound(
                    os.path.join(sounds_directory, filename))

def play_sound(sound_name, loops=0):
    """
    Plays the sound with the provided name.
    The name should not include the file extension.
    """
    if not _is_initialized:
        raise RuntimeError("Programmer Error: sound module used " +
                "before load_sounds() call.")
    if settings.PLAY_SFX:
        _sound_library[sound_name].play(loops)

def stop_sound(sound_name, fadeout_ms=0):
    """
    Fades out and stops the sound with the provided name.
    Only necessary when sound was previously looped.
    """
    if not _is_initialized:
        raise RuntimeError("Programer Error: sound module used " +
                "before load_sounds() call.")
    _sound_library[sound_name].fadeout(fadeout_ms)

def stop_all_sounds():
    """
    Immediately halts playback of all sounds.
    """
    if not _is_initialized:
        raise RuntimeError("Programer Error: sound module used " +
                "before load_sounds() call.")
    for _, sound in _sound_library.items():
        sound.stop()

