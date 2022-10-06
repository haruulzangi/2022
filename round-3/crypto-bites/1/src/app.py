# -*- coding: utf-8 -*-
import struct
import socket
import socketserver


class InputOverflowException(Exception):
    pass


class InputUnderflowException(Exception):
    pass


def read_message(s, max_input_length=1024*16) -> bytes:
    received_buffer = s.recv(8)
    if len(received_buffer) < 8:
        raise InputUnderflowException(
            'Failed to receive data: the received length is less than 8 bytes long')
    to_receive = struct.unpack('<Q', received_buffer[0:8])[0]
    if to_receive > max_input_length:
        raise InputOverflowException(
            'Failed to receive data: requested to accept too much data')
    received_buffer = b''

    while len(received_buffer) < to_receive:
        data = s.recv(to_receive - len(received_buffer))
        if len(data) == 0:
            raise InputUnderflowException(
                'Failed to receive data: the pipe must have been broken')
        received_buffer += data
        if len(received_buffer) > max_input_length:
            raise InputOverflowException(
                'Failed to receive data: accepted too much data')

    return received_buffer


def send_message(s, message: bytes):
    send_buffer = struct.pack('<Q', len(message)) + message
    s.sendall(send_buffer)


class ForkingTCPServer(socketserver.ForkingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketserver.TCPServer.server_bind(self)


encrypted_flag = open('flag.txt.enc', 'rb').read()
encryption_key = 'HaruulZangi2022'


class ServiceServerHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)

    def handle(self):
        try:
            while True:
                cmd = read_message(self.request)
                if cmd == b'DATA':
                    send_message(
                        self.request, encrypted_flag)
                elif cmd == b'KEY':
                    send_message(self.request, encryption_key.encode('ascii'))
                elif cmd == b'CMD':
                    send_message(
                        self.request, 'openssl enc -aes-256-cbc -in flag.txt -out flag.txt.enc')
                elif cmd == b'EXIT':
                    send_message(self.request, b'OK')
                    break
                else:
                    raise Exception(
                        '[%s] Failed to process command: command %s is unknown', self.client_address[0], cmd)
        except Exception as ex:
            pass


if __name__ == '__main__':
    server = ForkingTCPServer(('0.0.0.0',  8777), ServiceServerHandler)
    server.serve_forever()
