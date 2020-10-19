#!/bin/bash

source ~/.bashrc 2> /dev/null

declare -A ttylist
eval ttylist=$(listalltmuxpanes| awk -F\| 'BEGIN {printf "(" } 1 {printf "[\"%s\"]=\"%s-%s-%s\" ",$8,$1,$2,$3} END { printf ")" } ')

existing_files=($(\ls /tmp/vimPos.*))
for i in "${existing_files[@]}" ; do
    pid=${i:12}
    exists=$(ps -o args= -p $pid)
    if [[ $exists == *"nvim"* ]] ; then
        window="unknown"
        tty=$(ps -o tty= -p $pid)
        key="/dev/${tty}"
        if [ ${ttylist[${key}]+_} ] ; then
            window=${ttylist[${key}]}
        fi
        echo "${i} exists in tty:${tty} in window:${window}"
    else
        echo "${i} is no longer around"
    fi
done
