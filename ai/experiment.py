"""
Defines functions for running AI experiments.
"""

from __future__ import print_function
from ai.ai_app import AI_App
from ai.generation import Generation
from ai.utils import algorithm_id_to_generation_class, \
        LOG_FILENAME, META_FILENAME
from collections import OrderedDict
from datetime import datetime
import json
import os
import settings
import shutil
import sys
import traceback

def run_experiment():
    """
    Starts or continues an experiment according to
    the configuration parameters set in settings.
    """
    ai_app = AI_App()
    generation_class = algorithm_id_to_generation_class(
            settings.EXPERIMENT_ALGORITHM_ID)
    algorithm_name = generation_class.get_algorithm_name()

    experiment_dir = settings.EXPERIMENT_DIRECTORY
    experiment_name = os.path.basename(os.path.normpath(experiment_dir))
    log_filename = os.path.join(experiment_dir, LOG_FILENAME)
    meta_filename = os.path.join(experiment_dir, META_FILENAME)
    best_brain_filename = os.path.join(experiment_dir, "_best.brn")

    # If the experiment directory doesn't exist
    # yet, create it, and start a new experiment
    if not os.path.exists(experiment_dir):
        print("Initializing experiment directory '%s'..." % experiment_dir)

        # Create the experiment directory, ensuring
        # the parent directory exists beforehand
        parent_dir = os.path.dirname(os.path.normpath(experiment_dir))
        if parent_dir != "" and not os.path.exists(parent_dir):
            raise ValueError("Parent directory '%s' does not exist." %
                    parent_dir)
        os.mkdir(experiment_dir)

        best_fitness = 0
        best_brain_tag = "N/A"
        generation_idx = 0
        stagnation_idx = 0

        # Create the experiment meta file
        meta_dict = OrderedDict({
                "AI Algorithm": algorithm_name,
                "Best Fitness": best_fitness,
                "Best Brain": best_brain_tag,
                "Generation Index": generation_idx,
                "Stagnation Index": stagnation_idx,
        })
        try:
            _write_meta_file(meta_filename, meta_dict)
        except Exception as e:
            print("ERROR CREATING META FILE!")
            raise e

        # Create the experiment log file
        log = open(log_filename, "w")
        current_time_str = datetime.now().strftime("%m/%d/%Y %H:%M")
        print("========================================", file=log)
        print("=     STARTED ON %s" % current_time_str, file=log)
        print("========================================", file=log)
        _write_to_log(log, "Starting experiment '%s':\n" % experiment_name, True)

    # If it does, resume the previous experiment
    elif os.path.isdir(experiment_dir):
        print("Resuming experiment '%s':" % experiment_name)

        # Load the meta data
        try:
            meta_dict = _load_meta_file(meta_filename)
        except Exception as e:
            print("ERROR LOADING META FILE!")
            raise e
        best_fitness = meta_dict["Best Fitness"]
        best_brain_tag = meta_dict["Best Brain"]
        generation_idx = meta_dict["Generation Index"]
        stagnation_idx = meta_dict["Stagnation Index"]

        # Load the log file
        log = open(log_filename, "a")
        current_time_str = datetime.now().strftime("%m/%d/%Y %H:%M")
        print("", file=log)
        print("========================================", file=log)
        print("=     CONTINUED ON %s" % current_time_str, file=log)
        print("========================================", file=log)

    # If the provided location exists, but is
    # not a directory, fail and alert the user
    else:
        raise ValueError(("Experiment Directory '%s' exists, but "
                "is not a directory.") % experiment_directory)

    generation = None
    start_idx = generation_idx

    # If we are continuing an experiment, load the last completed generation
    if generation_idx > 0:
        print("Loading generation %03d... " % (generation_idx-1), end="")
        generation_dirname = os.path.join(experiment_dir,
                "gen%03d" % (generation_idx-1))
        generation = generation_class.load(generation_dirname, ai_app)
        print("Complete")

    # Create and evaluate generations of AI
    # brains until an end condition is reached
    for generation_idx in range(start_idx, settings.MAX_GENERATIONS+1):
        generation_dirname = os.path.join(experiment_dir,
                "gen%03d" % generation_idx)
        generation_meta_filename = os.path.join(generation_dirname,
                META_FILENAME)

        # End the experiment if we've reached an end condition
        if generation_idx == settings.MAX_GENERATIONS:
            _write_to_log(log, "Max generations reached. Ending Experiment.\n")
            break
        if stagnation_idx >= settings.MAX_GENERATIONS_WITHOUT_PROGRESS:
            _write_to_log(log, "Progress has stagnated. Ending Experiment.\n")
            break

        if os.path.isdir(generation_dirname):
            shutil.rmtree(generation_dirname)

        # Create the initial generation, or breed the next generation
        _write_to_log(log, "Generation %d: Creating" % generation_idx)
        try:
            if generation is None:
                generation = generation_class(generation_idx, ai_app)
            else:
                generation = generation.breed()
        except Exception as e:
            _write_to_log(log, "\nERROR CREATING GENERATION %d\n%s" % \
                    (generation_idx, traceback.format_exc()), True)
            return

        # Evaluate the generation
        _write_to_log(log, " - Evaluating")
        try:
            generation.evaluate_fitnesses()
            best_brain_id = generation.get_best_brain_id()
            best_brain = generation.get_brain(best_brain_id)
        except Exception as e:
            _write_to_log(log, "\nERROR EVALUATING GENERATION %d\n%s" % \
                    (generation_idx, traceback.format_exc()), True)
            return
        _write_to_log(log, ": Best Fitness = %.2f - Saving" % best_brain.fitness)

        # Save the generation
        try:
            generation.save(generation_dirname)
        except Exception as e:
            _write_to_log(log, "\nERROR SAVING GENERATION %d\n%s" % \
                    (generation_idx, traceback.format_exc()), True)
            return
        _write_to_log(log, "\n")

        # Determine whether progress was made
        progress_threshold = best_fitness + settings.PROGRESS_IMPROVEMENT_THRESHOLD
        if best_brain.fitness < progress_threshold:
            stagnation_idx += 1

        # Update the best brain and fitness, if necessary
        if best_brain.fitness >= best_fitness:
            best_fitness = best_brain.fitness
            best_brain_tag = "Generation: %03d - ID: %03d" % \
                    (generation_idx, best_brain_id)
            best_brain_filename = os.path.join(experiment_dir, "_best.brn")
            if os.path.exists(best_brain_filename):
                os.remove(best_brain_filename)
            try:
                best_brain.save(best_brain_filename)
            except Exception as e:
                _write_to_log(log, "\nERROR SAVING BEST BRAIN OF GENERATION " + \
                        "%d\n%s" % (generation_idx, traceback.format_exc()), True)
                return

        # Update meta file
        meta_dict = OrderedDict({
                "AI Algorithm": algorithm_name,
                "Best Fitness": best_fitness,
                "Best Brain": best_brain_tag,
                "Generation Index": generation_idx+1,
                "Stagnation Index": stagnation_idx,
        })
        _write_meta_file(meta_filename, meta_dict)

    # Clean up
    ai_app.cleanup_simulation()
    log.close()

def _write_to_log(log, message, force_echo=False):
    """
    Writes message to the provided log.

    If force_echo or EXPERIMENT_ECHO_LOGS is True,
    prints log messages to standard out as well.
    """
    print(message, end="", file=log)
    log.flush()
    if force_echo or settings.EXPERIMENT_ECHO_LOGS:
        print(message, end="")
        sys.stdout.flush()

def _write_meta_file(filename, meta_dict):
    """
    Writes the data contained in meta_dict to the specified file.
    """
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as meta_file:
        json.dump(meta_dict, meta_file, indent=4)

def _load_meta_file(filename):
    """
    Loads the data from the specified file and returns it as a dictionary.
    """
    with open(filename, "r") as meta_file:
        result = json.load(meta_file)
    return result
