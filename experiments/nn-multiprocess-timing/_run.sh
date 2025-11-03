#!/bin/bash
echo "--------------"
echo "STARTING TESTS"
echo "--------------"

BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

# Run experiments with different thread counts, and time how long each one took
time ( python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/one-thread --num-threads=1 )
echo ""

time ( python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/four-threads --num-threads=4 )
echo ""

time ( python start.py --run-mode=experiment --settings-file=$BASE_DIR/settings.json --experiment-directory=$BASE_DIR/default-threads )
echo ""

# Save one of the brains for demoing
echo "Saving one brain..."
mkdir -p $BASE_DIR/results
cp $BASE_DIR/default-threads/_best.brn $BASE_DIR/results/_best.brn

# Clean up (we probably don't need these results)
echo "Cleaning up experiment directories..."
rm -rf $BASE_DIR/one-thread
rm -rf $BASE_DIR/four-threads
rm -rf $BASE_DIR/default-threads

echo "--------------"
echo "TESTS FINISHED"
echo "--------------"
