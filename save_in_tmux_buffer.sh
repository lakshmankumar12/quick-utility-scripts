#!/bin/bash

source ~/.bashrc

bufname="$1"
if [ -n "$bufname" ]; then
    tmux set-buffer -b $bufname "$(tmux save-buffer -)"
fi
