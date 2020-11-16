#!/bin/sh
if [ $(pgrep -f 'python3 -u /app/main.py') -lt 1 ]; then
  exit 1
else
  exit 0
fi