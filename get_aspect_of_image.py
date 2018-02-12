#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

def add_aspect(known_aspects, w,h):
    if w > h:
        return add_aspect(known_aspects, h, w)
    # h is defintely < w
    known_aspects[round(float(w)/float(h),5)] = "{}:{}, tall".format(w,h)
    known_aspects[round(float(h)/float(w),5)] = "{}:{}, wide".format(w,h)

known_aspects = {}
add_aspect(known_aspects, 2, 3)
add_aspect(known_aspects, 3, 4)
add_aspect(known_aspects, 9, 16)
add_aspect(known_aspects, 5, 8)

def find_aspect(width, height):
    a = round(float(width)/float(height),5)

    if a in known_aspects:
        aspect = known_aspects[a]
    else:
        aspect = "{}".format(a)

    return aspect

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to parge")
    parsed_args = parser.parse_args()

    with Image.open(parsed_args.file) as img:
        width, height = img.size

    aspect = find_aspect(width, height)

    print ("file:{} w:{} h:{} aspect: {}".format(parsed_args.file, width, height, aspect))

