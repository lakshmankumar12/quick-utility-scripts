#!/bin/bash

export TERM=screen-256color-bce

SESSION_NAME="virtualbox"

names_arr=()
names_arr+=("scratch")
names_arr+=("clip")
names_arr+=("nixPower")
names_arr+=("pynotes")
names_arr+=("dn-space")
names_arr+=("dot")
names_arr+=("quick")
names_arr+=("lang")
names_arr+=("general")

cwd_arr=()
cwd_arr+=("$HOME")
cwd_arr+=("$HOME")
cwd_arr+=("$HOME/github/nixPowerToolNotes")
cwd_arr+=("$HOME/github/pynotes")
cwd_arr+=("$HOME")
cwd_arr+=("$HOME/github/dotfiles")
cwd_arr+=("/host_c/Users/laksh/Downloads/work/github/quick-utility-scripts")
cwd_arr+=("$HOME/github/languageNotes")
cwd_arr+=("$HOME/github/general_reading_notes")

cmds_arr=()
cmds_arr+=("vi scratchpad.md")
cmds_arr+=("clip_anchor")
cmds_arr+=("vi")
cmds_arr+=("vi")
cmds_arr+=("dn")
cmds_arr+=("vi")
cmds_arr+=("vi")
cmds_arr+=("vi")
cmds_arr+=("vi")

if [ "x$1" == "xkill" ] ; then

    for name in ${names_arr[@]} ; do
        tmux send-keys -t "$name" Escape ":qa" "C-m"
        i=$((i+1))
    done

else

    no_sessions=$(tmux list-session 2> /dev/null | wc -l)
    if [[ $no_sessions -ne 0 ]] ; then
        echo "Hey there is already running tmux session"
        tmux list-session
        exit 1
    fi

    mkdir -p /tmp/tmuxbuffer

    tmux -2 -u new-session -d -s $SESSION_NAME
    i=0
    for name in ${names_arr[@]} ; do
        cwd_i=${cwd_arr[$i]}
        cmd_i=${cmds_arr[$i]}
        extra=""
        if [ $i -eq 0 ] ; then
            extra="-k"
        fi
        eval tmux new-window -d "$extra" -t $i -n "$name" -c "$cwd_i"
        tmux send-keys -t "$name" "$cmd_i" "C-m"
        i=$((i+1))
    done

    tmux -2 -u attach -d -t $SESSION_NAME
fi
