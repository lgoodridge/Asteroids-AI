#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# An experiment that ends very quickly...
# For testing the experiment framework itself
python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/results --use-predetermined-seeds=true --num-evaluation-simulations=2 -s 1 -s 2 --generation-population=50 --max-generations=5

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
