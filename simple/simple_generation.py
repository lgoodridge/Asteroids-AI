from ai.generation import Generation
from simple.simple_brain import Simple_Brain
import os

class Simple_Generation(Generation):
    """
    Defines a generation of Simple AI brains.
    """

    def __init__(self, generation_number, ai_app, brains=None):
        super(Simple_Generation, self).__init__(generation_number,
                ai_app, brains)

    def _create_initial_brains(self, num_brains):
        """
        Creates the brains for the initial generation.
        """
        return [Simple_Brain() for i in range(num_brains)]

    def breed(self):
        """
        Breeds the brains in this generation amongst themselves,
        according to their fitness, and returns the new generation.

        A procedural algorithm is hardcoded, and has nothing to breed,
        so this method just returns a generation containing a new list
        of simple brains.
        """
        brains = [Simple_Brain() for i in range(len(self._brains))]
        return Simple_Generation(self._generation_number+1, self._app,
                brains=brains)

    @staticmethod
    def _load_brain(filename):
        """
        Calls the load function of the appropiate
        AI Brain subclass and returns the result.
        """
        return Simple_Brain.load(filename)

    @staticmethod
    def get_algorithm_name():
        """
        Returns the name of the algorithm used by the brains.
        """
        return "Simple"
