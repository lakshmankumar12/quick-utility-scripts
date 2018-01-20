#!/usr/bin/python

import argparse
import sys

import lyricwikia
import PyLyrics


parser = argparse.ArgumentParser()
parser.add_argument("title",   help="Song title")
parser.add_argument("author",  help="Author")

parsed_args = parser.parse_args()

def get_lyrics(author, title):
    try:
        lyrics = lyricwikia.get_lyrics(author,title)
        return (lyrics, '(1)lyricwikia')
    except:
        print ("Couldn't get it off lyricwikia.. Trying pylyrics")

    try:
        lyrics = PyLyrics.PyLyrics.getLyrics(author,title)
        return (lyrics,'(2)pylyrics')
    except ValueError:
        print ("Couldn't get it off pylyrics")
        sys.exit(1)

(lyrics,source) = get_lyrics(parsed_args.author,parsed_args.title)
print ("Lyrics form {} for title: {} - author: {}".format(source,parsed_args.title,parsed_args.author))
print (lyrics.encode('ascii','xmlcharrefreplace'))
