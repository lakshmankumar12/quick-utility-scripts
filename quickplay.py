#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import vlc
import sys
from threading import Thread
from time import sleep
import select

user_in_loop = 1
play_pause_state = 1

class GetUserInput(Thread):
    def run(self):
        global user_in_loop
        global play_pause_state
        global player
        prompt = "Command:"
        print  (prompt, end=""); sys.stdout.flush()
        while (user_in_loop):
            try:
                i, o, e = select.select( [sys.stdin], [], [], 10 )
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
                        time = int(variable[2:])
                        if time < player.get_length() and time > 0:
                            player.set_time(time)
                        else:
                            print ("time:{} is out of range 1-{}".format(time, player.get_length()))
                    else:
                        print("didnt understand:{}".format(variable))
                    print  (prompt, end=""); sys.stdout.flush()
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

player = vlc.MediaPlayer(sys.argv[1])
player.play()
t1 = GetUserInput()
t2 = PlayerWait()
t1.start()
t2.start()
t2.join()
t1.join()
print 
