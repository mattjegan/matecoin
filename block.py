import json
from hashlib import blake2b
from collections import defaultdict

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
            self.transactions = [Transaction(deserialize=t) for t in deserialized['transactions']]
            self.prev_hash = deserialized['prev_hash']
            self.hash = deserialized['hash']
            self.nonce = deserialized['nonce']
        
    def mine(self, minerAddr=None):
        assert isinstance(minerAddr, str) or minerAddr is None
        assert self.hash is None
        assert self.nonce == -1
        self.addReward(minerAddr)
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

    def getTransactionDiff(self):
        diff = defaultdict(lambda: 0)
        for t in self.transactions:
            diff[t.send] -= t.amount
            diff[t.recv] += t.amount
        return dict(diff)

    def addReward(self, minerAddr=None):
        assert isinstance(minerAddr, str) or minerAddr is None
        # TODO: Is a fixed reward good enough?
        self.transactions.append(Transaction(recv=minerAddr, amount=1, reward=True))
