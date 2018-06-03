"""
Implementations of several activation functions.
"""

import math
import settings

def log_activation(x):
    """
    Returns the log of x.
    """
    return math.log(x)

def relu_activation(x):
    """
    Returns x if positive, 0 otherwise.
    """
    return x if x > 0.0 else 0.0

def sigmoid_activation(x):
    """
    Returns the sigmoid output of x.
    """
    return 1.0 / (1.0 + math.exp(-x))

def softplus_activation(x):
    """
    Returns a smooth approximation of ReLU.
    """
    return math.log(1 + math.exp(x))

def threshold_activation(x, threshold):
    """
    Returns 1 if x is above threshold, 0 otherwise.
    """
    return int(x > threshold)

def get_activation_function(function_id):
    """
    Returns the function specified by the
    provided function ID, as defined in settings
    """
    if function_id == settings.LOG:
        return log_activation
    elif function_id == settings.RELU:
        return relu_activation
    elif function_id == settings.SIGMOID:
        return sigmoid_activation
    elif function_id == settings.SOFTPLU:
        return softplus_activation
    else:
        raise RuntimeError("Programmer Error: Invalid activation " +
                "function id '%d'" % function_id)
