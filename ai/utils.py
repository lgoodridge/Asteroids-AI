"""
Defines utility functions for the AI modules.
"""

LOG_FILENAME = "_log.txt"
META_FILENAME = "_meta.txt"
SUMMARY_FILENAME = "_summary.txt"

def algorithm_id_to_generation_class(brain_type):
    """
    Returns the Generation class corresponding to the
    provided algorithm ID (as defined in settings).
    """
    raise NotImplementedError()
