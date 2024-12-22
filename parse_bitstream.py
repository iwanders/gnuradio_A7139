#!/usr/bin/env python3

import socketserver

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

if __name__ == '__main__':
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
