#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# Run two experiments trained to different seeds
python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/defaults-1 --use-predetermined-seeds=true -s 1

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/defaults-2 --use-predetermined-seeds=true -s 2

# Merge the two experiments, and train on a different seed
python manage.py merge $BASE_DIR/defaults-1 $BASE_DIR/defaults-2 $BASE_DIR/defaults-merged --experiment-algorithm-id=nn --use-predetermined-seeds=true -s 3

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/defaults-merged --use-predetermined-seeds=true -s 3

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
