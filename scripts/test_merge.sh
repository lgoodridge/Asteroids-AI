#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

mkdir experiments/test-merge

# Run two experiments trained to different seeds
python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=experiments/test-merge/nn-defaults-1 --use-predetermined-seed=true --predetermined-seed=1

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=experiments/test-merge/nn-defaults-2 --use-predetermined-seed=true --predetermined-seed=2

# Merge the two experiments, and train on a different seed
python manage.py merge experiments/test-merge/nn-defaults-1 experiments/test-merge/nn-defaults-2 experiments/test-merge/nn-defaults-merged --experiment-algorithm-id=nn --use-predetermined-seed=true --predetermined-seed=3

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=experiments/test-merge/nn-defaults-merged --use-predetermined-seed=true --predetermined-seed=3

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
