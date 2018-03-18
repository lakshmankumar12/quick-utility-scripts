#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import vlc
import sys
from threading import Thread
from time import sleep
import select
import tqdm
import sys, tty, termios
import random
import os
import fnmatch

class GlobalState:
    def __init__(self):
        self.running = 1
        self.song_playing = 0
        self.play_pause = 1
        self.curr_file_name = "Unknown"

        self.tot_time = None
        self.curr_time = None
        self.player = None

        self.user_in_so_far = ""

        self.disp_title = ""
        self.disp_time = ""

        self.disp_time = "Not Playig"

def print_current_status(gs):
    update_display(gs)
    current_line="{:50.50s}|{:10s}|{:17s}|{:5s}".format(gs.disp_title, gs.disp_st, gs.disp_time, gs.user_in_so_far)
    print("\r{}".format(current_line),end="")
    sys.stdout.flush()

def get_time_from_ms(millis):
    seconds=int((millis/1000)%60)
    minutes=int((millis/(1000*60))%60)
    hours=int((millis/(1000*60*60))%24)
    return (hours, minutes, seconds)

def update_display(gs):
    if gs.player:
        gs.tot_time = get_time_from_ms(gs.player.get_length())
        gs.curr_time = get_time_from_ms(gs.player.get_time())
        gs.disp_time = "{:02d}:{:02d}:{:02d}/{:02d}:{:02d}:{:02d}".format(
                gs.curr_time[0],gs.curr_time[1],gs.curr_time[2],
                gs.tot_time[0],gs.tot_time[1],gs.tot_time[2])
    if len(gs.curr_file_name) > 50:
        gs.disp_title = gs.curr_file_name[-50:]
    else:
        gs.disp_title = gs.curr_file_name
    if gs.song_playing != 1:
        gs.disp_title = "Not Playig"
    elif gs.play_pause == 1:
        gs.disp_st = "Playing"
    else:
        gs.disp_st = "Paused"

def process_char(gs, char):
    #print ("processing char:{}, so_far:{}".format(char,gs.user_in_so_far))
    flush = 0
    add = 0
    if gs.user_in_so_far == "":
        if char == 'q':
            flush = 1
            gs.running = 0
        elif char == 'p':
            if gs.play_pause == 1:
                gs.player.pause()
            else:
                gs.player.play()
                sleep(0.5)
            gs.play_pause = 1 - gs.play_pause
            flush = 1
        elif char == 'n':
            gs.player.stop()
            gs.song_playing = 0
        elif char == 'g':
            add = 1
        elif char == 'v' or char == 's':
            add = 1
        else:
            flush = 1
    elif len (gs.user_in_so_far) == 1:
        if gs.user_in_so_far[0] == 'g':
            if char == 'v':
                print ("\ncurrent volume is {}".format(gs.player.audio_get_volume()))
                flush = 1
            else:
                flush = 1
                pass
        elif gs.user_in_so_far[0] == 'v' or gs.user_in_so_far[0] == 's':
            #we expect numbers only
            if char.isdigit():
                add = 1
            elif char == "`" or char == "\n" or char == ';':
                flush = 1
    else:
        if char == "\n" or char == ';':
            if gs.user_in_so_far[0] == 'v':
                val=int(gs.user_in_so_far[1:])
                if val > 0 and val < 100:
                    gs.player.audio_set_volume(val)
                flush = 1
            elif gs.user_in_so_far[0] == 's':
                val=int(gs.user_in_so_far[1:])
                val *= 1000
                if val < gs.player.get_length() and val > 0:
                    gs.player.set_time(val)
        elif char.isdigit():
            add = 1
        else:
            flush = 1
    if flush:
        gs.user_in_so_far = ""
    if add:
        gs.user_in_so_far += char

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--shuffle", help="Shuffle", action="store_true")
parser.add_argument("files", nargs="+", help="Files to play!")
cmd_options = parser.parse_args()

files=[]

for i in cmd_options.files:
    if os.path.isfile(i):
        files.append(i)
    elif os.path.isdir(i):
        for root, dirnames, filenames in os.walk(i):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                files.append(os.path.join(root, filename))
    else:
        print("{} doesn't seem to be a dir or file".format(i))

if cmd_options.shuffle:
    import random
    random.seed()
    random.shuffle(files)

# print ("Enter something:")
# so_far=""
# while 1:
    # i, o, e = select.select( [sys.stdin], [], [], 1)
    # if i:
        # a = getch()
        # print("You entered :{}, so_far: {}".format(a,so_far))
        # if a == '\n':
            # break
        # elif a == '`':
            # so_far = ""
        # elif a == ';':
            # break
        # else:
            # so_far+=a
    # print ("\r{:20s}".format(so_far),end="")
# sys.exit(0)


gs = GlobalState()

for f in files:
    gs.curr_file_name = f
    gs.player = vlc.MediaPlayer(f)
    r = gs.player.play()
    gs.play_pause = 1
    gs.song_playing = 1
    if r != 0:
        print ("some trouble in playing")
        sys.exit(0)
    while gs.song_playing and gs.running:
        print_current_status(gs)

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        char = None
        try:
            tty.setraw(sys.stdin.fileno())
            i, o, e = select.select( [sys.stdin], [], [], 1)
            if i:
                char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if char:
            process_char(gs, char)
        if gs.play_pause == 1:
            if not gs.player.is_playing():
                print ("Play completed")
                gs.song_playing = 0
                break
    del gs.player
    gs.player = None

