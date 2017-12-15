import json
from hashlib import blake2b

from transaction import Transaction


class Block(object):
    def __init__(self, prev_hash=None, deserialize=None):
        assert isinstance(prev_hash, str) or prev_hash is None
        assert isinstance(deserialize, str) or deserialize is None

        if deserialize is None:
            self.transactions = []
            self.prev_hash = prev_hash
            self.hash = None
            self.nonce = -1
        else:
            deserialized = json.loads(deserialize)
            self.transactions = deserialized['transactions']
            self.prev_hash = deserialized['prev_hash']
            self.hash = deserialized['hash']
            self.nonce = deserialized['nonce']
        
    def mine(self):
        assert self.hash is None
        assert self.nonce == -1
        curr_hash = self.getNextHash()
        while not self.satisfies(curr_hash):
            curr_hash = self.getNextHash()
        self.hash = curr_hash.hexdigest()

    def getNextHash(self):
        self.nonce += 1
        if self.prev_hash is None:
            return blake2b((str([t.toDict() for t in self.transactions]) + str('doh') + str(self.nonce)).encode('utf-8'))
        return blake2b((str([t.toDict() for t in self.transactions]) + str(self.prev_hash) + str(self.nonce)).encode('utf-8'))

    def satisfies(self, curr_hash):
        return curr_hash.hexdigest().startswith('1729')  # Ramanujan's Number

    def serialize(self):
        return json.dumps({
            'transactions': [t.toDict() for t in self.transactions],
            'prev_hash': self.prev_hash,
            'hash': self.hash,
            'nonce': self.nonce
        })

    def addTransaction(self, send, recv, amount):
        self.transactions.append(Transaction(send, recv, amount))
