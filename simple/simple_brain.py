from ai.ai_brain import AI_Brain
from ai.sensor import sense_eight_dir
from asteroids.utils import LINEAR, HYPERBOLIC
import os

class Simple_Brain(AI_Brain):
    """
    Simple, procedural implementation of an AI brain.
    """

    def __init__(self):
        super(Simple_Brain, self).__init__()

    def sense(self, player, asteroids, bullets):
        """
        Checks the state of the world, and returns a feature
        matrix to be used as input to the AI update function.
        """
        return sense_eight_dir(player, asteroids, 300, shape=LINEAR)

    def think(self, player, bullets, sensor_data):
        """
        Runs the AI algorithm on sensor_data and
        outputs a decision vector in response.

        This AI just spins and shoots when possible.
        """
        return [True, False, True, True]

    def crossover(self, other_brain):
        """
        Combines the network of this AI brain with that of the
        other, exchanging network weights and or structure, and
        returns a new AI brain with the resultant combined network.

        A procedural algorithm is hardcoded, and has no chromosomes
        to crossover, so this method just returns a new instance.
        """
        return Simple_Brain()

    def mutate(self, mutation_rate):
        """
        Mutates the network at the specified rate.

        A procedural algorithm is hardcoded, and has no chromosomes
        to mutate, so this method does nothing.
        """
        return

    def save(self, filename):
        """
        Saves this AI brain to the specified file.

        Since all procedural brains are the same, there is nothing
        to save, so this method just creates an empty file.
        """
        open(filename, "a").close()

    @classmethod
    def load(cls, filename):
        """
        Loads the AI brain from the specified file and returns it.

        Since all procedural brains are the same, there is nothing
        to load, so this method just returns a new instance.
        """
        return Simple_Brain()
