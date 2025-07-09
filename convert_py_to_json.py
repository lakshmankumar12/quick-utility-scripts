#!/bin/python

import ast
import json
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='convert python obj dump to json')
    parser.add_argument("-i", "--infile", help="input file", default="")
    parser.add_argument("-o", "--outfile", help="output file", default="")
    cmd_options = parser.parse_args()

    infd = sys.stdin
    outfd = sys.stdout
    if cmd_options.infile != "":
        infd = open(cmd_options.infile, 'r', encoding='utf-8')
    if cmd_options.outfile != "":
        outfd = open(cmd_options.outfile, 'w', encoding='utf-8')

    return infd, outfd

def main():
    infd, outfd = parse_args()
    py_obj = ast.literal_eval(infd.read())
    json.dump(py_obj, outfd, indent=4)

if __name__ == "__main__":
    main()
