#!/bin/bash

port="$1"
if [ -z "$port" ] ; then
    echo "Supply port"
    exit 1
fi

while read line ; do
    pid=$(echo $line | awk '{print $2}')
    echo "Killing pid:$pid in line: $line"
    kill -9 $pid
done < <(lsof -Pn -i4TCP:$port | tail -n +2)

