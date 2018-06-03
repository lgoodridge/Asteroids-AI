from ai.ai_brain import AI_Brain
from ai.ai_player import AI_Player
from ai.sensor import sense_eight_dir
from asteroids.utils import LINEAR, HYPERBOLIC
from nn.neural_network import Neural_Network
import json
import os

class NN_Brain(AI_Brain):
    """
    AI brain implementation that uses a neural network for making decisions.
    """

    def __init__(self, network=None):
        super(NN_Brain, self).__init__()
        if network:
            self.network = network
        else:
            self.network = Neural_Network.init_random(8,
                    AI_Player.DECISION_VECTOR_SIZE)

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
        """
        return map(bool, self.network.get_output(sensor_data))

    def crossover(self, other_brain):
        """
        Combines the network of this AI brain with that of the
        other, exchanging network weights and or structure, and
        returns a new AI brain with the resultant combined network.
        """
        return NN_Brain(self.network.crossover(other_brain.network))

    def mutate(self, mutation_rate):
        """
        Mutates the network at the specified rate.
        """
        self.network.mutate(mutation_rate)

    def save(self, filename):
        """
        Saves this AI brain to the specified file.
        """
        with open(filename, "w") as save_file:
            serialized_nn = self.network.serialize()
            save_data = {"Fitness": self.fitness, "Network": serialized_nn}
            json.dump(save_data, save_file)

    @classmethod
    def load(cls, filename):
        """
        Loads the AI brain from the specified file and returns it.
        """
        with open(filename, "r") as load_file:
            load_data = json.load(load_file)
            serialized_nn = load_data["Network"]
            loaded_brain = cls(Neural_Network.deserialize(serialized_nn))
            loaded_brain.fitness = load_data["Fitness"]
            return loaded_brain
