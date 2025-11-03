#!/bin/bash
BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

python start.py --run-mode=game --player-mode=ai --settings-file=$BASE_DIR/settings.json --game-ai-brain=$BASE_DIR/evaluations-4/_best.brn -s 1
