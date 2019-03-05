#!/usr/bin/env python

# <!--licensing stuff
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# licensing stuff-->

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

import argparse
import sys

### Protocol Implementation

# This is just about the simplest possible protocol
class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.transport.write(data)

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--localip",   help="localip")
    parser.add_argument("-p","--localport", help="localport", type=int)
    cmd_options = parser.parse_args()
    if not cmd_options.localip or not cmd_options.localport:
        print ("you should supply local-ip and local-port")
        parser.print_help()
        sys.exit(1)
    return cmd_options

def main():
    opts = parse_options()
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(opts.localport, f, interface=opts.localip)
    reactor.run()

if __name__ == '__main__':
    main()

