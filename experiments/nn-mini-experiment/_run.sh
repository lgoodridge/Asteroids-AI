#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# An experiment that ends very quickly...
# For testing the experiment framework itself
python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/results

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
