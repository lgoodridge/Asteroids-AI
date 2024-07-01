#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# Run with increasing evaluation simulations
python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/evaluations-1 --use-predetermined-seeds=true --num-evaluation-simulations=1 -s 1

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/evaluations-2 --use-predetermined-seeds=true --num-evaluation-simulations=2 -s 1 -s 2

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/evaluations-4 --use-predetermined-seeds=true --num-evaluation-simulations=4 -s 1 -s 2 -s 3 -s 4

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
