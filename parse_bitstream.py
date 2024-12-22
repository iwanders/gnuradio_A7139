#!/usr/bin/env python3

import socketserver
import sys
import crcmod
import struct

def hexdump(z):
    return " ".join(f"{i:0>2x}" for i in z)

class A7139BitstreamParser:
    def __init__(self):
        self.buffer = bytearray([])
        
    def feed(self, data):
        # If data is all ones, it's probably boring.
        self.buffer += data
        print(len(self.buffer))
        while True:
            # print(self.buffer)
            # Try to find a preamble;
            preamble = self.buffer.find(bytes([0, 1, 0, 1, 0, 1]))
            # from the preamble, walk right until we encounter 'n' ones.
            all_high = self.buffer.find(bytes([1] * 20), preamble + 1)
            # print(f"p at {preamble}  high at {all_high}")
            if preamble != -1  and all_high != -1:
                packet = self.buffer[preamble:all_high+10]
                self.buffer = self.buffer[all_high + 1:]
                # print(f"Found packet at {packet}  {hexdump(packet)}")
                print(f"{len(packet)}  {hexdump(packet)}")
                continue

            # print(f"Stripping buffer and continuing")
            self.buffer = self.buffer.lstrip(bytes([1]))
            break
        print(len(self.buffer))

def bits_to_bytes(z, endianness=False):
    b = bytearray([])
    if (len(z) % 8 != 0):
        raise RuntimeError(f"incorrect input {len(z)}")
    for block in range(int(len(z) / 8)):
        d = z[block*8: (block + 1) * 8]
        if endianness:
            byte = sum(map(lambda x: x[1] << x[0], enumerate(d)))
        else:
            byte = sum(map(lambda x: x[1] << (7 - x[0]), enumerate(d)))
            
        b.append(byte)
    return bytes(b)

def parse_from_cli():
    a = sys.argv[1]
    d = [int(v, 16) for v in a.split()]
    # Two options:
    # [0]: CRC-CCITT (X 16 + X 12 + X 5 + 1).
    # [1]: CRC-DNP (X 16 + X 13 + X 12 + X 11 + X 10 + X 8 + X 6 + X 5 + X 2 + 1).
    # from crcmod:
    # [1] dnp; crc-16-dnp
    # [0] ccitt one; crc-ccitt-false or crc-aug-ccitt or xmodem or x-25 or crc-16-mcrf4xx... everything with 0x11021 from crcmod basically.

    # payload starts somewhere.
    # crc starts after the payload.
    # preamble of 4 bytes, 4 * 8 = 32
    # id of 4 bytes, 4 * 8 = 32
    # Payload of 'n' bytes.
    # crc of 2 bytes.
    preamble_bytes = 4
    idcode_bytes = 4
    crc_bytes = 2
    total_bytes = int(len(d) / 8)
    print(f"total_bytes: {total_bytes}")
    # crc_length = 2 * 8

    payload_bytes_possible = total_bytes - preamble_bytes - idcode_bytes - crc_bytes
    print(f"payload_bytes_possible: {payload_bytes_possible}")
    for payload_len in range(1, payload_bytes_possible + 1):
        for offset in range(0, len(d) - (payload_len * 8 + crc_bytes * 8)):
            payload = d[offset: offset + payload_len * 8]
            crc_value = d[offset + payload_len * 8: offset + payload_len * 8 + crc_bytes * 8]
            print(payload, crc_value)
            for endianness in [True, False]:
                for c in ["crc-16-dnp", "crc-ccitt-false", "crc-aug-ccitt", "xmodem", "x-25", "crc-16-mcrf4xx", "crc-16-genibus", "crc-16-riello", "kermit"]:
                    for invert in [True, False]:
                        for crc_invert in [True, False]:
                            for stuct_endianness in ["<", ">"]:
                                payload_data = bits_to_bytes(payload, endianness)
                                crc_data = bits_to_bytes(crc_value, endianness)
                                if invert:
                                    payload_data = bytes([~v + 256 for v in payload_data])
                                crc_func = crcmod.predefined.mkCrcFun(c)
                                crc_calc = crc_func(payload_data)
                                crc_calc = bytes(struct.pack(f"{stuct_endianness}H", crc_calc))
                                for crc_invert in [True, False]:
                                    crc_calc = bytes([~v + 256 for v in crc_calc])
                                if crc_data == crc_calc:
                                    print(f"yay at {locals()}")
                                    sys.exit(1)
            
    print(d)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        parse_from_cli()
    sys.exit()
    listen_addr = ('0.0.0.0', 2003)

    parser = A7139BitstreamParser()

    class GnuRadioTCPHandler(socketserver.DatagramRequestHandler):
        def handle(self):
            data = self.rfile.read()
            # print(f"{self.client_address[0]}: {len(data)}: {hexdump(data)}");
            parser.feed(data)

    server = socketserver.UDPServer(listen_addr, GnuRadioTCPHandler)
    server.allow_reuse_address = True 
    server.serve_forever()
