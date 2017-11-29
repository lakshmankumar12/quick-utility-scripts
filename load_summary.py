#!/usr/bin/python

from __future__ import print_function
import os
import psutil

def load_summary():
    load = os.getloadavg()
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_times_percent = psutil.cpu_times_percent()
    op = "L: {:.2f}".format(load[0])
    if cpu_percent > 10.0:
        op += " T: {:.2f}%".format(cpu_percent)
    if cpu_times_percent.user > 10.0:
        op += " U: {:.2f}%".format(cpu_times_percent.user)
    if cpu_times_percent.system > 10.0:
        op += " S: {:.2f}%".format(cpu_times_percent.system)
    #print ("L: {:.2f} T%: {:.2f} U%: {:.2f} S%: {:.2f}".format(load[0],cpu_percent,cpu_times_percent.user,cpu_times_percent.system))
    print (op)

if __name__ == '__main__':
    load_summary()

