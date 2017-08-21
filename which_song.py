#!/usr/bin/python

from __future__ import print_function
import json
import os
import pprint

info_file=os.path.expanduser("~/Library/Application Support/Google Play Music Desktop Player/json_store/playback.json")

j = None

with open(info_file,"r") as fd:
    j = json.loads(fd.read())

def get(js,field,def_val="Not set"):
    if field in js:
        return js[field]
    else:
        return def_val

title = get(j["song"],"title","No Title")
artist = get(j["song"],"artist","No Artist")
album = get(j["song"],"album","No Album")
lyrics = get(j,"songLyrics",None)

print("Orig-Json:")
pprint.pprint(j)
print("--"*40)
print("Title:  {}".format(title))
print("Artist: {}".format(artist))
print("Album:  {}".format(album))
print("--"*40)
if lyrics:
    print(lyrics)
else:
    print("No lyrics")


