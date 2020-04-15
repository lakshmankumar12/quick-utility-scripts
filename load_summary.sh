#!/bin/bash

awk '/MemTotal/ { tot=$2;next  } /MemFree/ { free=$2;exit } END {printf "MemFree:%.2f%%\n",free*100.0/tot }' /proc/meminfo > $HOME/.load_summary
