#!/bin/bash
BASE_DIR=$(dirname "$0")
BASE_DIR=${BASE_DIR#./}

python start.py --run-mode=game --player-mode=ai --game-algorithm-id=nn --game-ai-brain=$BASE_DIR/results/_best.brn --use-predetermined-seeds=true -s 1
