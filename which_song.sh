#!/bin/bash

file="$HOME/Library/Application Support/Google Play Music Desktop Player/json_store/playback.json"

title=$(grep '"title":' "$file" | cut -c19- | sed 's/",$//')
artist=$(grep '"artist":' "$file" | cut -c20- | sed 's/",$//')
album=$(grep '"album":' "$file" | cut -c19- | sed 's/",$//')
art=$(grep '"albumArt":' "$file" | cut -c22- | sed 's/",$//')
playing=$(grep '"playing":' "$file" | cut -c16- | sed 's/,$//' )
current=$(grep '"current":' "$file" | cut -c20- | sed 's/,$//' )
total=$(grep '"current":' "$file" | cut -c18- | sed 's/,$//' )

message=$(echo -en "Title: $title\nArtist: $artist\nAlbum : $album\n")

if [ -n "$1" ] ; then
    terminal-notifier -title "Google Play Music" -message "$message" -contentImage "$art"
else
    cat "$file"
fi
