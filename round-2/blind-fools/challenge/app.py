#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import socketserver

from utils import *
from crypto import encrypted_flag, blind_sign, public_key_data


class ForkingTCPServer(socketserver.ForkingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketserver.TCPServer.server_bind(self)


class ServiceServerHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)

    def handle(self):
        logger.info('[%s] Accepted connection', self.client_address[0])
        try:
            while True:
                cmd = read_message(self.request)
                logger.info('[%s] Accepted command: %s',
                            self.client_address[0], cmd)
                if cmd == b'PULL':
                    logger.info('[%s] PULL: Executing', self.client_address[0])
                    send_message(self.request, encrypted_flag)
                elif cmd == b'SIGN':
                    logger.info('[%s] SIGN: Executing', self.client_address[0])
                    data = read_message(self.request)
                    send_message(self.request, blind_sign(data))
                elif cmd == b'PUBKEY':
                    logger.info('[%s] PUBKEY: Executing',
                                self.client_address[0])
                    send_message(self.request, public_key_data)
                elif cmd == b'EXIT':
                    send_message(self.request, b'OK')
                    break
                else:
                    raise Exception(
                        '[%s] Failed to process command: command %s is unknown', self.client_address[0], cmd)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        finally:
            logger.info('[%s] Processed connection', self.client_address[0])


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger('service')

    server = ForkingTCPServer(('0.0.0.0',  8777), ServiceServerHandler)
    server.serve_forever()
