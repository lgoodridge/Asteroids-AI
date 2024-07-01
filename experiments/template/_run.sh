#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# Run experiments...
python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/<foo>  --use-predetermined-seeds=true --num-evaluation-simulations=2 -s 1 -s 2 ...

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
