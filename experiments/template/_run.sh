#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# Run experiments...
python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/results

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
