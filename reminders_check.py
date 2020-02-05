#!/usr/bin/env python3

'''
Idea is to have this called by launchctl/cron every minute.
We will scan for $HOME/.current_reminders file, that is a simple
cron style file. And Open a system dialog if a reminder is pending.
If the user needs to remove a reminder, the user must remove it
off the current_reminders file.
'''

import subprocess
import datetime
import logging

def check_asked_entity(asked,current):
    if asked == '*':
        asked = current
    else:
        asked = int(asked)
    return asked

def stale(message, asked_min, asked_hour, current_second, reminders_file):
    display_message = "Old Reminder {}:{}. Now {}:{} : {}. If this is done, remove from {} file".format(
                            asked_hour, asked_min, current_second.hour,current_second.minute,message, reminders_file)
    command='''/usr/bin/osascript -e 'tell application "System Events" to display dialog "{}" with icon note' &'''.format(display_message)
    subprocess.run(command,shell=True)

def expired(message, current_second):
    display_message = "Reminder at {}:{} : {}".format(current_second.hour,current_second.minute,message)
    command='''/usr/bin/osascript -e 'tell application "System Events" to display dialog "{}" with icon caution' &'''.format(display_message)
    subprocess.run(command,shell=True)

def scan_file(reminders_file, current_second):
    with open(reminders_file, 'r') as fd:
        for line in fd:
            if line.startswith('#'):
                continue
            fields = [ i.strip() for i in line.split('|') ]
            if len(fields) != 6:
                logging.error ("Bad line: {}".format(line.strip()))
                continue
            asked_min, asked_hour, asked_day, asked_month, asked_weekday, message = fields
            asked_min = check_asked_entity(asked_min, current_second.minute)
            asked_hour = check_asked_entity(asked_hour, current_second.hour)
            asked_day = check_asked_entity(asked_day, current_second.day)
            asked_month = check_asked_entity(asked_month, current_second.month)
            asked_weekday = check_asked_entity(asked_weekday, (current_second.weekday()+1)%7) # python weekday is 1 ahead of cron's weekday.
            if asked_min     == current_second.minute and \
                   asked_hour    == current_second.hour and \
                   asked_day     == current_second.day and \
                   asked_month   == current_second.month and \
                   asked_weekday == (current_second.weekday()+1)%7:
                logging.debug("expired line: {}".format(line.strip()))
                expired(message, current_second)
            elif (asked_min + asked_hour * 60) < (current_second.minute + current_second.hour * 60):
                logging.debug("stale line: {}".format(line.strip()))
                stale(message, asked_min, asked_hour, current_second, reminders_file)

def main():
    logging.basicConfig(filename="/tmp/reminders_check.log", level=logging.DEBUG)
    current_second = datetime.datetime.now()

    logging.debug("Triggered at {}".format(current_second))

    scan_file("/Users/lakshman_narayanan/.reminders", current_second)

main()
