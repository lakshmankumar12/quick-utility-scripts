#!/bin/bash

export TERM=screen-256color-bce

if [ $1 == "-k" ] ; then

  tmux send-keys -t "mac-notes" Escape ":qa" "C-m"
  tmux send-keys -t "what" Escape ":qa" "C-m"
  tmux send-keys -t "nixPow" Escape ":qa" "C-m"
  tmux send-keys -t "lang" Escape ":qa" "C-m"
  tmux send-keys -t "general" Escape ":qa" "C-m"
  tmux send-keys -t "dotf" Escape ":qa" "C-m"
  tmux send-keys -t "vimf" Escape ":qa" "C-m"
  tmux send-keys -t "docker" Escape ":qa" "C-m"

else

  tmux new-session -d -s mac-main
  #tmux move-window -t 20
  tmux new-window -d -k -t 0 -n "mac-notes" -c "$HOME/bitbucket/aryaka-mac-notes"
  tmux new-window -d -t 1 -n "what" -c "$HOME/gitlab/what_repo_is_where"
  tmux new-window -d -t 2 -n "nixPow" -c "$HOME/github/nixPowerToolNotes"
  tmux new-window -d -t 3 -n "lang" -c "$HOME/github/languageNotes"
  tmux new-window -d -t 4 -n "general" -c "$HOME/github/general_reading_notes"
  tmux new-window -d -t 5 -n "dotf" -c "$HOME/github/dotfiles"
  tmux new-window -d -t 6 -n "vimf" -c "$HOME/github/vimfiles"
  tmux new-window -d -t 7 -n "docker" -c "$HOME/github/devbox"

  tmux send-keys -t "mac-notes" "vi" "C-m"
  #tmux send-keys -t "mac-notes" "Esc" ":e scratchpad" "C-m" "Esc" ":tabnew maintodo.org" "C-m"
  tmux send-keys -t "what" "vi" "C-m"
  tmux send-keys -t "nixPow" "vi" "C-m"
  tmux send-keys -t "lang" "vi" "C-m"
  tmux send-keys -t "general" "vi" "C-m"
  tmux send-keys -t "dotf" "vi" "C-m"
  tmux send-keys -t "vimf" "vi" "C-m"
  tmux send-keys -t "docker" "vi" "C-m"

  tmux -2 attach -d -t mac-main
fi
