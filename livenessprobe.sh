#!/bin/sh
if [ $(ps -ef | grep -v grep | grep 'python3 -u /app/main.py' | wc -l) -lt 1 ]; then
  exit 1
else
  exit 0
fi