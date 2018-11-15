#!/bin/bash

export TERM=screen-256color-bce

if [ $1 == "-k" ] ; then

  tmux send-keys -t "mac-notes" Escape ":qa" "C-m"
  tmux send-keys -t "what" Escape ":qa" "C-m"
  tmux send-keys -t "nixPow" Escape ":qa" "C-m"
  tmux send-keys -t "lang" Escape ":qa" "C-m"
  tmux send-keys -t "general" Escape ":qa" "C-m"
  tmux send-keys -t "pynotes" Escape ":qa" "C-m"
  tmux send-keys -t "dotf" Escape ":qa" "C-m"
  tmux send-keys -t "vimf" Escape ":qa" "C-m"
  tmux send-keys -t "docker" Escape ":qa" "C-m"
  tmux send-keys -t "quick" Escape ":qa" "C-m"
  tmux send-keys -t "mio-grab" Escape ":qa" "C-m"
  tmux send-keys -t "mp3" Escape ":qa" "C-m"
  tmux send-keys -t "mac-script" Escape ":qa" "C-m"
  tmux send-keys -t "ppl" Escape ":qa" "C-m"
  tmux send-keys -t "free-term" Escape ":qa" "C-m"

else

  tmux new-session -d -s mac-main
  #tmux move-window -t 20
  tmux new-window -d -k -t 0 -n "mac-notes" -c "$HOME/bitbucket/aryaka-mac-notes"
  tmux new-window -d -t 1 -n "what" -c "$HOME/gitlab/what_repo_is_where"
  tmux new-window -d -t 2 -n "nixPow" -c "$HOME/github/nixPowerToolNotes"
  tmux new-window -d -t 3 -n "lang" -c "$HOME/github/languageNotes"
  tmux new-window -d -t 4 -n "general" -c "$HOME/github/general_reading_notes"
  tmux new-window -d -t 5 -n "pynotes" -c "$HOME/github/pynotes"
  tmux new-window -d -t 6 -n "dotf" -c "$HOME/github/dotfiles"
  tmux new-window -d -t 7 -n "vimf" -c "$HOME/github/vimfiles"
  tmux new-window -d -t 8 -n "docker" -c "$HOME/github/devbox"
  tmux new-window -d -t 9 -n "quick" -c "$HOME/github/quick-utility-scripts"
  tmux new-window -d -t 10 -n "mio-grab" -c "$HOME/gitlab/mio-track-grab"
  tmux new-window -d -t 11 -n "mp3" -c "$HOME/github/mp3_tag_editor"
  tmux new-window -d -t 12 -n "mac-script" -c "$HOME/github/mac_scripts"
  tmux new-window -d -t 13 -n "ppl" -c "$HOME/gitlab/office-api-try/python3-connect-rest-sample"
  tmux new-window -d -t 14 -n "free-term" -c "$HOME"

  tmux send-keys -t "mac-notes" "vi" "C-m"
  tmux send-keys -t "what" "vi" "C-m"
  tmux send-keys -t "nixPow" "vi" "C-m"
  tmux send-keys -t "lang" "vi" "C-m"
  tmux send-keys -t "general" "vi" "C-m"
  tmux send-keys -t "pynotes" "vi" "C-m"
  tmux send-keys -t "dotf" "vi" "C-m"
  tmux send-keys -t "vimf" "vi" "C-m"
  tmux send-keys -t "docker" "vi" "C-m"
  tmux send-keys -t "quick" "vi" "C-m"
  tmux send-keys -t "mio-grab" "vi" "C-m"
  tmux send-keys -t "mp3" "vi" "C-m"
  tmux send-keys -t "mac-script" "vi" "C-m"
  tmux send-keys -t "ppl" "vi" "C-m"
  tmux send-keys -t "free-term" "C-m"

  tmux new-session -d -s second

  tmux -2 attach -d -t mac-main
fi
