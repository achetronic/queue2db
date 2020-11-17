#!/bin/sh
pkill -f python3
nohup python3 -u /app/main.py &>/dev/null &
echo "sh /app/restart.sh" | at now + 10 minutes
