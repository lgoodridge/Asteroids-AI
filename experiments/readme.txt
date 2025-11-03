Contains the results of all ran AI experiments.

========================
CREATING NEW EXPERIMENTS
========================

To create a new experiment, copy the "template" folder into a new folder, then adjust "settings.json", "_run.sh", and "_demo.sh" as appropriate.

It is possible to perform multiple experiment commands in a single "_run.sh" script, and thereby have several settings files and sub-directories. For consistency, and compatibility with certain manage.py commands, the final experiment command should output into a directory named "results", and the settings used to create or run brains from those results named "settings.json".

===============================
RUNNING AND DEMOING EXPERIMENTS
===============================

To run an experiment, execute the experiment's "_run.sh" script from the project's root directory, for example:
$ ./experiments/nn-defaults/_run.sh

To see the experiment's best brain in action, execute the experiment's "_demo.sh" script from the project's root directory, for example:
$ ./experiments/nn-defaults/_demo.sh

================
EXPERIMENT SEEDS
================

Most experiments rely on predetermined seeds for fairness when evaluating brains against each other. If "PREDETERMINED_SEEDS" has multiple values (because brains are run against multiple seeds during fitness evaluation), the first value in the list will be used when demoing the brain.

It is common for less sophisticated models to develop "spin-shoot" behavior (brains that just spin in one direction, and fire at the fastest cadence), and struggle to develop further until a lucky mutation occurs. To discourage this, the template suggests including a predetermined seed of "2" - an arbitrary seed that punishes spin-shoot brains with an asteroid that kills them immediately.
