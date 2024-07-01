#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

python start.py --run-mode=experiment --experiment-algorithm-id=nn --experiment-directory=$BASE_DIR/defaults --use-predetermined-seeds=true -s 2

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
