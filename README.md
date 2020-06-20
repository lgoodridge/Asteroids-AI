# Asteroids-AI

A remake of Asteroids, and implementations of several Neural Network algorithms to play it.

Check out our [wiki!](https://github.com/lgoodridge/Asteroids-AI/wiki)

## Installation

This project runs on Python 3, and the dependencies can be installed via `pip`:

    pip install -r requirements.txt --pre

The Asteroids game is built with [Pygame](https://www.pygame.org/news), and some systems may only be compatible with certain versions of Pygame. In particular, newer versions of Mac OS currently [require the dev build of Pygame 2](https://github.com/pygame/pygame/issues/1594), so that is listed in the requirements to be safe. This is also why the `--pre` option is present on the install command.

## Example Commands

Use the `start.py` and `manage.py` scripts to interact with the project. All commands have a `--help` option that explains what subcommands or options are available (for example `python start.py --help` or `python manage.py merge --help`).

To play the game yourself run:

    python start.py

To have an AI brain play the game (in this case, a Neural Network brain with no special settings or conditions) run:

    python start.py --run-mode=game --player-mode=ai --game-algorithm-id=nn --game-ai-brain=path/to/brain.brn

To start an experiment (in this case, genetic evolution of Neural Networks, using a predetermined seed for each simulation) run:

    python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=experiments/example-nn --use-predetermined-seed=true

We recommend using the `--help` option to get an idea of what commands are possible and what each command expects. You can also run `python manage.py settings` to view what settings the project supports.

## Running Examples and Scripts

Some pre-made brains, and the commands to the run them are included in the `examples` directory. To see an example brain in action, invoke the `run.sh` script in the desired example's folder from the project's root directory. For example:

    ./examples/simple/run.sh

Some scripts for running multiple tests at once, or performing various other tasks are included in the `scripts` directory. These should also be run from the project's root directory. For example:

    ./scripts/test-merge.sh
