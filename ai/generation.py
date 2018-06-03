from ai.utils import META_FILENAME, SUMMARY_FILENAME
import os
import settings

class Generation(object):
    """
    Base class for a generation of AI brains.
    """

    def __init__(self, generation_number, ai_app, brains=None):
        self._generation_number = generation_number
        self._app = ai_app
        self._evaluated = False
        self._results = None
        self._best_brain_id = -1
        if brains is not None:
            self._brains = brains
        else:
            self._brains = self._create_initial_brains(
                    settings.GENERATION_POPULATION)

    def evaluate_fitnesses(self):
        """
        Runs a simulation on each brain in the generation,
        and sets their fitness score to the simulation result.
        """
        best_fitness = -1
        for id, brain in enumerate(self._brains):
            brain.fitness = self._app.run_simulation(brain)
            if brain.fitness > best_fitness:
                self._best_brain_id = id
                best_fitness = brain.fitness
        self._evaluated = True

    def get_evaluation_results(self):
        """
        Returns a dictionary containing brain ID to
        fitness pairs, and some group statistics.
        """
        if not self._evaluated:
            raise RuntimeError("Programmer Error: 'get_evaluation_results' " +
                    "used before generation was evaluated.")
        if self._results is None:
            fitnesses = [brain.fitness for brain in self._brains]
            results = {i: fitness for i, fitness in enumerate(fitnesses)}
            results["mean"] = float(sum(fitnesses)) / len(fitnesses)
            results["max"] = max(fitnesses)
            results["min"] = min(fitnesses)
            self._results = results
        return self._results

    def get_best_brain_id(self):
        """
        Returns the ID of the generation's best brain.
        """
        if not self._evaluated:
            raise RuntimeError("Programmer Error: 'get_best_brain_id' " +
                    "used before generation was evaluated.")
        return self._best_brain_id

    def get_brain(self, id):
        """
        Returns the brain with the provided ID,
        or None if no such brain exists.
        """
        if id < 0 or id >= len(self._brains):
            raise ValueError("No brain exists with ID '%d'." % id)
        return self._brains[id]

    def save(self, dirname):
        """
        Saves this generation to the specified directory.
        """
        if os.path.exists(dirname):
            raise ValueError("Directory to save generation to, " +
                    "'%s', already exists." % dirname)
        os.mkdir(dirname)

        # Save all of the generation's brains
        for id, brain in enumerate(self._brains):
            brain.save(os.path.join(dirname, "%s-%03d-%03d.brn" % \
                    (self.get_algorithm_name().lower(),
                    self._generation_number, id)))

        # Save the best brain in a designated file
        if self._evaluated:
            self._brains[self._best_brain_id].save(os.path.join(dirname,
                    "%s-%03d-best.brn" % (self.get_algorithm_name().lower(),
                    self._generation_number)))

        # Save the evaluation results in a summary file
        if self._evaluated:
            results = self.get_evaluation_results()
            summary_filename = os.path.join(dirname, SUMMARY_FILENAME)
            with open(summary_filename, "w") as summary_file:
                summary_file.write("")
                summary_file.write("%s Generation #%03d SUMMARY\n\n" % \
                        (self.get_algorithm_name(), self._generation_number))
                summary_file.write("Fitness Stats:\n--------------\n")
                summary_file.write("Max: %.2f\nMin: %.2f\nMean: %.2f\n\n" % \
                        (results["max"], results["min"], results["mean"]))
                summary_file.write("Individual Fitnesses:" +
                        "\n---------------------\n")
                for id in range(len(self._brains)):
                    summary_file.write("%03d: %.2f\n" % (id, results[id]))

        # Write the meta file
        meta_filename = os.path.join(dirname, META_FILENAME)
        with open(meta_filename, "w") as meta_file:
            meta_file.write("%s Generation #%03d\n" % \
                    (self.get_algorithm_name(), self._generation_number))
            meta_file.write("Total Brains in this Generation: %d\n" % \
                    len(self._brains))
            meta_file.write("Evaluated: %s\n" % \
                    ("YES" if self._evaluated else "NO"))
            best_brain_id = self._best_brain_id if self._evaluated else -1
            best_fitness = self._brains[best_brain_id].fitness \
                    if self._evaluated else -1
            meta_file.write("Best Brain: %03d\n" % best_brain_id)
            meta_file.write("Best Fitness: %.2f\n" % best_fitness)

    @classmethod
    def load(cls, dirname, ai_app):
        """
        Loads the generation from the specified directory and returns it.
        """
        if not os.path.exists(dirname):
            raise ValueError("Director to load generation from, " +
                    "'%s', does not exist." % dirname)
        meta_filename = os.path.join(dirname, META_FILENAME)
        if not os.path.exists(meta_filename):
            raise ValueError("Could not find meta file " +
                    "'%s' for this generation." % meta_filename)

        # Load the generation's brains
        brains = []
        for filename in os.listdir(dirname):
            if filename.endswith(".brn"):
                brains.append(cls._load_brain(os.path.join(dirname, filename)))

        # Load the metafile
        with open(meta_filename, "r") as meta_file:
            line = meta_file.readline()
            generation_number = int(line.split("#")[1])
            meta_file.readline()
            line = meta_file.readline()
            evaluated = line.split(": ")[1] == "YES"
            if evaluated:
                line = meta_file.readline()
                best_brain_id = int(line.split(": ")[1])
            else:
                best_brain_id = -1

        # Create and return the loaded generation
        loaded_generation = cls(generation_number, ai_app, brains)
        loaded_generation._evaluated = evaluated
        loaded_generation._best_brain_id = best_brain_id
        return loaded_generation

    ##################################################
    #   TO BE IMPLEMENTED BY GENERATION SUBCLASSES
    ##################################################

    def _create_initial_brains(self, num_brains):
        """
        Creates the brains for the initial generation.
        """
        raise NotImplementedError("'_create_initial_brains' should be " +
                "implemented by Generation subclasses.")

    def breed(self):
        """
        Breeds the brains in this generation amongst themselves,
        according to their fitness, and returns the new generation.
        """
        raise NotImplementedError("'breed' should be implemented by " +
                "Generation subclasses.")

    @staticmethod
    def _load_brain(filename):
        """
        Calls the load function of the appropiate
        AI Brain subclass and returns the result.
        """
        raise NotImplementedError("'_load_brain' should be " +
                "implemented by Generation subclasses.")

    @staticmethod
    def get_algorithm_name():
        """
        Returns the name of the algorithm used by the brains.
        """
        raise NotImplementedError("'get_algorithm_name' should be " +
                "implemented by Generation subclasses.")
