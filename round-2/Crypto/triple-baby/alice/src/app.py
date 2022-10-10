#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
from os.path import exists
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Protocol.KDF import PBKDF2

import collections
try:
    from collections.abc import Iterable, Mapping
    collections.Iterable = Iterable
    collections.Mapping = Mapping
except ImportError:
    pass

import jwt
import socket
import socketserver

from utils import *

jwt_key = None
carol_key = None


class ForkingTCPServer(socketserver.ForkingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketserver.TCPServer.server_bind(self)


flag_part = b'HZ{n0th1ng_st@ys_h1dd3n_fr0m_m3+'


class ServiceServerHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)

    def handle(self):
        logger.info('[%s] Accepted connection', self.client_address[0])
        try:
            # Three-way ECDHE handshake, baby!
            key = ECC.generate(curve='P-256')
            envelope = jwt.encode({
                'key': base64.urlsafe_b64encode(key.public_key().export_key(format='DER')).decode('ascii')
            }, jwt_key, algorithm='ES256')
            send_message(self.request, envelope)

            carol_envelope = read_message(self.request)
            carol_pk = ECC.import_key(
                base64.urlsafe_b64decode(
                    jwt.decode(carol_envelope, carol_key,
                               algorithms=['ES256'])['key']
                )
            ).public_key()

            point_ac = carol_pk.pointQ * key.d
            send_message(self.request, str(point_ac.x).encode('ascii'))
            send_message(self.request, str(point_ac.y).encode('ascii'))

            point_bc_x = int(read_message(self.request).decode('ascii'))
            point_bc_y = int(read_message(self.request).decode('ascii'))

            shared_secret = ECC.EccPoint(
                point_bc_x,
                point_bc_y,
                curve='P-256'
            ) * key.d
            derived_secret = PBKDF2(
                shared_secret.x.to_bytes(32, 'big'),
                shared_secret.y.to_bytes(32, 'big'),
                64, count=1000000, hmac_hash_module=SHA512
            )

            key = derived_secret[:32]

            cipher = AES.new(key, AES.MODE_CCM)
            ciphertext, tag = cipher.encrypt_and_digest(flag_part)
            send_message(self.request, cipher.nonce)
            send_message(self.request, ciphertext)
            send_message(self.request, tag)

            self.finish()
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        finally:
            logger.info('[%s] Processed connection', self.client_address[0])


if __name__ == '__main__':
    if not exists('jwt.key'):
        print('Generating new JWT key...')
        key = ECC.generate(curve='P-256')
        f = open('jwt.key', 'wt')
        f.write(key.export_key(format='PEM'))
        f.close()

    jwt_key = open('jwt.key', 'rt').read()
    public_key = ECC.import_key(jwt_key).public_key().export_key(format='PEM')
    print("Alice's public key:")
    print(public_key)

    if not exists('carol.key'):
        print("Carol's key was not found. Cannot start :c")
        exit(1)
    carol_key = open('carol.key', 'rt').read()

    logging.basicConfig(format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger('service')

    server = ForkingTCPServer(('0.0.0.0',  8778), ServiceServerHandler)
    server.serve_forever()
