#!/usr/bin/python
import dateutil.parser
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("time1", help="time1")
    parser.add_argument("time2", help="time2")
    cmd_options = parser.parse_args()
    return cmd_options


def compute(opts):

    t1_date = dateutil.parser.parse(opts.time1)
    t2_date = dateutil.parser.parse(opts.time2)

    return t2_date - t1_date


opts = parse_args()
diff = compute(opts)
print(f"{diff}")




