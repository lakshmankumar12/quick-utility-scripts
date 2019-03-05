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
        for i in range(self.factory.opts.transactions):
            tosend = "This is line:{}".format(i)
            self.sendLine(bytes(tosend, 'utf-8'))
        self.sendLine(self.end)


    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self, opts):
        self.done = Deferred()
        self.opts = opts


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
    parser.add_argument("-c","--count",      help="noofclients", type=int, default=1)
    parser.add_argument("-t","--transactions", help="no of transactions for each client", type=int, default=3)
    cmd_options = parser.parse_args()
    if not cmd_options.localip or not cmd_options.serverport or not cmd_options.serverip:
        print ("you should supply local-ip, serverip and server-port")
        parser.print_help()
        sys.exit(1)
    return cmd_options

def main(reactor):
    opts= parse_options()
    factory = EchoClientFactory(opts)
    reactor.connectTCP(opts.serverip, opts.serverport, factory, bindAddress=(opts.localip,0))
    return factory.done



if __name__ == '__main__':
    task.react(main)
