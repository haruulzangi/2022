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

import base64
import socket
from utils import *

alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice.connect(('localhost', 8778))
alice_envelope = read_message(alice)

carol = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
carol.connect(('localhost', 8777))
carol_envelope = read_message(carol)

send_message(carol, alice_envelope)
send_message(alice, carol_envelope)

key = ECC.generate(curve='P-256')
public_key = key.public_key().export_key(format='DER')

point_ac_x = int(read_message(alice).decode('ascii'))
point_ac_y = int(read_message(alice).decode('ascii'))
point_ac = ECC.EccPoint(point_ac_x, point_ac_y, curve='P-256')

alice_pk = ECC.import_key(
	base64.urlsafe_b64decode(
		jwt.decode(alice_envelope, verify=False)['key']
	)
).public_key()
carol_pk = ECC.import_key(
	base64.urlsafe_b64decode(
		jwt.decode(carol_envelope, verify=False)['key']
	)
).public_key()

point_bc = carol_pk.pointQ * key.d
send_message(alice, str(point_bc.x).encode('ascii'))
send_message(alice, str(point_bc.y).encode('ascii'))

point_ab = alice_pk.pointQ * key.d
send_message(carol, str(point_ab.x).encode('ascii'))
send_message(carol, str(point_ab.y).encode('ascii'))

shared_secret = point_ac * key.d
derived_secret = PBKDF2(
	shared_secret.x.to_bytes(32, 'big'),
	shared_secret.y.to_bytes(32, 'big'),
	64, count=1000000, hmac_hash_module=SHA512
)

key = derived_secret[:32]

alice_nonce = read_message(alice)
cipher_alice = AES.new(key, AES.MODE_CCM, nonce=alice_nonce)
alice_ciphertext = read_message(alice)
alice_tag = read_message(alice)
flag_alice = cipher_alice.decrypt_and_verify(alice_ciphertext, alice_tag)
print(flag_alice)

carol_nonce = read_message(carol)
cipher_carol = AES.new(key, AES.MODE_CCM, nonce=carol_nonce)
carol_ciphertext = read_message(carol)
carol_tag = read_message(carol)
flag_carol = cipher_carol.decrypt_and_verify(carol_ciphertext, carol_tag)
print(flag_carol)
