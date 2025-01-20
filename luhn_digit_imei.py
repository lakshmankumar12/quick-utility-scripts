#!/usr/bin/python

import argparse

def calculate_15th_digit(first_14_digits):
    digits = [int(d) for d in str(first_14_digits[:14]).zfill(14)]
    for i in [1,3,5,7,9,11,13]:
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    return (10 - (total % 10)) % 10

def parse_args():
    parser = argparse.ArgumentParser(description='imei-luhn-digit')
    parser.add_argument("imei", help="imei")
    cmd_options = parser.parse_args()
    return cmd_options

def main():
    opts = parse_args()
    digit = calculate_15th_digit(opts.imei)
    print(f'{digit}')

if __name__ == "__main__":
    main()
