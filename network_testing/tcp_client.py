#!/usr/bin/env python
# <!--licensing stuff
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# licensing stuff-->

from __future__ import print_function

from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

import argparse
import sys

def echoClientCallback(arg):
    arg.initiate_a_transaction()

class EchoClient(LineReceiver):

    def __init__(self):
        LineReceiver.__init__(self)
        self.inited=0
        self.complete = 0

    def postFactorySetInit(self):
        self.myinstance=next(self.factory.counter)
        self.inited=1
        self.factory.clients_created += 1
        self.transactions_done = 0

    def connectionMade(self):
        if not self.inited:
            self.postFactorySetInit()
        self.initiate_a_transaction()

    def initiate_a_transaction(self):
        tosend = "This is line:{} from instance:{}".format(self.transactions_done, self.myinstance)
        self.sendLine(bytes(tosend, 'utf-8'))

    def lineReceived(self, line):
        print("receive:", line)
        self.transactions_done += 1
        if self.transactions_done < self.factory.opts.transactions:
            reactor.callLater(self.factory.opts.timeout, echoClientCallback, self)
        else:
            self.complete = 1
            self.transport.loseConnection()

    def connectionLost(self, reason):
        print('connection failed for {},reason:{}'.format(self.myinstance,reason.getErrorMessage()))

    def connectionLost(self, reason):
        if not self.complete:
            print('connection lost for {},reason:{}'.format(self.myinstance,reason.getErrorMessage()))
        else:
            print('done for client:{}'.format(self.myinstance))


def counter():
    cntr = 1
    while 1:
        yield cntr
        cntr += 1



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self, opts):
        self.done = Deferred()
        self.opts = opts
        self.counter = counter()
        self.clients_created = 0
        self.clients_completed = 0
        self.errored = 0
        self.errorReason = None

    def clientConnectionFailed(self, connector, reason):
        self.clients_completed+=1
        self.errored = 1
        self.errorReason = reason
        self.maybeDone()

    def clientConnectionLost(self, connector, reason):
        self.clients_completed+=1
        self.maybeDone()

    def maybeDone(self):
        if self.clients_completed == self.clients_created:
            if self.errored:
                self.done.errback(reason)
            else:
                print ("All clients done")
                self.done.callback(None)


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--localip",    help="localip")
    parser.add_argument("-b","--baseport",   help="use a baseport", type=int)
    parser.add_argument("-s","--serverip",   help="serverip")
    parser.add_argument("-p","--serverport", help="serverport", type=int)
    parser.add_argument("-c","--count",      help="noofclients", type=int, default=1)
    parser.add_argument("-n","--transactions", help="no of transactions for each client", type=int, default=3)
    parser.add_argument("-t","--timeout",    help="timeout between each client in seconds", type=float, default=0)
    cmd_options = parser.parse_args()
    if not cmd_options.localip or not cmd_options.serverport or not cmd_options.serverip:
        print ("you should supply local-ip, serverip and server-port")
        parser.print_help()
        sys.exit(1)
    return cmd_options

def main(reactor):
    opts= parse_options()
    factory = EchoClientFactory(opts)
    port = 0
    if opts.baseport:
        port = opts.baseport
    for i in range(opts.count):
        reactor.connectTCP(opts.serverip, opts.serverport, factory, bindAddress=(opts.localip,port))
        if opts.baseport:
            port+=1
    return factory.done

if __name__ == '__main__':
    task.react(main)
