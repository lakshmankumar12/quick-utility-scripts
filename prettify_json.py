#!/usr/bin/python

from __future__ import print_function
import fileinput, json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename.js",  help="input json (stdin used if skipped)", nargs="?")

parsed_args = parser.parse_args()

print(json.dumps(json.loads("".join(fileinput.input())), sort_keys=True, indent=4))
