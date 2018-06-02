class AI_Brain(object):
    """
    Base class for the AI Player controllers.
    """

    def __init__(self):
        self.fitness = 0

    def sense(self, player, asteroids, bullets):
        """
        Checks the state of the world, and returns a feature
        matrix to be used as input to the AI decide function.
        """
        raise NotImplementedError("'sense' should be implemented by " +
                "AI_Brain subclasses.")

    def think(self, player, bullets, sensor_data):
        """
        Runs the AI algorithm on sensor_data and
        outputs a decision vector in response.
        """
        raise NotImplementedError("'think' should be implemented by " +
                "AI_Brain subclasses.")

    def crossover(self, other_brain):
        """
        Combines the network of this AI brain with that of the
        other, exchanging network weights and or structure, and
        returns a new AI brain with the resultant combined network.
        """
        raise NotImplementedError("'crossover' should be implemented by " +
                "AI_Brain subclasses.")

    def mutate(self, mutation_rate):
        """
        Mutates the network at the specified rate.
        """
        raise NotImplementedError("'mutate' should be implemented by " +
                "AI_Brain subclasses.")

    def save(self, filename):
        """
        Saves this AI brain to the specified file.
        """
        raise NotImplementedError("'save' should be implemented by " +
                "AI_Brain subclasses")

    @classmethod
    def load(cls, filename):
        """
        Loads the AI brain from the specified file and returns it.
        """
        raise NotImplementedError("'load' should be implemented by " +
                "AI_Brain subclasses.")
