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
import mutagen
import mutagen.id3
import socket

class GlobalState:
    def __init__(self):
        self.running = 1
        self.song_playing = 0
        self.play_pause = 1

        self.files=[]
        self.curr_file_n = 0

        self.starfile = None
        self.dumpfile = None

        self.tot_time = None
        self.curr_time = None
        self.player = None
        self.curr_volume = 100

        self.user_in_so_far = ""

        self.disp_title = ""
        self.disp_time = ""

        self.disp_time = "Not Playig"

def print_current_status(gs):
    update_display(gs)
    current_line="{:3d}|{:50.50s}|{:10s}|{:17s}|{:5s}".format(gs.curr_file_n+1, gs.disp_title, gs.disp_st, gs.disp_time, gs.user_in_so_far)
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
    if len(gs.files[gs.curr_file_n]) > 50:
        gs.disp_title = gs.files[gs.curr_file_n][-50:]
    else:
        gs.disp_title = gs.files[gs.curr_file_n]
    if gs.song_playing != 1:
        gs.disp_title = "Not Playig"
    elif gs.play_pause == 1:
        gs.disp_st = "Playing"
    else:
        gs.disp_st = "Paused"

def get_volume(gs):
    if gs.player:
        gs.curr_volume = gs.player.audio_get_volume()
    return gs.curr_volume

def set_volume(gs, val):
    if val > 0 and val < 100:
        if gs.player:
            gs.player.audio_set_volume(val)
        gs.curr_volume = val

def play_or_pause():
    if gs.play_pause == 1:
        gs.player.pause()
    else:
        gs.player.play()
        sleep(0.5)
    gs.play_pause = 1 - gs.play_pause

helpString=\
'''Keys:
    q        -> exit Player
    Space    -> Play/Pause
    n        -> Next Song
    p        -> Prev Song
    vNN;     -> set volume to NN (0 to 100)
    sNNN;    -> move to NNN sec
    *        -> Add to star file
    gv       -> show current volume
    gp       -> dump current playlist
    Left/Right -> move forward/backward by 10s
    f/r      -> forward/backward by 2s
    F/R      -> forward/backward by 1min
    ?        -> Show this help
'''
def showHelp():
    print (helpString)

def move_by_sec(sec):
    val = gs.player.get_time()
    val += (sec * 1000)
    if val < gs.player.get_length() and val > 0:
        gs.player.set_time(val)

def process_char(gs, char):
    if len(char) == 3:
        if char[2] == 'C':
            #right arrow
            move_by_sec(10)
        elif char[2] == 'D':
            #left arrow
            move_by_sec(-10)
        else:
            pass
        return
    add = 0
    if gs.user_in_so_far == "":
        if char == 'q':
            gs.player.stop()
            gs.song_playing = 0
            gs.running = 0
        elif char == ' ':
            play_or_pause()
        elif char == 'n':
            gs.player.stop()
            gs.song_playing = 0
        elif char == 'p':
            if gs.curr_file_n >= 1:
                gs.player.stop()
                gs.song_playing = 0
                gs.curr_file_n -= 2
        elif char == 'g':
            add = 1
        elif char == 'v' or char == 's':
            add = 1
        elif char == '*':
            starcurrent(gs)
        elif char == 'f':
            move_by_sec(2)
        elif char == 'r':
            move_by_sec(-2)
        elif char == 'F':
            move_by_sec(60)
        elif char == 'R':
            move_by_sec(-60)
        elif char == '?':
            showHelp()
        else:
            print ("\nGot {:d} {}".format(ord(char), char))
            pass
    elif len (gs.user_in_so_far) == 1:
        if gs.user_in_so_far[0] == 'g':
            if char == 'v':
                print ("\ncurrent volume is {}".format(get_volume(gs)))
            elif char == 'p':
                dump_playlist(gs)
                print ("\nCurrent playlist dumped")
            else:
                pass
        elif gs.user_in_so_far[0] == 'v' or gs.user_in_so_far[0] == 's':
            #we expect numbers only
            if char.isdigit():
                add = 1
            elif char == "`" or char == "\n" or char == ';':
                pass
    else:
        if char == "\n" or char == ';':
            if gs.user_in_so_far[0] == 'v':
                val=int(gs.user_in_so_far[1:])
                set_volume(gs, val)
            elif gs.user_in_so_far[0] == 's':
                val=int(gs.user_in_so_far[1:])
                val *= 1000
                if val < gs.player.get_length() and val > 0:
                    gs.player.set_time(val)
        elif char.isdigit():
            add = 1
        else:
            pass
    if add:
        gs.user_in_so_far += char
    else:
        gs.user_in_so_far = ""

