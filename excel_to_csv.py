#!/usr/bin/python

import openpyxl
import csv
import argparse

def xls_to_csv(infile, outfile):
    wb = openpyxl.load_workbook(infile)
    sh = wb.active
    with open(outfile, 'w', newline="") as f:
        c = csv.writer(f)
        for r in sh.rows:
            c.writerow([cell.value for cell in r])

def get_args():
    parser = argparse.ArgumentParser(description="xls to cvs converter")

    parser.add_argument("-i", "--infile", help="input xls file", action="store", required=True)
    parser.add_argument("-o", "--outfile", help="output csv file", action="store", required=True)

    options = parser.parse_args()
    return options

opts=get_args()
xls_to_csv(opts.infile, opts.outfile)

