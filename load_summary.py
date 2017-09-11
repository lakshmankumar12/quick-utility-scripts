#!/usr/bin/python

from __future__ import print_function
import os
import psutil

def load_summary():
    load = os.getloadavg()
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_times_percent = psutil.cpu_times_percent()
    print ("Load: {:.2f} Total%: {:.2f} user%: {:.2f} system: {:.2f}".format(load[0],cpu_percent,cpu_times_percent.user,cpu_times_percent.system))

if __name__ == '__main__':
    load_summary()

