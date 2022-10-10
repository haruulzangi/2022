from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey

import socket
from utils import *

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 8777))

    private_key = X25519PrivateKey.generate()
    public_key_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    peer_public_key_raw = read_message(s)
    peer_public_key = X25519PublicKey.from_public_bytes(peer_public_key_raw)
    send_message(s, public_key_bytes)

    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'Codename: Phoenix'
    ).derive(shared_key)

    encrypted_flag = read_message(s)
    fernet = Fernet(urlsafe_b64encode(derived_key))

    flag = fernet.decrypt(encrypted_flag)
    print(flag)
    s.close()
