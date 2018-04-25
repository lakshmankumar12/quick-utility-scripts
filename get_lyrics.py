#!/usr/bin/python3

import argparse
import sys

import lyricwikia
import PyLyrics
import lyricsgenius

## to include; https://github.com/johnwmillr/GeniusAPI

parser = argparse.ArgumentParser()
parser.add_argument("title",   help="Song title")
parser.add_argument("author",  help="Author")

parsed_args = parser.parse_args()

def get_lyrics(author, title):
    try:
        with open ('/tmp/genius_client_access_token') as fd:
            token = fd.read().strip()
            api = lyricsgenius.Genius(client_access_token=token)
            song = api.search_song(title,author)
            if song:
                result = song._body['lyrics']
                result += "\n---------------\n" + song.title + '\n' + song.artist + '\n' + song.album + '\n' + song.year
                return (result,'(1) lyricsgenius')
            else:
                raise Exception("Not found")
    except IOError:
        print("/tmp/genius_client_access_token not there?.. Trying lyricwikia")
    except:
        print("Coudlnt' get it off lyricsgenius.. Trying lyricwikia")

    try:
        lyrics = lyricwikia.get_lyrics(author,title)
        return (lyrics, '(2)lyricwikia')
    except:
        print ("Couldn't get it off lyricwikia.. Trying pylyrics")

    try:
        lyrics = PyLyrics.PyLyrics.getLyrics(author,title)
        return (lyrics,'(3)pylyrics')
    except ValueError:
        print ("Couldn't get it off pylyrics for {}, {}".format(title, author))
        sys.exit(1)

(lyrics,source) = get_lyrics(parsed_args.author.strip(),parsed_args.title.strip())
print ("Lyrics from {} for title: {} - author: {}".format(source,parsed_args.title,parsed_args.author))
print (lyrics)
