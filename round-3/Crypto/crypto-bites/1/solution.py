# -*- coding: utf-8 -*-
import base64
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


import socket
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect(('smol-bite.challenge.haruulzangi.mn', 18777))
        send_message(conn, b'DATA')
        data = read_message(conn)
        print(base64.b64encode(data))
        send_message(conn, b'KEY')
        key = read_message(conn)
        print(key)
