"""
Defines utility functions for the AI modules.
"""

import settings

# Base filenames for experiment / generation files
LOG_FILENAME = "_log.txt"
META_FILENAME = "_meta.txt"
SUMMARY_FILENAME = "_summary.txt"

# Relates each algorithm ID to a tuple containing
# the corresponding AI Brain and Generation classes
_ALGORITHM_ID_TO_CLASS_DATA = {
    settings.SIMPLE: (None, None)
}

def algorithm_id_to_ai_brain_class(algorithm_id):
    """
    Returns the AI Brain class corresponding to the
    provided algorithm ID (as defined in settings).
    """
    if algorithm_id not in _ALGORITHM_ID_TO_CLASS_DATA:
        raise ValueError(("Programmer Error: '%d' not a recognized"
            "algorithm ID") % algorithm_id)
    return _ALGORITHM_ID_TO_CLASS_DATA[algorithm_id][0]

def algorithm_id_to_generation_class(algorithm_id):
    """
    Returns the Generation class corresponding to the
    provided algorithm ID (as defined in settings).
    """
    if algorithm_id not in _ALGORITHM_ID_TO_CLASS_DATA:
        raise ValueError(("Programmer Error: '%d' not a recognized"
            "algorithm ID") % algorithm_id)
    return _ALGORITHM_ID_TO_CLASS_DATA[algorithm_id][1]
