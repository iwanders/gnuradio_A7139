#!/usr/bin/env python3

import socketserver

def hexdump(z):
    return " ".join(f"{i:0>2x}" for i in z)

class A7139BitstreamParser(socketserver.DatagramRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = []

    def handle(self):
        data = self.rfile.read()
        print(f"{self.client_address[0]}: {len(data)}: {hexdump(data)}");


if __name__ == '__main__':
    listen_addr = ('0.0.0.0', 2003)

    server = socketserver.UDPServer(listen_addr, A7139BitstreamParser)
    server.allow_reuse_address = True 
    server.serve_forever()
