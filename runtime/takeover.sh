#!/bin/sh
pkill -f 'python3 -u /app/main.py'
nohup python3 -u /app/main.py &>/dev/null &
echo "sh /app/runtime/takeover.sh" | at now + 1 hour
