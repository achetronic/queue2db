#!/bin/sh
pkill -f python3
nohup python3 -u /app/main.py &>/dev/null &
echo "sh /app/takeover.sh" | at now + 1 hour
