
from base64 import b32decode

from copy import deepcopy

from block import Block
from crypto import sign, verify_from_str
from exceptions import WalletDoesNotExist, WalletAmountTooLow
from wallet import Wallet


class BlockChain(object):
    def __init__(self):
        self.blocks = []
        self.wallets = {}
        self.wallets_at_block_edge = None

        # Check if the blockchain exists and load it
        self.load()
        self.verifyHistory()

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

        print('=== BLOCK MINED ===')
        print(f'Block: {len(self.blocks)} Hash: {block.hash} Nonce: {block.nonce}')
        print('Transactions:')
        for t in block.transactions:
            print(f'\t{t.send[:4]} -> {t.recv[:4]}: {t.amount}')
        print('Wallet States:')
        for addr, wallet in self.wallets.items():
            print(f'\t{addr[:4]}: {wallet.amount}')
        print()

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

    def getTransactionSig(self, send, recv, amount, priv_key):
        return sign(priv_key, send + recv + str(amount))

    def addTransaction(self, send, recv, amount, sig):
        self.verifyTransaction(send, recv, amount, sig)
        self.next_block.addTransaction(send, recv, amount)

        # If this is the first transaction of this block, we want to keep track of the wallet amounts at the
        # end of the last block so we can display amounts correctly later
        if self.wallets_at_block_edge is None:
            self.wallets_at_block_edge = deepcopy(self.wallets)

        self.wallets[send].amount -= amount
        self.wallets[recv].amount += amount

    def createWallet(self):
        wallet = Wallet()
        self.wallets[wallet.address] = wallet
        return wallet.address, wallet.priv_key

    def verifyTransaction(self, send, recv, amount, sig):
        # Verify the wallets exist
        if send not in self.wallets:
            raise WalletDoesNotExist('The sending wallet does not exist')
        if recv not in self.wallets:
            raise WalletDoesNotExist('The receiving wallet does not exist')

        # Verify the sender is who they say they are
        verify_from_str(send, sig, send + recv + str(amount))

        # Verify there is enough DOH in the wallet
        if self.wallets[send].amount < amount:
            raise WalletAmountTooLow('The sending wallet did not have enough DOH')

    def updateWalletsFromDiff(self, diff):
        # Need to set our local state back to the last block to avoid double incr/decr
        if self.wallets_at_block_edge is not None:
            self.wallets = self.wallets_at_block_edge

        for addr, value in diff.items():
            if addr == 'reward':  # TODO: Abstract Magic Vals (reward, ramanujan etc)
                continue

            if addr not in self.wallets:
                self.wallets[addr] = Wallet(addr)
            self.wallets[addr].amount += value

    def savePrivKey(self, priv_key):
        with open('priv_key.pem', 'x') as f:
            f.write(priv_key.to_pem().decode())

    def verifyHistory(self):
        # TODO: Should raise an exception if things don't add up in the blockchain
        pass
