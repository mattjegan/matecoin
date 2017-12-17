from blockchain import BlockChain


def main():

    # Create or load the blockchain
    bc = BlockChain()

    # Create a new wallet to mine into (this could be set to the same string each run to maintain your wallet addr)
    # TODO: Make the chain into a cli so we can save wallet addresses locally for mining into
    my_wallet, priv_key = bc.createWallet()
    bc.savePrivKey(priv_key)

    w1, w1_priv_key = bc.createWallet()
    w2, w2_priv_key = bc.createWallet()

    # Mine some coin into w1 and w2
    # Note: blocks don't need transactions in them to give a reward
    #       this doesn't matter as it make the chain longer (more secure) and thus we should reward the miner
    for _ in range(20):
        bc.mineBlock(w1)
        bc.mineBlock(w2)

    try:
        for _ in range(20):
            # Create some transactions
            sig = bc.getTransactionSig(w1, w2, 5, w1_priv_key)
            bc.addTransaction(w1, w2, 5, sig)

            sig = bc.getTransactionSig(w2, w1, 5, w2_priv_key)
            bc.addTransaction(w2, w1, 5, sig)

            # Mine the current block with the transactions we made and collect the reward into our wallet
            bc.mineBlock(my_wallet)

    # Watch for a keyboard interrupt so we gracefully exit and save the blockchain to the db
    except KeyboardInterrupt:
        pass

    bc.save()

if __name__ == '__main__': main()