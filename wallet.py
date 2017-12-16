import os
from time import time
from hashlib import blake2b


class Wallet(object):
    def __init__(self, address=None):
        # TODO: Secure wallets with priv keys
        self.address = address or blake2b((str(os.urandom(1729)) + str(time())).encode('utf-8')).hexdigest()

        # TODO: Figure out initial amount and how to generate initial value in the chain
        self.amount = 200
