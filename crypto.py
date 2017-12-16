
from ecdsa import SigningKey, NIST521p, VerifyingKey


def generate_private_key():
    return SigningKey.generate(curve=NIST521p)


def generate_public_key(priv_key):
    return priv_key.get_verifying_key()


def sign(priv_key, data):
    return priv_key.sign(data)


def verify_from_key(publ_key, sig, data):
    return publ_key.verify(sig, data)


def verify_from_str(publ_key, sig, data):
    return verify_from_key(VerifyingKey.from_string(bytes.fromhex(publ_key), curve=NIST521p), sig, data)
