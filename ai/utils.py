"""
Defines utility functions for the AI modules.
"""

import settings

# Base filenames for experiment / generation files
LOG_FILENAME = "_log.txt"
META_FILENAME = "_meta.txt"
SUMMARY_FILENAME = "_summary.txt"

def _algorithm_id_to_class_data(algorithm_id):
    """
    Relates each algorithm ID to a tuple containing
    the corresponding AI Brain and Generation classes
    """
    if algorithm_id == settings.SIMPLE:
        from simple.simple_brain import Simple_Brain
        from simple.simple_generation import Simple_Generation
        return (Simple_Brain, Simple_Generation)
    elif algorithm_id == settings.NN:
        from nn.nn_brain import NN_Brain
        from nn.nn_generation import NN_Generation
        return (NN_Brain, NN_Generation)
    else:
        raise ValueError(("Programmer Error: '%d' not a recognized"
            "algorithm ID") % algorithm_id)

def algorithm_id_to_ai_brain_class(algorithm_id):
    """
    Returns the AI Brain class corresponding to the
    provided algorithm ID (as defined in settings).
    """
    return _algorithm_id_to_class_data(algorithm_id)[0]

def algorithm_id_to_generation_class(algorithm_id):
    """
    Returns the Generation class corresponding to the
    provided algorithm ID (as defined in settings).
    """
    return _algorithm_id_to_class_data(algorithm_id)[1]
