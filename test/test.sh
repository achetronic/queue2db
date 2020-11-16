#!/usr/bin/env bash

#nohup python3 -u test.py > output.log &
nohup python3 -u test.py &>/dev/null &
echo "running papa"
