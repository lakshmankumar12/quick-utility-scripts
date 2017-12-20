#!/usr/bin/python

import PyLyrics
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("title",   help="Song title")
parser.add_argument("author",  help="Author")

parsed_args = parser.parse_args()

print(PyLyrics.PyLyrics.getLyrics(parsed_args.author,parsed_args.title))
