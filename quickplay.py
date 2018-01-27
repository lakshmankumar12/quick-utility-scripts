#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import vlc
import sys
from threading import Thread
from time import sleep
import select
import tqdm

user_in_loop = 1
play_pause_state = 1

class GetUserInput(Thread):
    def run(self):
        global user_in_loop
        global play_pause_state
        global player
        pbar_tot = 0
        while pbar_tot == 0:
            pbar_tot = player.get_length()
            prompt = "Total: {}-{}s".format(pbar_tot/60000, (pbar_tot%60000)/1000)
            sleep(0.5)
        pbar_sofar = 0
        with tqdm.tqdm(total=pbar_tot) as pbar:
            pbar.set_description(prompt)
            while (user_in_loop):
                try:
                    i, o, e = select.select( [sys.stdin], [], [], 1)
                    curr_time = player.get_time()
                    pbar_new = curr_time - pbar_sofar
                    if (pbar_new > 0):
                        to_set = {}
                        to_set["curr"] = "{}:{}s".format(curr_time/60000, (curr_time%60000)/1000)
                        pbar.set_postfix(to_set, refresh=False)
                        pbar.update(pbar_new)
                        pbar_sofar += pbar_new
                    if (i):
                        variable=sys.stdin.readline().strip()
                        if variable == 'q':
                            user_in_loop = 0
                            break
                        elif variable == 'p':
                            player.pause()
                            play_pause_state = 1 - play_pause_state
                        elif variable == 'l':
                            print("Length:{} , Time:{}".format(player.get_length(), player.get_time()))
                        elif variable == 'gv':
                            print ("current volume is {}".format(player.audio_get_volume()))
                        elif variable.startswith('v '):
                            level = int(variable[2:])
                            if level:
                                print("setting volume to {}".format(level))
                                player.audio_set_volume(level)
                        elif variable.startswith('s '):
                            mn, sc = map(int, variable[2:].split(' '))
                            tot = (mn * 60 + sc) * 1000
                            if tot < player.get_length() and tot > 0:
                                player.set_time(tot)
                            else:
                                print ("time:{} is out of range 1-{}".format(time, player.get_length()))
                        else:
                            print("didnt understand:{}".format(variable))
                except:
                    user_in_loop = 0
                    raise

class PlayerWait(Thread):
    def run(self):
        global user_in_loop
        global play_pause_state
        global player
        while (user_in_loop):
            sleep(1)
            if play_pause_state == 1:
                if not player.is_playing():
                    print ("Play completed")
                    user_in_loop = 0


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file",   help="File to play!")
parsed_args = parser.parse_args()

player = vlc.MediaPlayer(parsed_args.file)
player.play()
t1 = GetUserInput()
t2 = PlayerWait()
t1.start()
t2.start()
t2.join()
t1.join()
