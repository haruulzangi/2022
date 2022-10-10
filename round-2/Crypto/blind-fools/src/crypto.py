from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

private_key = rsa.generate_private_key(
    public_exponent=0x10001,
    key_size=2048
)
public_key = private_key.public_key()
public_key_data = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

flag = b'HZ{th3y_w311_c0w3r_E6te5aPzaNpwmqvvnQ}'
encrypted_flag = public_key.encrypt(
    flag,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
)

public_numbers = public_key.public_numbers()
private_numbers = private_key.private_numbers()


def blind_sign(data: bytes):
    result = pow(int.from_bytes(data, 'big'),
                 private_numbers.d, public_numbers.n)
    result_byte_length = (result.bit_length() + 7) // 8
    return result.to_bytes(result_byte_length, 'big')
