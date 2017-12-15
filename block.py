import json
from hashlib import blake2b


class Block(object):
    def __init__(self, data={}, prev_hash=None, deserialize=None):
        assert isinstance(data, dict)
        assert isinstance(prev_hash, str) or prev_hash is None
        assert isinstance(deserialize, str) or deserialize is None

        if deserialize is None:
            self.data = data
            self.prev_hash = prev_hash
            self.hash = None
            self.nonce = -1
        else:
            deserialized = json.loads(deserialize)
            self.data = deserialized['data']
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
            return blake2b((str(self.data) + str('doh') + str(self.nonce)).encode('utf-8'))
        return blake2b((str(self.data) + str(self.prev_hash) + str(self.nonce)).encode('utf-8'))

    def satisfies(self, curr_hash):
        return curr_hash.hexdigest().startswith('1729')  # Ramanujan's Number

    def serialize(self):
        return json.dumps({
            'data': self.data,
            'prev_hash': self.prev_hash,
            'hash': self.hash,
            'nonce': self.nonce
        })
