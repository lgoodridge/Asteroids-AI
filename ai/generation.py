import os

class Generation(object):
    """
    Base class for a generation of AI brains.
    """

    META_FILENAME = "_meta.txt"

    def __init__(self, generation_number, ai_app, brains=None):
        self._generation_number = generation_number
        self._app = ai_app
        self._evaluated = False
        self._best_brain_id = -1
        if brains is not None:
            self._brains = brains
        else:
            self._brains = _create_initial_brains()

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

    def get_best_brain(self):
        """
        Returns the best brain of the generation.
        """
        if not self._evaluated:
            raise RuntimeError("Programmer Error: 'get_best_brain' " +
                    "used before generation was evaluated.")
        return self._best_brain

    def save(self, dirname):
        """
        Saves this generation to the specified directory.
        """
        if os.path.exists(dirname):
            raise ValueError("Directory to save generation to, " +
                    "'%s', already exists." % dirname)
        os.mkdir(dirname)

        # Save the best brain in a designated file
        if self._evaluated:
            self._brains[self._best_brain_id].save(os.path.join(dirname,
                    "%s-%02d-best.brn" % (self._get_algorithm_name().lower(),
                    self._generation_number)))

        # Save all of the generation's brains
        for id, brain in enumerate(self._brains):
            brain.save(os.path.join(dirname, "%s-%02d-%03d.brn" % \
                    (self._get_algorithm_name().lower(),
                    self._generation_number, id)))

        # Write the meta file
        meta_filename = os.path.join(dirname, Generation.META_FILENAME)
        with open(meta_filename, "w") as meta_file:
            meta_file.write("%s Generation #%d\n" % \
                    (self._get_algorithm_name(), self._generation_number))
            meta_file.write("Total Brains in this Generation: %d\n" % \
                    len(self._brains))
            meta_file.write("Evaluated: %s\n" % \
                    ("YES" if self._evaluated else "NO"))
            best_brain_id = self._best_brain_id if self._evaluated else -1
            best_fitness = self._brains[best_brain_id] if self._evaluated else -1
            meta_file.write("Best Brain: %d\n" % best_brain_id)
            meta_file.write("Best Fitness: %f\n" % best_fitness)

    @classmethod
    def load(cls, dirname, ai_app):
        """
        Loads the generation from the specified directory and returns it.
        """
        if not os.path.exists(dirname):
            raise ValueError("Director to load generation from, " +
                    "'%s', does not exist." % dirname)
        meta_filename = os.path.join(dirname, Generation.META_FILENAME)
        if not os.path.exists(meta_filename):
            raise ValueError("Could not find meta file " +
                    "'%s' for this generation." % meta_filename)

        # Load the generation's brains
        brains = []
        for filename in os.listdir(dirname):
            if filename.endswith(".brn"):
                brains.append(self._load_brain(filename))

        # Load the metafile
        with open(meta_filename, "r") as meta_file:
            line = meta_file.read()
            generation_number = int(line.split("#")[1])
            meta_file.read()
            line = meta_file.read()
            evaluated = line.split(": ")[1] == "YES"
            if evaluated:
                line = meta_file.read()
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

    @staticmethod
    def _get_algorithm_name():
        """
        Returns the name of the algorithm used by the brains.
        """
        raise NotImplementedError("'_get_algorithm_name' should be " +
                "implemented by Generation subclasses.")

    @staticmethod
    def _load_brain(filename):
        """
        Calls the load function of the appropiate
        AI Brain subclass and returns the result.
        """
        raise NotImplementedError("'_load_brain' should be " +
                "implemented by Generation subclasses.")

    def _create_initial_brains(self):
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

