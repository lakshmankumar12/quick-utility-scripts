#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import datetime
import os

db="listened_songs"

def parse_song_info(infile):
    title, artist, album = (None, None, None)
    for line in infile:
        line = line.strip()
        if 'Title:' in line:
            title = line[9:]
        elif 'Artist:' in line:
            artist = line[9:]
        elif 'Album' in line:
            album = line[9:]
    if not title or not artist or not album:
        print ("Couldn't spot title/artist/album fully = {}/{}/{}".format(title, artist, album))
        sys.exit(1)
    return (title, artist, album)

def update_in_db(infile, outfile, song, rating):
    (title, artist, album) = song
    to_find = "{}`{}`{}".format(song[0],song[1],song[2])
    found_line = None
    for line in infile:
        if to_find in line:
            found_line = line.strip()
        else:
            outfile.write(line)
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d-%H-%M-%S')
    if found_line:
        ex_val = found_line.split('`')
        if rating == "None":
            rating=ex_val[5]
        final_line="{}`{}`{}`{}\n".format(to_find, ex_val[3], now_str, rating)
    else:
        final_line="{}`{}`{}`{}\n".format(to_find, now_str, now_str, rating)
    outfile.write(final_line)
    return final_line

parser = argparse.ArgumentParser()
parser.add_argument("-f","--filein",  help="use filein instead of stdin")       # captures if --verbosity present or not in arg-list. No arg per-se for this option.
parser.add_argument("-r","--rating",  help="use the rating")       # captures if --verbosity present or not in arg-list. No arg per-se for this option.
parser.add_argument("--songdb",  help="file for song-db, default: listened_songs")       # captures if --verbosity present or not in arg-list. No arg per-se for this option.

cmd_options = parser.parse_args()

close_fd = 0
if cmd_options.filein:
    read_fd = open(cmd_options.filein, 'r')
    close_fd = 1
else:
    read_fd = sys.stdin

if cmd_options.songdb:
    db = cmd_options.songdb

rating="None"
if cmd_options.rating:
    rating=cmd_options.rating

target_file=".{}.out".format(db)

infile=open(db,'r')
outfile=open(target_file,'w')

song = parse_song_info(read_fd)
if close_fd: close(read_fd)

outline = update_in_db(infile, outfile, song, rating)

print ("wrote {} to {}".format(outline,db))

infile.close()
outfile.close()
os.rename(target_file, db)
