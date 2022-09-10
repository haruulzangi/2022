plaintext = 0x00 # TODO: Solve me

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


def decodeOAEP(data: int) -> bytes:
    k = byte_length(n)
    em = data.to_bytes(k, 'big')
    seed = em[1: hash_size+1]
    db = em[hash_size+1:]
    seed = mgf1XOR(seed, db)
    db = mgf1XOR(db, seed)
    return db


print(decodeOAEP(plaintext).hex())
