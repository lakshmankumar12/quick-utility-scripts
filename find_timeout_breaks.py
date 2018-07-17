#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime

NormalBreakInfoFile='/Users/lakshman.narayanan/Library/Group Containers/6Z7QW53WB6.com.dejal.timeout/Breaks/Normal.tobreak'

OutputFormat=\
'''\
Timeout
-------
BreakAt: {}
UtcNow:  {}
Now:     {}
Diff:    {}'''

def getNextDueInfo(fileName):
    info = None
    with open (fileName, 'r') as fd:
        info = json.load(fd)
        nextDueStr = info['state']['nextDue']['string']
        nextDue = datetime.datetime.strptime(nextDueStr,"%Y-%m-%dT%H:%M:%SZ")
    return nextDue

def getTimeToBreak(utcBreakTime):
    utcnow = datetime.datetime.utcnow()
    now = datetime.datetime.now()
    diff = utcBreakTime - utcnow
    return (utcnow,now,diff)

if __name__ == "__main__":
    breakAt = getNextDueInfo(NormalBreakInfoFile)
    utcnow, now, diff = getTimeToBreak(breakAt)
    print (OutputFormat.format(breakAt, utcnow, now, diff))
