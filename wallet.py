
from base64 import b32encode

from crypto import generate_private_key, generate_public_key


class Wallet(object):
    def __init__(self, address=None):
        if address is None:  # Creating a new wallet, we need to generate the priv and publ keys
            self.priv_key = generate_private_key()
            self.address = b32encode(generate_public_key(self.priv_key).to_string()).decode()
        else:
            self.address = address

        self.amount = 0
