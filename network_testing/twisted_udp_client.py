#!/usr/bin/env python

# <!--licensing stuff
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# licensing stuff-->

from __future__ import print_function

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import argparse
import sys

def echoClientCallback(arg):
    arg.initiate_a_transaction()

def batchCallBack(arg):
    arg.start_a_batch()

class EchoClientDatagramProtocol(DatagramProtocol):

    def __init__(self, mgr, myinstance):
        DatagramProtocol.__init__(self)
        self.mgr = mgr
        self.myinstance = myinstance
        self.complete = 0
        self.transactions_done = 0

    def startProtocol(self):
        self.transport.connect(self.mgr.opts.serverip, self.mgr.opts.serverport)
        self.initiate_a_transaction()

    def initiate_a_transaction(self):
        tosend = "This is line:{} from instance:{}".format(self.transactions_done, self.myinstance)
        self.transport.write(bytes(tosend, 'utf-8'))

    def datagramReceived(self, datagram, host):
        print('Datagram received: ', repr(datagram))
        self.transactions_done += 1
        if self.transactions_done < self.mgr.opts.transactions:
            reactor.callLater(self.mgr.opts.timeout, echoClientCallback, self)
        else:
            self.complete = 1
            print('done for client:{}'.format(self.myinstance))
            self.mgr.clientDone()

def counter():
    cntr = 1
    while 1:
        yield cntr
        cntr += 1

class Manager:
    def __init__(self, opts):
        self.opts = opts
        self.counter = counter()
        self.clients_created = 0
        self.clients_completed = 0
        if opts.baseport:
            self.localport = opts.baseport
        else:
            self.localport = 0

    def clientDone(self):
        self.clients_completed+=1
        self.maybeDone()

    def maybeDone(self):
        if self.clients_created >= self.opts.count:
            if self.clients_completed == self.clients_created:
                print ("All clients done")
                reactor.stop()

    def start_a_batch(self):
        self.clients_created += self.opts.batch
        for i in range(self.opts.batch):
            protocol = EchoClientDatagramProtocol(self, next(self.counter))
            t = reactor.listenUDP(self.localport, protocol)
            if self.localport:
                self.localport+=1
        if self.clients_created < self.opts.count:
            reactor.callLater(self.opts.batch_timeout, batchCallBack, self)

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--localip",    help="localip")
    parser.add_argument("-b","--baseport",   help="use a baseport", type=int)
    parser.add_argument("-s","--serverip",   help="serverip")
    parser.add_argument("-p","--serverport", help="serverport", type=int)
    parser.add_argument("-c","--count",      help="noofclients", type=int, default=1)
    parser.add_argument("-B","--batch",      help="noofclients-in-one-batch", type=int, default=1)
    parser.add_argument("-T","--batch-timeout", help="timeout between batches", type=float, default=1)
    parser.add_argument("-n","--transactions",  help="no of transactions for each client", type=int, default=3)
    parser.add_argument("-t","--timeout",    help="timeout between each txn in seconds", type=float, default=0)
    cmd_options = parser.parse_args()
    if not cmd_options.localip or not cmd_options.serverport or not cmd_options.serverip:
        print ("you should supply local-ip, serverip and server-port")
        parser.print_help()
        sys.exit(1)
    if cmd_options.batch == 0:
        cmd_options.batch = cmd_options.count
    return cmd_options

def main():
    opts = parse_options()
    mgr = Manager(opts)
    mgr.start_a_batch()
    reactor.run()

if __name__ == '__main__':
    main()

