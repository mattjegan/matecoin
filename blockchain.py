from block import Block

class BlockChain(object):
    def __init__(self, genesis_block=None):
        self.blocks = []
        if not genesis_block:
            genesis_block = Block()
        self.addBlock(genesis_block)

    def addBlock(self, block):
        assert isinstance(block, Block)
        block.mine()
        self.blocks.append(block)

    def mineBlock(self, data):
        assert isinstance(data, dict)
        block = Block(data, self.blocks[-1])
        self.addBlock(block)
        print(f'Block: {len(self.blocks)} Hash: {block.hash} Nonce: {block.nonce}')

