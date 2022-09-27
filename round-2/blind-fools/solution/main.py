from hashlib import sha256
from cryptography.hazmat.primitives import serialization

import socket
from utils import *

hash_size = 256 // 8


def byte_length(i):
    return (i.bit_length() + 7) // 8


def mgf1XOR(target: bytes, seed: bytes) -> bytes:
    counter = 0
    done = 0
    out = list(target)
    while done < len(out):
        h = sha256(seed + counter.to_bytes(4, 'big')).digest()
        i = 0
        while i < len(h) and done < len(out):
            out[done] ^= h[i]
            done += 1
            i += 1
        counter += 1
    return bytes(out)


def decodeOAEP(n: int, data: int) -> bytes:
    k = byte_length(n)
    em = data.to_bytes(k, 'big')
    seed = em[1: hash_size+1]
    db = em[hash_size+1:]
    seed = mgf1XOR(seed, db)
    db = mgf1XOR(db, seed)
    return db


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 8777))

    send_message(s, b'PUBKEY')
    pubkey_data = read_message(s)
    pubkey = serialization.load_ssh_public_key(pubkey_data)

    send_message(s, b'PULL')
    encrypted_flag = read_message(s)

    send_message(s, b'SIGN')
    send_message(s, encrypted_flag)
    result = read_message(s)

    send_message(s, b'EXIT')

    flag = decodeOAEP(pubkey.public_numbers().n, int.from_bytes(result, 'big'))
    print(flag)
