from bs4 import BeautifulSoup
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="input file")
    cmd_options = parser.parse_args()
    return cmd_options

opts = parse_args()
with open(opts.file) as fd:
    html = fd.read()

soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)
