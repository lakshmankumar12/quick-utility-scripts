from scapy.all import *

def ping_generator(dst,count=10,icmp_seq=RandShort(),start_id=0):
    for i in range(count):
        pkt=IP(dst=dst)/ICMP(seq=icmp_seq,id=start_id+i)
        yield pkt
    return