def dump_playlist(gs):
    with open (gs.dumpfile, 'w') as fd:
        for n,f in enumerate(gs.files,1):
            if gs.curr_file_n == n-1:
                curr="*"
            else:
                curr=" "
            tit="***"
            art="***"
            alb="***"
            try:
                tags=mutagen.id3.ID3(f, v2_version=3)
                if 'TIT2' in tags:
                    tit=tags['TIT2']
                if 'TALB' in tags:
                    alb=tags['TALB']
                if 'TPE1' in tags:
                    art=tags['TPE1']
            except:
                pass
            print ("{:1s}{:4d}|{:50.50s}|{:50.50s}|{:50.50s}|{:s}".format(curr,n,tit,art,alb,f), file=fd)

def initialize_udp_command_listener(gs, cmd_options):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host="127.0.0.1"
    port=19999
    s.bind((host, port))

    return s

def process_udp_command(s):
    cmd,data = s.recvfrom(1024)
    cmd = cmd.strip()
    if cmd == 'pause':
        play_or_pause()

def starcurrent(gs):
    with open (gs.starfile,'a') as fd:
        try:
            curr_file_name = gs.files[gs.curr_file_n]
            abspath = os.path.abspath(gs.files[gs.curr_file_n])
            fd.write(abspath + '\n')
            print("Starred")
        except:
            print("Couldn't get abs path")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--shuffle", help="Shuffle", action="store_true")
parser.add_argument("-e", "--noerrorsuppress", help="Dont redirect stderr to /tmp/qplayerr.log", action="store_true")
parser.add_argument("-l", "--playlist", help="Treat each arg as a file containing path to files", action="store_true")
parser.add_argument("-t", "--tempmode", help="Dont write playlist file in end", action="store_true")
parser.add_argument("-r", "--starfile", help="write this in starred files", default="/tmp/starred")
parser.add_argument("-d", "--dumpfile", help="use this dump file", default="/tmp/currp.lst")
parser.add_argument("files", nargs="+", help="Files to play!")
cmd_options = parser.parse_args()

files=[]

if cmd_options.playlist:
    for f in cmd_options.files:
        with open (f,'r') as fd:
            for l in fd:
                l = l.strip()
                if os.path.isfile(l):
                    files.append(l)
else:
    for i in cmd_options.files:
        if os.path.isfile(i):
            files.append(i)
        elif os.path.isdir(i):
            for root, dirnames, filenames in os.walk(i):
                for filename in fnmatch.filter(filenames, '*.mp3'):
                    files.append(os.path.join(root, filename))
        else:
            print("{} doesn't seem to be a dir or file".format(i))

if not files:
    print ("Couldn't get even 1 file to play")
    sys.exit(1)

if cmd_options.shuffle:
    import random
    random.seed()
    random.shuffle(files)

# Keep this last in options - so that you
# see any errors
if not cmd_options.noerrorsuppress:
    fd = open('/tmp/qplayerr.log','a')
    os.close(sys.stderr.fileno())
    os.dup2(fd.fileno(), sys.stderr.fileno())


gs = GlobalState()
gs.files = files
gs.curr_file_n = 0
gs.starfile = cmd_options.starfile
gs.dumpfile = cmd_options.dumpfile

if not cmd_options.tempmode:
    dump_playlist(gs)

udp = initialize_udp_command_listener(gs, cmd_options)

while gs.curr_file_n < len(gs.files) and gs.running:
    f = gs.files[gs.curr_file_n]
    gs.player = vlc.MediaPlayer(f)
    r = gs.player.play()
    gs.play_pause = 1
    gs.song_playing = 1
    if r != 0:
        print ("Trouble in playing file {}".format(f))
        gs.curr_file_n += 1
        continue
    set_volume(gs, gs.curr_volume)
    while gs.song_playing and gs.running:
        print_current_status(gs)

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        char = None
        try:
            tty.setraw(sys.stdin.fileno())
            i, o, e = select.select( [sys.stdin, udp], [], [], 1)
            for f in i:
                if f == sys.stdin:
                    char = sys.stdin.read(1)
                    if ord(char) == 27:
                        char = sys.stdin.read(1)
                        if ord(char) == 91:
                            char = sys.stdin.read(1)
                            char = b'\x1b\x5b' + char
                if f == udp:
                    process_udp_command(udp)
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
    gs.curr_file_n += 1

if not cmd_options.tempmode:
    dump_playlist(gs)
