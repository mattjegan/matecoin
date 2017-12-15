from block import Block

class BlockChain(object):
    def __init__(self):
        self.blocks = []

        # Check if the blockchain exists and load it
        self.load()

        self.last_save = len(self.blocks)

        if len(self.blocks) == 0:
            genesis_block = Block()
            self.addBlock(genesis_block)

    def addBlock(self, block):
        assert isinstance(block, Block)
        block.mine()
        self.blocks.append(block)

    def mineBlock(self, data):
        assert isinstance(data, dict)
        block = Block(data, self.blocks[-1].hash)
        self.addBlock(block)
        print(f'Block: {len(self.blocks)} Hash: {block.hash} Nonce: {block.nonce}')

    def save(self):
        with open('dd.db', 'a') as db:
            for block in self.blocks[self.last_save:]:
                db.write(f'{block.serialize()}\n')

    def load(self):
        try:
            db = open('dd.db', 'r')
        except FileNotFoundError:
            db = open('dd.db', 'x+')

        for entry in db:
            entry = entry.rstrip()
            block = Block(deserialize=entry)
            self.blocks.append(block)

        db.close()
