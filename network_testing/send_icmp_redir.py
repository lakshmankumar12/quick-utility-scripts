#!/usr/bin/env python3
"""Send an ICMP Redirect packet using Scapy."""

import argparse
import sys

from scapy.all import Dot1Q, Ether, IP, ICMP, sendp

# peer_mac=98:fa:9b:99:17:20
# uplinkbr0_mac=aa:de:06:e4:d5:49
# def_gw_ip=10.65.121.1
# ue_ip=10.65.121.16
# peer_ip=10.65.121.20
# vlan=507

# sudo python3 send_icmp_redir.py \
#    --ifc uplink_fwd_br \
#    --src-mac $peer_mac \
#    --dst-mac $uplinkbr0_mac \
#    --src-ip $def_gw_ip \
#    --dst-ip $ue_ip \
#    --gateway-ip $peer_ip \
#    --redir-dst-ip $peer_ip \
#    --vlan $vlan \
#    --code 1 \
#    --count 1


def parse_args():
    p = argparse.ArgumentParser(
        description="Craft and send an ICMP Redirect (Type 5) packet"
    )
    p.add_argument("--ifc", required=True, help="Interface to send the packet from")
    p.add_argument("--src-mac", required=True, help="Source MAC address")
    p.add_argument("--dst-mac", required=True, help="Destination MAC address")
    p.add_argument("--src-ip", required=True, help="Source IP (router issuing redirect)")
    p.add_argument("--dst-ip", required=True, help="Destination IP (host being redirected)")
    p.add_argument("--gateway-ip", required=True, help="New gateway IP (better next hop)")
    p.add_argument("--redir-dst-ip", required=True, help="IP for which the redirect is issued (original destination)")
    p.add_argument(
        "--code", type=int, default=1, choices=[0, 1, 2, 3],
        help="ICMP redirect code: 0=network, 1=host (default), 2=TOS+network, 3=TOS+host",
    )
    p.add_argument("--vlan", type=int, default=0, help="VLAN ID for 802.1Q tag (0 = no tag)")
    p.add_argument("--count", type=int, default=1, help="Number of packets to send")
    return p.parse_args()


def main():
    args = parse_args()

    # Outer packet: from router to the host being redirected
    eth = Ether(src=args.src_mac, dst=args.dst_mac)
    ip = IP(src=args.src_ip, dst=args.dst_ip)
    icmp = ICMP(type=5, code=args.code, gw=args.gateway_ip)

    # Inner IP header: the "original" packet that triggered the redirect
    # (from the redirected host toward the original destination)
    inner_ip = IP(src=args.dst_ip, dst=args.redir_dst_ip, ttl=64)

    if args.vlan:
        pkt = eth / Dot1Q(vlan=args.vlan) / ip / icmp / inner_ip
    else:
        pkt = eth / ip / icmp / inner_ip

    print(f"Sending ICMP Redirect on {args.ifc}:")
    print(f"  {args.src_ip} -> {args.dst_ip}: redirect for {args.redir_dst_ip} via {args.gateway_ip}")
    pkt.show2()

    sendp(pkt, iface=args.ifc, count=args.count, verbose=True)


if __name__ == "__main__":
    main()
