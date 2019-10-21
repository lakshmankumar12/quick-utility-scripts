#!/usr/bin/env python

"""
A TCP swiss army knife is the making.

Iptables reference:
iptables -A OUTPUT -t filter -p tcp --tcp-flags RST RST -s ${local_ip} -m comment --comment "get-tcp-scapy-working" -j DROP
"""

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import random
import sys
import argparse
import threading
import queue
import tty, termios

def sanitise_args(parser, options):

    if not options.start_client and \
            not options.start_server and \
            not options.reset:
        options.start_client = True

    if options.reset:
        if options.source_port == -1 or \
                options.isn == -1 or \
                options.iack == -1:
            parser.print_help()
            print("\n\nBad Args:")
            print("--reset requires --source-port, --isn, --iack too")
            sys.exit(1)

    if options.start_client:
        if options.destination_port == -1:
            print("\n\nBad Args:")
            print("--start-client requires --destination-port/-d")
            sys.exit(1)

    if options.start_server:
        if options.source_port == -1:
            print("\n\nBad Args:")
            print("--start-server requires --source-port/-s")
            sys.exit(1)

def get_args():

    parser = argparse.ArgumentParser(description="tcpTester: Swiss Army Knife for TCP")

    basic_tcp_args = parser.add_argument_group('Basic TCP arguments')

    basic_tcp_args.add_argument("-I", "--source-interface", help="Interface to sniff for reply", action="store", required=True)
    basic_tcp_args.add_argument("-S", "--source-ip"       , help="Source IP address",            action="store", required=True)
    basic_tcp_args.add_argument("-D", "--destination-ip"  , help="Destination IP address",       action="store", required=True)
    basic_tcp_args.add_argument("-d", "--destination-port", help="Destination TCP port",         action="store", type=int, default=-1)
    basic_tcp_args.add_argument("-s", "--source-port",      help="Source TCP port",              action="store", type=int, default=-1)

    optional_tcp_args = parser.add_argument_group('Optional TCP arguments')

    optional_tcp_args.add_argument(      "--isn",         help="Initial Sequence Number", action="store", type=int, default=-1)
    optional_tcp_args.add_argument(      "--iack",        help="Initial Ack      Number", action="store", type=int, default=-1)
    optional_tcp_args.add_argument(      "--rwin",        help="Initial Window Size",     action="store", type=int, default=8192)
    optional_tcp_args.add_argument(      "--wscale",      help="Window Scale Factor",     action="store", type=int, default=0)
    optional_tcp_args.add_argument(      "--mss",         help="Maximum Segment Size",    action="store", type=int, default=1460)
    optional_tcp_args.add_argument(      "--sack",        help="SACK Permitted",          action="store", type=int, default=0)
    optional_tcp_args.add_argument(      "--tsval",       help="Timestamp Value (TSval)", action="store", type=int, default=0)

    what_to_do_args = parser.add_mutually_exclusive_group()

    what_to_do_args.add_argument("--start-client", help="do a client",       action="store_true")
    what_to_do_args.add_argument("--start-server", help="do a server",       action="store_true")
    what_to_do_args.add_argument("--reset",        help="just send a reset", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    sanitise_args(parser, options)
    return options


class Manager():

    def background_sniffer_thread(self):
        print ("filter string is {}".format(self.filterStr))
        while self.keep_sniffing:
            pkt = sniff(iface=self.ifc, filter=self.filterStr, timeout=2)
            if pkt:
                for p in pkt:
                    self.pktQueue.put(p)
            else:
                #print("Nothing sniffed")
                pass

    def __init__(self, conn):
        #start the sniffer
        self.keep_sniffing = True
        self.pktQueue=queue.Queue()
        self.filterStr="dst {} and tcp and dst port {}".format(conn.src_ip,conn.src_port)
        self.ifc=conn.interface
        self.snifferthr = threading.Thread(target=self.background_sniffer_thread)
        self.snifferthr.start()
        self.connections = []
        self.connections.append(conn)

    def getNextPacket(self, timeout=3, block=True):
        try:
            pkt = self.pktQueue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
        return pkt

    def stopSniffing(self):
        self.keep_sniffing = False
        self.snifferthr.join()

    def abort(self, message=""):
        if message:
            print(message)
        self.stopSniffing()
        print ("isn={}  ; iack={} ; sport={} ; dport={}".format(conn.myseq,conn.peerseq,conn.src_port,conn.dst_port))
        sys.exit(1)

    def run_main_loop(self):
        print ("Running main_loop: Type '?' for help")
        while self.keep_sniffing:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            char = None
            try:
                tty.setraw(sys.stdin.fileno())
                i, o, e = select.select( [sys.stdin], [], [], 0.25)
                for f in i:
                    if f == sys.stdin:
                        char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            if char:
                self.process_char(char)
            while True:
                pkt = self.getNextPacket(block=False)
                if pkt:
                    self.connections[0].process_a_packet(pkt)
                else:
                    break
            self.connections[0].connection_maintenance()

    def print_help(self):
        self.helpString=\
        '''Keys:
            q        -> exit
            ?        -> show this help
            f        -> send fin
            d        -> send data
            R        -> send Reset
            s        -> print connection state details
            h        -> toggle half-close flag (whether to respond to fin or not with a fin)
        '''
        print (self.helpString)

    def process_char(self, char):
        if char == 'q':
            self.abort("user requested exit")
        elif char == '?':
            self.print_help()
        elif char == 'f':
            print ("Initiating a fin")
            self.connections[0].send_fin()
        elif char == 'd':
            print ("sending data")
            self.connections[0].send_data(data="happy")
        elif char == 'R':
            print ("sending reset")
            self.connections[0].send_tcp_reset()
        elif char == 's':
            print ("sending reset")
            print("%s"%self.connections[0])
        elif char == 'h':
            self.connections[0].maintain_half_close = 1 - self.connections[0].maintain_half_close
            print("Connection maintain_half_close is now %d"%self.connections[0].maintain_half_close)


class TcpState:
    CLOSED = 0
    SYN_SENT = 1
    SYN_RCVD = 2
    ESTABLISHED = 3
    LISTEN = 4
    FLOWING = 5
    CLOSE_WAIT = 6
    LAST_ACK = 7
    FIN_WAIT1 = 8
    FIN_WAIT2 = 9
    CLOSING = 10
    TIME_WAIT = 11

    def __init__(self):
        self._value = TcpState.CLOSED

    def getStateValue(self, statevalue):
        if statevalue == TcpState.CLOSED:
            result = "CLOSED"
        elif statevalue == TcpState.SYN_SENT:
            result = "SYN_SENT"
        elif statevalue == TcpState.SYN_RCVD:
            result = "SYN_RCVD"
        elif statevalue == TcpState.ESTABLISHED:
            result = "ESTABLISHED"
        elif statevalue == TcpState.LISTEN:
            result = "LISTEN"
        elif statevalue == TcpState.FLOWING:
            result = "FLOWING"
        elif statevalue == TcpState.CLOSE_WAIT:
            result = "CLOSE_WAIT"
        elif statevalue == TcpState.LAST_ACK:
            result = "LAST_ACK"
        elif statevalue == TcpState.FIN_WAIT1:
            result = "FIN_WAIT1"
        elif statevalue == TcpState.FIN_WAIT2:
            result = "FIN_WAIT2"
        elif statevalue == TcpState.CLOSING:
            result = "CLOSING"
        elif statevalue == TcpState.TIME_WAIT:
            result = "TIME_WAIT"
        else:
            result = "Unknown:%d"%statevalue
        return result

    def __repr__(self):
        return self.getStateValue(self._value)

    def update(self,newvalue):
        if newvalue != self._value:
            self._value = newvalue
            print("Updating state to {}".format(self.getStateValue(self._value)))

    def check(self,value):
        if self._value == value:
            return True
        return False


class Connection():

    def __init__(self, args):
        self.state = TcpState()
        self.conn_dead = False
        self.src_ip = args.source_ip
        self.dst_ip = args.destination_ip
        self.dst_port = args.destination_port
        self.interface = args.source_interface
        self.maintain_half_close = 0

        self.rwin = args.rwin
        if args.isn == -1:
            self.myseq = random.getrandbits(32)
        else:
            self.myseq = args.isn
        if args.iack == -1:
            self.peerseq = 0
        else:
            self.peerseq = args.iack

        self.seqstart = self.myseq
        self.peer_acked = self.myseq
        self.peerseqstart = self.peerseq

        if args.source_port == -1:
            self.src_port = random.randrange(32768,61000)
        else:
            self.src_port = args.source_port

        self.tcp_options = []
        if args.wscale != 0:
            self.tcp_options.append(('WScale', args.wscale))

        if args.mss != 0:
            self.tcp_options.append(('MSS', args.mss))

        if args.sack != 0:
            self.tcp_options.append(('SAckOK', b''))

        self.timestamps = []

        if args.tsval != 0:
            tsval = args.tsval
            tsecr = 0
            self.tcp_options.append(('Timestamp', (tsval, tsecr)))
            print(self.tcp_options)
            self.timestamps = [('Timestamp', (tsval, tsecr))]

        self.mgr = None
        self.ip = self.packet_constructor('IP')

    def update_mgr(self, mgr):
        self.mgr = mgr

    def __repr__(self):
        connection  = "Src-IP/Dest-IP:      {}/{}\n".format(self.src_ip,self.dst_ip)
        connection += "Src-Port/Dst-Port:   {}/{}\n".format(self.src_port,self.dst_port)
        connection += "Intf:                {}\n".format(self.interface)
        connection += "Seq/Ack,  Seq/Peer-acked/me-acked:   {}/{}   {}/{}/{}\n".format(self.myseq, self.peerseq,  self.myseq-self.seqstart, self.peer_acked-self.seqstart, self.peerseq-self.peerseqstart)
        connection += "Tcp-Option:          {}\n".format(self.tcp_options)
        connection += "TimeStamps:          {}\n".format(self.timestamps)
        connection += "State:               {}\n".format(self.state)
        connection += "Half-close flag:     {}\n".format(self.maintain_half_close)
        return connection

    def pkt_printer(self, pkt):
        print ("got a pkt with flags:{} peer-seq:{} peer-ack:{}".format(pkt[TCP].flags,
                                        pkt[TCP].seq - self.peerseqstart,
                                        pkt[TCP].ack - self.seqstart))

    def update_my_ack_with_peer_data(self, peer_pkt):
        to_send_ack = False

        #are we receiving without holes?
        # TODO

        if peer_pkt.haslayer(Raw):
            if peer_pkt[TCP].seq <= self.peerseq:
                if peer_pkt[TCP].seq + len(peer_pkt[Raw].load) > self.peerseq:
                    old_ack = self.peerseq - self.peerseqstart
                    self.peerseq = peer_pkt[TCP].seq + len(peer_pkt[Raw].load)
                    print("Got new data. Setting my-ack from {} to {}".format(old_ack, self.peerseq - self.peerseqstart))
            to_send_ack = True
        if 'F' in peer_pkt[TCP].flags:
            if self.state.check(TcpState.ESTABLISHED) or \
                    self.state.check(TcpState.FIN_WAIT1) or \
                    self.state.check(TcpState.FIN_WAIT2):
                self.peerseq += 1
                to_send_ack = True
                print("Got Fin. Setting my-ack to {}".format(self.peerseq - self.peerseqstart))
        return to_send_ack

    def update_peer_ack(self, peer_pkt):
        if peer_pkt[TCP].ack > self.peer_acked:
            #some new ack.
            self.peer_acked = peer_pkt[TCP].ack
            print("Got peer-ack to {}. My seq: {}".format(self.peer_acked - self.seqstart, self.myseq-self.seqstart))


    def packet_constructor(self, packet_flags, load_data=""):
        src_ip = self.src_ip
        dst_ip = self.dst_ip
        src_port = self.src_port
        dst_port = self.dst_port
        seq = self.myseq
        ack = self.peerseq
        rwin = self.rwin
        tcp_options = self.tcp_options
        timestamps = self.timestamps

        if packet_flags == 'IP':
            packet = IP(src=src_ip, dst=dst_ip)
        elif packet_flags == 'S':
            packet = TCP(sport=src_port, dport=dst_port, flags='S', seq=seq,
                         window=rwin, options=tcp_options)
            if self.state.check(TcpState.CLOSED):
                self.myseq += 1
        else:
            packet = TCP(sport=src_port, dport=dst_port, flags=packet_flags,
                         seq=seq, ack=ack, window=rwin, options=timestamps)
            if len(load_data):
                packet = packet/Raw(load=load_data)
                oldseq = self.myseq - self.seqstart
                self.myseq += len(packet[Raw].load)
                print ("Moving my seq from {} to {}".format(oldseq, self.myseq - self.seqstart))

        return packet

    def send_tcp_reset(self):
        print("Sending TCP Reset")
        rst = self.packet_constructor('R')
        send(self.ip/rst, verbose=0)
        self.state.update(TcpState.CLOSED)
        self.conn_dead = True

    def start_client_handshake(self):
        if not self.state.check(TcpState.CLOSED):
            print("Huh cant start handshake when state is not CLOSED. Its {}".format(self.state))

        syn = self.packet_constructor('S')

        # send SYN
        print ("sending syn")
        synPacket=self.ip/syn
        send(synPacket, verbose=0)
        self.state.update(TcpState.SYN_SENT)

        pkt = mgr.getNextPacket()
        if not pkt:
            mgr.abort("no pkt after syn")

        if pkt[TCP].flags != "SA":
            mgr.abort("not syn-ack after syn")
            sys.exit(1)

        print("Got syn-ack")
        self.peerseqstart = pkt[TCP].seq
        self.peerseq = pkt[TCP].seq + 1
        self.peer_acked = pkt[TCP].ack
        self.state.update(TcpState.ESTABLISHED)

        # send ACK to complete the establishing handshake
        print ("Sending ack")
        ack = self.packet_constructor('A')
        send(self.ip/ack, verbose=0)

    def send_fin(self):
        if self.state.check(TcpState.ESTABLISHED):
            next_state = TcpState.FIN_WAIT1
        elif self.state.check(TcpState.CLOSE_WAIT):
            next_state = TcpState.LAST_ACK
        else:
            print("Not a good state to send fin")
            return

        fin = self.packet_constructor('FA')
        send((self.ip/fin), verbose=0)
        self.myseq += 1
        self.state.update(next_state)

    def send_data(self, data):
        if not self.state.check(TcpState.ESTABLISHED) and \
                not self.state.check(TcpState.CLOSE_WAIT):
            print("Data can't be sent in state:{}".format(self.state))
            return
        data_pkt = self.packet_constructor('A',load_data=data)
        send((self.ip/data_pkt), verbose=0)

    def wait_for_syn(self):
        if not self.state.check(TcpState.CLOSED):
            print ("Cant wait_for_synack in state:{}".format(self.state))
            mgr.abort()

        print ("Waiting for a syn")
        while True:
            pkt = mgr.getNextPacket(timeout=10)
            if not pkt:
                print ("No pkt received in 10s. Press C-c twice to exit")
            else:
                break

        if pkt[TCP].flags != 'S':
            print ("Not a syn pkt")
            self.pkt_printer(pkt)
            mgr.abort()

        print ("Got a syn pkt")
        self.peerseqstart = pkt[TCP].seq
        self.peerseq = pkt[TCP].seq + 1
        self.peer_acked = self.seqstart
        self.state.update(TcpState.ESTABLISHED)
        self.dst_port = pkt[TCP].sport

        synack = self.packet_constructor('SA')
        send(self.ip/synack, verbose=0)
        self.myseq += 1

        while True:
            pkt = mgr.getNextPacket(timeout=5)
            if not pkt:
                print ("No response to syn-ack for 5s")
                mgr.abort()
            if pkt[TCP].flags == 'S':
                print ("Got a Syn again")
                continue
            if 'A' not in pkt[TCP].flags:
                print ("Not getting ack")
                self.pkt_printer(pkt)
                mgr.abort()
            if pkt[TCP].ack != self.peer_acked + 1:
                print ("Wrong ack number! Expected:{}, Got:{}",
                        self.peer_acked+1,
                        pkt[TCP].ack)
                continue
            break

        self.peer_acked = pkt[TCP].ack
        self.state.update(TcpState.ESTABLISHED)
        to_send_ack = self.update_my_ack_with_peer_data(pkt)
        if to_send_ack:
            #not sure, if user wants to send data/fin on this too.
            # to support that
            ack = self.packet_constructor('A')
            send(self.ip/ack, verbose=0)

    def get_a_packet_and_process(self, mustGet=True, timeout=3):
        pkt = mgr.getNextPacket(timeout=timeout)
        if not pkt:
            if mustGet:
                mgr.abort("No pkt received")
            else:
                return None
        self.process_a_packet(pkt)

    def process_a_packet(self, pkt):

        self.pkt_printer(pkt)

        if 'R' in pkt[TCP].flags:
            print("Received a peer reset")
            self.state.update(TcpState.CLOSED)
            self.conn_dead = True
            return

        to_send_ack = self.update_my_ack_with_peer_data(pkt)

        if 'A' in pkt[TCP].flags:
            self.update_peer_ack(pkt)
            if self.state.check(TcpState.FIN_WAIT1):
                if self.peer_acked == self.myseq:
                    self.state.update(TcpState.FIN_WAIT2)
                else:
                    print("Peer yet to ack fin: my-seq:{}, peer_acked:{}".format(
                                        self.myseq - self.seqstart,
                                        self.peer_acked - self.seqstart))
            elif self.state.check(TcpState.CLOSING):
                if self.peer_acked == self.myseq:
                    self.state.update(TcpState.TIME_WAIT)

        if 'F' in pkt[TCP].flags:
            if self.state.check(TcpState.ESTABLISHED):
                self.state.update(TcpState.CLOSE_WAIT)
            elif self.state.check(TcpState.FIN_WAIT1):
                self.state.update(TcpState.CLOSING)
            elif self.state.check(TcpState.FIN_WAIT2):
                self.state.update(TcpState.TIME_WAIT)

        if to_send_ack:
            #not sure, if user wants to send data/fin on this too.
            # to support that
            ack = self.packet_constructor('A')
            send(self.ip/ack, verbose=0)

    def is_peer_fin_received(self):
        if self.state.check(TcpState.CLOSING) or \
                self.state.check(TcpState.CLOSING) or \
                self.state.check(TcpState.CLOSE_WAIT):
            return True
        return False

    def connection_maintenance(self):
        if self.state.check(TcpState.CLOSE_WAIT):
            if self.maintain_half_close == 0:
                print ("We got a fin. Responding with a fin")
                self.send_fin()
        elif self.state.check(TcpState.LAST_ACK):
            if not self.conn_dead:
                self.conn_dead=True
                print ("Done with a server connection")


if __name__ == "__main__":
    args = get_args()
    conn = Connection(args)
    print("Created connection:\n{}".format(conn))
    mgr = Manager(conn)
    conn.update_mgr(mgr)
    if args.reset:
        conn.send_tcp_reset()
        mgr.abort()
    elif args.start_client:
        conn.start_client_handshake()
        print ("Done with 3wHS")
        mgr.run_main_loop()
    elif args.start_server:
        conn.wait_for_syn()
        mgr.run_main_loop()
