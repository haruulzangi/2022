#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
import socket
import socketserver

from utils import *


class ForkingTCPServer(socketserver.ForkingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketserver.TCPServer.server_bind(self)


flag = b'HZ{j0k3_1s_0v3r_u_R_S@f3!_jEXObuwJroTXtN}'


class ServiceServerHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)

    def handle(self):
        logger.info('[%s] Accepted connection', self.client_address[0])
        try:
            private_key = X25519PrivateKey.generate()
            public_key_bytes = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            send_message(self.request, public_key_bytes)

            peer_public_key_raw = read_message(self.request)
            peer_public_key = X25519PublicKey.from_public_bytes(
                peer_public_key_raw
            )

            shared_key = private_key.exchange(peer_public_key)
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'Codename: Phoenix'
            ).derive(shared_key)
            fernet = Fernet(urlsafe_b64encode(derived_key))
            ciphertext = fernet.encrypt(flag)

            send_message(self.request, ciphertext)
            self.finish()
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
