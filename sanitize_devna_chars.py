import readline
import os
import sys

from devna_charlist import devna_charlist as dcl
from devna_charlist import (
        vowels,
        consonants,
        vowelizers,
        vowelizers2,
        halfizer,
        swaras,
        space,
        newline,
        known_chars
        )

def input_with_prefill(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

def process_line(line):
    conv_chars = []
    for c in line:
        conv_chars.append(known_chars.get(c, "({:s} {:04x})".format(c, ord(c))))
    str_to_show = ' '.join(conv_chars)
    print (f"The line as is was: {str_to_show}")
    while True:
        final = input_with_prefill("Line: ", str_to_show)
        to_save = final.split()
        result = ""
        str_to_show = final
        ok = True
        for i,c in enumerate(to_save):
            if c not in dcl:
                print (f"char:{c} at {i} not a known char")
                ok = False
            else:
                #print (f"Adding char:{c} at {i}")
                result += dcl[c]
        if ok:
            return result


def main():
    result = ""
    clipfile=os.path.join(os.environ['HOME'],"host_c/Users/laksh/Documents/cliptest.txt")
    while True:
        try:
            line = input_with_prefill("Enter the devanagiri line: ", "")
            if len(line.strip()) == 0:
                break
        except EOFError:
            break
        processed = process_line(line)
        print (f"processed line: {processed}")
        with open(clipfile, 'w') as cfd:
            print (f"{processed}", file=cfd)
        result += processed
    return result

result = main()

file=os.path.join(os.environ['HOME'],"host_c/Users/laksh/Downloads/a.txt")
fd=open(file,'w')
print (result, end="", file=fd)
print ("Written to %s"%file)
