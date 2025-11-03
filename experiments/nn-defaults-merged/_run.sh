#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# Run two experiments trained to different seeds
python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/defaults-1 -s 1

python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/defaults-2 -s 2

# Merge the two experiments, and train on a different seed
python manage.py merge $BASE_DIR/defaults-1 $BASE_DIR/defaults-2 $BASE_DIR/results --settings-file=$BASE_DIR/settings.json

python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/results

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
