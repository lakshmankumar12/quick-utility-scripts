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
        0x84,                   # Protocol (132 for SCTP)
        0x00, 0x00,             # Header Checksum
        0x0a, 0x00, 0x02, 0x02, # Source IP (10.0.2.2)
        0x0a, 0x00, 0x02, 0x01  # Dest IP (10.0.2.1)
    ])

    # sctp Header
    sctp_header = bytes([
        0x96, 0x0c,             # Source Port (38412)
        0x96, 0x0c,             # Dest Port (38412)
        0x01, 0x02, 0x03, 0x04, # verification tag
        0x00, 0x00, 0x00, 0x00, # Checksum
    ])

    data_chunk_header = bytes([
        0x00,                    # Chunk type data(0)
        0x03,                    # Chunk flags (first/last segment)
        0x00, 0x00,              # chunk length
        0x11, 0x12, 0x13, 0x14,  # transmission sequence number
        0x00, 0x01,              # stream identifer
        0x00, 0x01,              # stream seq number
        0x00, 0x00, 0x00, 0x3c   # protcol - NGAP (60)
    ])
    ## and there is chunk padding

    ngap_pdu_till_length = bytes([
        0x00,                    # First octet is always 00
        0x0f,                    # Initial ue message (15)
        0x40,                    # criticality ignore(1), 3bits, 5unused bits
    ])
    #   0x00,                    # length of reset of ngap-pdu ( can be 1 or 2 bytes )

    ngap_till_nas_pdu = bytes([
        0x00, 0x00, 0x05,        # num-ies (5)
        0x00, 0x55,              # ngap-ue-id (85)
        0x00,                    # criticality reject(0), 3bits, 5unused bits
        0x04,                    # length
        0x80, 0x01, 0x00, 0x77,  # ngap-ue-id: 65655
        0x00, 0x26,              # nas-pdu-id (38)
        0x00,                    # criticality reject(0), 3bits, 5unused bits
    ])
    #   0x00, 0x00,              # length of ngap, length of nas-pdu

    ngap_post_nas_pdu = bytes([
        0x00, 0x79,              # user-loc-info-id (121)
        0x00,                    # criticality reject(0), 3bits, 5unused bits
        0x13,                    # length = 19
        0x50,                    # not sure.. preamble?
        0x99, 0x09, 0x99,        # plmn - 999 099
        0x00, 0x00, 0x40,        # cellid
        0x00, 0x20,              # cellid
        0x99, 0x09, 0x99,        # plmn - 999 099 (tai)
        0x00, 0x00, 0x01,        # tac - 1
        0xeb, 0x50, 0x8d, 0x55,  # timestamp
        0x00, 0x5a,              # rrc est cause id (90)
        0x40,                    # criticality ignore(1), 3bits, 5unused bits
        0x01,                    # length
        0x18,                    # mo-signalling(3), 5 bits, 3 bitsunused?
        0x00, 0x70,              # ue-context-request-id (112)
        0x40,                    # criticality ignore(1), 3bits, 5unused bits
        0x01,                    # length
        0x00,                    # requestsed(0)
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
    nas_len = len(nas_bytes)
    ngap_payload_bytes = ngap_till_nas_pdu + \
                    (nas_len+1).to_bytes(1, 'big') + \
                    (nas_len).to_bytes(1, 'big') + \
                    nas_bytes + \
                    ngap_post_nas_pdu
    ngap_payload_len = len(ngap_payload_bytes)
    if ngap_payload_len < 127:
       ngap_len_bytes = ngap_payload_len.to_bytes(1, 'big')
    else:
       ngap_len_bytes = (ngap_payload_len | 0x8000).to_bytes(2, 'big')
       print(f"ngap_len_bytes:{ngap_len_bytes}, ngap_payload_len:{ngap_payload_len}")
    ngap_pdu_bytes = ngap_pdu_till_length + \
                     ngap_len_bytes + \
                     ngap_payload_bytes
    ngap_pdu_len = len(ngap_pdu_bytes)
    pad_size = (4-ngap_pdu_len%4)%4
    data_chunk_padding = b'\x00' * pad_size
    data_chunk_len = len(data_chunk_header) + ngap_pdu_len

    data_chunk = data_chunk_header[:2] + \
                 data_chunk_len.to_bytes(2, 'big') + \
                 data_chunk_header[4:] + \
                 ngap_pdu_bytes + \
                 data_chunk_padding

    ip_len = len(ip_header) + len(data_chunk) + len(sctp_header)
    ip_header = ip_header[:2] + ip_len.to_bytes(2, 'big') + ip_header[4:]
    eth_len = len(eth_header) + ip_len
    eth_len_bytes = eth_len.to_bytes(4, 'little')
    sll2_header = sll2_header[:8] + eth_len_bytes + eth_len_bytes

    with open("nas.pcap", "wb") as f:
        f.write(pcap_global_header)
        f.write(sll2_header)
        f.write(eth_header)
        f.write(ip_header)
        f.write(sctp_header)
        f.write(data_chunk)

create_pcap_with_headers()
