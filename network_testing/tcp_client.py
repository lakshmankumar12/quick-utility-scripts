#!/usr/bin/env python
# <!--licensing stuff
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# licensing stuff-->

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

import argparse
import sys


class EchoClient(LineReceiver):
    end = b"Bye-bye!"

    def connectionMade(self):
        self.sendLine(b"Hello, world!")
        self.sendLine(b"What a fine day it is.")
        self.sendLine(self.end)


    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--localip",   help="localip")
    parser.add_argument("-s","--serverip",  help="serverip")
    parser.add_argument("-p","--serverport", help="serverport", type=int)
    cmd_options = parser.parse_args()
    if not cmd_options.localip or not cmd_options.serverport or not cmd_options.serverip:
        print ("you should supply local-ip, serverip and server-port")
        parser.print_help()
        sys.exit(1)
    return cmd_options

def main(reactor):
    opts= parse_options()
    factory = EchoClientFactory()
    reactor.connectTCP(opts.serverip, opts.serverport, factory, bindAddress=(opts.localip,0))
    return factory.done



if __name__ == '__main__':
    task.react(main)
