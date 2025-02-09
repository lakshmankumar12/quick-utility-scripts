#!/usr/bin/python

def create_pcap_with_headers():
    # PCAP Global Header
    pcap_global_header = bytes([
        0xd4, 0xc3, 0xb2, 0xa1,  # Magic number
        0x02, 0x00, 0x04, 0x00,  # Version numbers
        0x00, 0x00, 0x00, 0x00,  # Timezone
        0x00, 0x00, 0x00, 0x00,  # Sigfigs
        0x00, 0x00, 0x04, 0x00,  # Snaplen
        0x01, 0x00, 0x00, 0x00   # Link-layer type (Ethernet)
    ])

    # Linux Cooked Header v2
    sll2_header = bytes([
        0xe0, 0xe1, 0xa6, 0x67,  # time-stamp sec
        0x00, 0x00, 0x00, 0x00,  # time-stamp micro-second
        0x00, 0x00, 0x00, 0x00,  # snap len - once
        0x00, 0x00, 0x00, 0x00,  # snap len - twice
    ])

    # Ethernet header
    eth_header = bytes([
        0x52, 0x54, 0x00, 0x7f, 0x92, 0x71,    # eth-src
        0x52, 0x54, 0x00, 0x4d, 0x1f, 0x7d,    # eth-dst
        0x08, 0x00,                            # ip-prot

    ])

    # IP Header
    ip_header = bytes([
        0x45,                    # Version (4) + IHL (5)
        0x02,                    # DSCP + ECN
        0x00, 0x00,             # Total Length
        0x02, 0xc3,             # Identification
        0x40, 0x00,             # Flags + Fragment Offset
        0x40,                    # TTL
        0x11,                    # Protocol (17 for UDP)
        0x00, 0x00,             # Header Checksum
        0x0a, 0x00, 0x02, 0x02, # Source IP (10.0.2.2)
        0x0a, 0x00, 0x02, 0x01  # Dest IP (10.0.2.1)
    ])

    # UDP Header
    udp_header = bytes([
        0x96, 0x0c,             # Source Port (38412)
        0xc3, 0x51,             # Dest Port (50001)
        0x00, 0x00,             # length
        0x00, 0x00,             # Checksum
    ])

    # Your NAS PDU
    nas_bytes = bytes.fromhex(
        "7e021c3e0ebb027e006701003" +
        "62e010ec1ffff9128017b002980" +
        "80211001000010810600000000" +
        "83060000000000d00000a00000" +
        "050000100000110000230000240" +
        "012018125090869647465726e6574"
    )

    # Calculate total length
    udp_len = len(udp_header) + len(nas_bytes)
    ip_len = len(ip_header) + udp_len
    eth_len = len(eth_header) + ip_len
    total_len = len(sll2_header) + eth_len

    udp_len_bytes = udp_len.to_bytes(2, byteorder='big')
    ip_len_bytes = ip_len.to_bytes(2, byteorder='big')
    total_len_bytes = eth_len.to_bytes(4, byteorder='little')

    udp_header = udp_header[:4] + udp_len_bytes + udp_header[6:]
    ip_header = ip_header[:2] + ip_len_bytes + ip_header[4:]
    sll2_header = sll2_header[:8] + total_len_bytes + total_len_bytes

    with open("nas.pcap", "wb") as f:
        f.write(pcap_global_header)
        f.write(sll2_header)
        f.write(eth_header)
        f.write(ip_header)
        f.write(udp_header)
        f.write(nas_bytes)

create_pcap_with_headers()
