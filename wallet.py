import os
from time import time
from hashlib import blake2b


class Wallet(object):
    def __init__(self):
        # TODO: Secure wallets with priv keys
        self.address = blake2b((str(os.urandom(1729)) + str(time())).encode('utf-8')).hexdigest()
        self.amount = 200
