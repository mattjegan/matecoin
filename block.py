from hashlib import blake2b

class Block(object):
    def __init__(self, data={}, prev=None):
        assert isinstance(data, dict)
        assert isinstance(prev, Block) or prev is None
        self.data = data
        self.prev = prev
        self.hash = None
        self.nonce = -1
        
    def mine(self):
        assert self.hash is None
        assert self.nonce == -1
        curr_hash = self.getNextHash()
        while not self.satisfies(curr_hash):
            curr_hash = self.getNextHash()
        self.hash = curr_hash.hexdigest()

    def getNextHash(self):
        self.nonce += 1
        if self.prev is None:
            return blake2b((str(self.data) + str('doh') + str(self.nonce)).encode('utf-8'))
        return blake2b((str(self.data) + str(self.prev.hash) + str(self.nonce)).encode('utf-8'))

    def satisfies(self, curr_hash):
        return curr_hash.hexdigest().startswith('1729')  # Ramanujan's Number
