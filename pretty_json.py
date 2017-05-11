#!/usr/bin/python

from __future__ import print_function
import fileinput, json

print(json.dumps(json.loads("".join(fileinput.input())), sort_keys=True, indent=4))
