from ai.activations import get_activation_function, threshold_activation
import json
import numpy as np
import settings

class Neural_Network(object):
    """
    Implementation of a neural network.
    """

    def __init__(self, weight_matrices):
        self._weight_matrices = weight_matrices

    @classmethod
    def init_random(cls, num_inputs, num_outputs):
        """
        Initializes a neural network with random weight values
        that accomodates the specified number of inputs and outputs.
        """
        weight_matrices = []

        # Each hidden layer has a weight matrix of size (# inputs x # outputs),
        # such that row i contains the edge weights from input node i to all
        # output nodes. There is one output layer + all of the hidden layers.
        for i in range(settings.NUM_HIDDEN_LAYERS + 1):

            # The first layer's inputs are the inputs to the neural network,
            # and the last layer's outputs are the network's outputs. All
            # other connections are between hidden layers.
            in_size = num_inputs if i == 0 else settings.HIDDEN_LAYER_SIZE
            out_size = num_outputs if i == settings.NUM_HIDDEN_LAYERS \
                    else settings.HIDDEN_LAYER_SIZE

            # Initialize the weights as random values between -1 and 1.
            # Note: we add an extra row of weights for the bias.
            layer_weights = (np.random.rand(in_size+1, out_size) - 0.5) * 2.0
            weight_matrices.append(layer_weights)

        return cls(weight_matrices)

    def get_output(self, input_values):
        """
        Feeds forward the input values through the network,
        and returns a vector of outputs, all either 0 or 1.
        """
        activation_fn = get_activation_function(settings.HIDDEN_LAYER_ACTIVATION_FN)
        curr_inputs = input_values

        # Compute the outputs of each layer, by dot multiplying the layer's
        # inputs (+ a bias term of 1) with the layer's weight matrix.
        # The output vector sent through the activation function is used
        # as the inputs to the next layer.
        for i in range(settings.NUM_HIDDEN_LAYERS):
            inputs_with_bias = np.append(curr_inputs, 1)
            curr_outputs = np.dot(inputs_with_bias, self._weight_matrices[i])
            curr_inputs = np.array(map(activation_fn, curr_outputs))

        # Compute the final output of the network, by dot multiplying the
        # last hidden layer's outputs with the output layer weights, and
        # sending it through the threshold activation function.
        inputs_with_bias = np.append(curr_inputs, 1)
        raw_outputs = np.dot(inputs_with_bias, self._weight_matrices[-1])
        threshold_fn = lambda x: threshold_activation(x,
                settings.OUTPUT_ACTIVATION_THRESHOLD)
        return map(threshold_fn, raw_outputs)

    def crossover(self, other_nn):
        """
        Mixes the weight matrices of this neural network and the other
        one according to the crossover scheme defined in settings, and
        returns a new Neural Network with this mixed weight matrix.
        """
        if len(self._weight_matrices) != len(other_nn._weight_matrices):
            raise RuntimeError("Programmer Error: Attempted crossover "
                    "between NNs with different numbers of hidden layers.")

        # Crossover each layer's weight matrix
        new_weight_matrices = []
        for i in range(len(self._weight_matrices)):
            if settings.CROSSOVER_MECHANISM == settings.RANDOM:
                weight_matrix = Neural_Network._random_crossover(
                        self._weight_matrices[i], other_nn._weight_matrices[i])
            elif settings.CROSSOVER_MECHANISM == settings.SPLIT:
                weight_matrix = Neural_Network._split_crossover(
                        self._weight_matrices[i], other_nn._weight_matrices[i])
            else:
                raise RuntimeError("Programmer Error: Unsupported crossover " +
                        "mechanism ID '%d'" % settings.CROSSOVER_MECHANISM)
            new_weight_matrices.append(weight_matrix)

        return Neural_Network(new_weight_matrices)

    def mutate(self, mutation_rate):
        """
        Sets values in the weight matrices to random
        values at the specified mutation rate.
        """
        for layer in range(len(self._weight_matrices)):
            for row in range(self._weight_matrices[layer].shape[0]):
                for col in range(self._weight_matrices[layer].shape[1]):
                    if float(np.random.random(1)) < mutation_rate:
                        self._weight_matrices[layer][row][col] = \
                                (float(np.random.random(1)) - 0.5) * 2.0

    def serialize(self):
        """
        Serializes the weight matrices into a 3D list.
        """
        return map(lambda x: x.tolist(), self._weight_matrices)

    @classmethod
    def deserialize(cls, serialized_nn):
        """
        Accepts a serialized neural network object and returns a new
        Neural Network containing the deserialized weight matrices.
        """
        return cls(map(np.asarray, serialized_nn))

    @staticmethod
    def _random_crossover(matrixA, matrixB):
        """
        Returns a fully random crossover between the two matrices,
        where each value in the new matrix is chosen at random from
        either of the two parents.
        """
        if matrixA.shape != matrixB.shape:
            raise RuntimeError("Programmer Error: Attempted crossover "
                    "between matrices with different shapes.")

        # Inherit each value from a parent at random
        new_matrix = np.zeros(matrixA.shape)
        for row in range(new_matrix.shape[0]):
            for col in range(new_matrix.shape[1]):
                parent = np.random.choice([matrixA, matrixB])
                new_matrix[row][col] = parent[row][col]
        return new_matrix

    @staticmethod
    def _split_crossover(matrixA, matrixB):
        """
        Picks a random point in the matrix, and returns a new
        matrix such that all values before that point come from
        parent A, and all other values come from parent B.
        """
        if matrixA.shape != matrixB.shape:
            raise RuntimeError("Programmer Error: Attempted crossover "
                    "between matrices with different shapes.")

        # Pick a random split point
        new_matrix = np.zeros(matrixA.shape)
        split_row = np.random.randint(matrixA.shape[0])
        split_col = np.random.randint(matrixB.shape[0])

        # Inherit all values before that point from
        # first parent, and the rest from the second
        for row in range(new_matrix.shape[0]):
            for col in range(new_matrix.shape[1]):
                parent = matrixA if (row < split_row) and \
                        (col < split_col) else matrixB
                new_matrix[row][col] = parent[row][col]
        return new_matrix
