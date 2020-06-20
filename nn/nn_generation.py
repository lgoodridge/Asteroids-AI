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

        # Organize brains into fitness buckets
        brain_buckets = {}
        for brain in self._brains:
            brain_buckets[brain.fitness] = \
                    brain_buckets.get(brain.fitness, []) + [brain]

        # Choose a single brain for each fitness value to represent that bucket
        sorted_fitnesses = sorted(brain_buckets.keys(), reverse=True)
        sorted_brains = [np.random.choice(brain_buckets[fitness])
                for fitness in sorted_fitnesses]

        # Choose the best brains of this generation to survive into the next
        num_survivors = int(num_brains * settings.GENERATION_SURVIVOR_RATE)
        survivors = sorted_brains[:num_survivors]
        new_brains.extend(survivors)

        # Breed half the remaining population from just the chosen survivors
        num_survivor_children = int((num_brains - len(new_brains)) / 2)
        survivor_fitnesses = np.array([x.fitness for x in survivors])
        survivor_probs = survivor_fitnesses / float(survivor_fitnesses.sum())
        for i in range(num_survivor_children):
            parents = np.random.choice(survivors, 2,
                    replace=False, p=survivor_probs)
            new_brains.append(parents[0].crossover(parents[1]))

        # Breed the remaining population from the entire previous generation
        num_remaining_children = num_brains - len(new_brains)
        all_probs = np.array(sorted_fitnesses) / sum(sorted_fitnesses)
        for i in range(num_remaining_children):
            parents = np.random.choice(sorted_brains, 2,
                    replace=False, p=all_probs)
            new_brains.append(parents[0].crossover(parents[1]))

        # Determine the number of champions in the previous generation
        if settings.CHAMPION_SELECTION_SCHEME == settings.STATIC:
            num_champions = settings.NUM_CHAMPIONS
        elif settings.CHAMPION_SELECTION_SCHEME == settings.PERFORMANCE:
            mean_fitness = sum(sorted_fitnesses) / len(sorted_fitnesses)
            threshold = mean_fitness * settings.CHAMPION_THRESHOLD_MULTIPLIER
            for num_champions in range(num_survivors):
                if survivor_fitnesses[num_champions] < threshold:
                    break

        # Mutate all members of the new generation,
        # except the previous generation's champion(s)
        map(lambda x: x.mutate(settings.MUTATION_RATE),
                new_brains[num_champions:])

        return NN_Generation(self._generation_number+1, self._app,
                brains=new_brains)

    @staticmethod
    def load_brain(filename):
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
