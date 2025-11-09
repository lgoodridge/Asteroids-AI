# Asteroids-AI

A remake of Asteroids, and implementations of several Neural Network algorithms to play it.

Check out our [wiki!](https://github.com/lgoodridge/Asteroids-AI/wiki)

## Installation

This project runs on Python 3, and the dependencies can be installed via `pip`:

    pip install -r requirements.txt

## Example Commands

Use the `start.py` and `manage.py` scripts to interact with the project. All commands have a `--help` option that explains what subcommands or options are available (for example `python start.py --help` or `python manage.py merge --help`).

To play the game yourself run:

    python start.py

To have an AI brain play the game (in this case, a Neural Network brain with no special settings or conditions) run:

    python start.py --run-mode=game --player-mode=ai --algorithm-id=nn --game-ai-brain=path/to/brain.brn

To start an experiment (in this case, genetic evolution of Neural Networks, using a predetermined seed for each simulation) run:

    python start.py --run-mode=experiment --algorithm-id=nn --experiment-directory=experiments/example-nn --use-predetermined-seeds=true

We recommend using the `--help` option to get an idea of what commands are possible and what each command expects. You can also run `python manage.py settings` to view what settings the project supports.

## Running Your Own Experiments

To start a single experiment, use `--run-mode=experiment` as mentioned above, followed by any settings you wish to experiment with:

    python start.py --run-mode=experiment [SETTINGS]

You must at least provide `--algorithm-id`, the type of AI to train during the experiment, and `--experiment-directory`, the folder to output progress and results to. You can also provide settings via a JSON file with `--settings-file=path/to/settings.json`.

To see the available settings, run:

    python manage.py settings

If you want to run multiple experiments back-to-back (for example, to compare multiple values for a setting against each other), a template is provided to aid this. In the `experiments` folder, copy and rename the `template` folder:

    cp -r template example-folder

Then edit `settings.json`, `_run.sh`, and `_demo.sh` as appropriate. There should (probably) be one `python start.py ...` command per experiment, each with a different `--experiment-directory`. Some default settings are provided in the template, but can be adjusted if necessary. See experiments/readme.txt for more information.

## Running Examples

Some pre-made brains, and the commands to the run them are included in the `examples` directory. To see an example brain in action, invoke the `_demo.sh` script in the desired example's folder from the project's root directory. For example:

    ./examples/simple/_demo.sh

If you want to save your own example brain, a template is provided to aid this. In the `examples` folder, copy and rename the `template` folder:

    cp -r template example-folder

Then edit `settings.json` and `_demo.sh` as appropriate. See experiments/readme.txt for more information.

## Running Scripts

Some scripts for running many experiments in sequence, or performing various other tasks are included in the `scripts` directory. These should also be run from the project's root directory. For example:

    ./scripts/test-merge.sh
