from ai.generation import Generation
from nn.nn_brain import NN_Brain
import numpy as np
import os
import settings

class NN_Generation(Generation):
    """
    Defines a generation of Neural Network AI brains.
    """

    def __init__(self, generation_number, ai_app, brains=None):
        super(NN_Generation, self).__init__(generation_number,
                ai_app, brains)

    def _create_initial_brains(self, num_brains):
        """
        Creates the brains for the initial generation.
        """
        return [NN_Brain() for i in range(num_brains)]

    def breed(self):
        """
        Breeds the brains in this generation amongst themselves,
        according to their fitness, and returns the new generation.
        """
        new_brains = []
        num_brains = len(self._brains)

        # Sort the brains by their fitness
        sorted_brains = sorted(self._brains, key=lambda x: x.fitness)

        # Choose the best brains of this generation to survive into the next
        num_survivors = int(num_brains * settings.GENERATION_SURVIVOR_RATE)
        survivors = sorted_brains[:num_survivors]
        new_brains.extend(survivors)

        # Breed half the remaining population from just the chosen survivors
        num_survivor_children = (num_brains - num_survivors) / 2
        survivor_fitnesses = np.array(map(lambda x: x.fitness, survivors))
        survivor_probs = survivor_fitnesses / float(survivor_fitnesses.sum())
        for i in range(num_survivor_children):
            parents = np.random.choice(survivors, 2,
                    replace=False, p=survivor_probs)
            new_brains.append(parents[0].crossover(parents[1]))

        # Breed the remaining population from the entire previous generation
        num_remaining_children = num_brains - num_survivors - num_survivor_children
        all_fitnesses = np.array(map(lambda x: x.fitness, sorted_brains))
        all_probs = all_fitnesses / float(all_fitnesses.sum())
        for i in range(num_remaining_children):
            parents = np.random.choice(sorted_brains, 2,
                    replace=False, p=all_probs)
            new_brains.append(parents[0].crossover(parents[1]))

        # Mutate all members of the new generation
        map(lambda x: x.mutate(settings.MUTATION_RATE), new_brains)

        return NN_Generation(self._generation_number+1, self._app,
                brains=new_brains)

    @staticmethod
    def _load_brain(filename):
        """
        Calls the load function of the appropiate
        AI Brain subclass and returns the result.
        """
        return NN_Brain.load(filename)

    @staticmethod
    def get_algorithm_name():
        """
        Returns the name of the algorithm used by the brains.
        """
        return "NN"
