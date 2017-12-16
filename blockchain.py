from block import Block
from exceptions import WalletDoesNotExist, WalletAmountTooLow
from wallet import Wallet


class BlockChain(object):
    def __init__(self):
        self.blocks = []
        self.wallets = {}  # TODO: Add persistence for wallets

        # Check if the blockchain exists and load it
        self.load()

        self.last_save = len(self.blocks)

        if len(self.blocks) == 0:
            genesis_block = Block()
            genesis_block.mine()
            self.blocks.append(genesis_block)

        self.next_block = Block(prev_hash=self.blocks[-1].hash)

    def mineBlock(self, minerAddr=None):
        assert isinstance(minerAddr, str) or minerAddr is None
        self.next_block.mine(minerAddr)
        block = self.next_block
        self.blocks.append(block)
        self.next_block = Block(prev_hash=block.hash)
        self.updateWalletsFromDiff(block.getTransactionDiff())
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
            self.updateWalletsFromDiff(block.getTransactionDiff())
            self.blocks.append(block)

        db.close()

    def addTransaction(self, send, recv, amount):
        # TODO: Add verification of transaction
        # each block will store the diff of the wallet amounts
        # and hence the BC and verify how much DOH each wallet has
        print(f'{send[:4]} -> {recv[:4]}: {amount}')
        self.verifyTransaction(send, recv, amount)
        self.next_block.addTransaction(send, recv, amount)

        self.wallets[send].amount -= amount
        self.wallets[recv].amount += amount

    def createWallet(self):
        wallet = Wallet()
        self.wallets[wallet.address] = wallet
        return wallet.address

    def verifyTransaction(self, send, recv, amount):
        # Verify the wallets exist
        if send not in self.wallets:
            raise WalletDoesNotExist('The sending wallet does not exist')
        if recv not in self.wallets:
            raise WalletDoesNotExist('The receiving wallet does not exist')

        # Verify there is enough DOH in the wallet
        if self.wallets[send].amount < amount:
            raise WalletAmountTooLow('The sending wallet did not have enough DOH')

    def updateWalletsFromDiff(self, diff):
        for addr, value in diff.items():
            if addr == 'reward':  # TODO: Abstract Magic Vals (reward, ramanujan etc)
                continue

            if addr not in self.wallets:
                self.wallets[addr] = Wallet(addr)
            self.wallets[addr].amount += value
