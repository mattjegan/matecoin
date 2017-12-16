from blockchain import BlockChain


def main():
    bc = BlockChain()
    w1 = bc.createWallet()
    w2 = bc.createWallet()
    try:
        for i in range(1000):
            bc.addTransaction(w1, w2, 123)
            bc.addTransaction(w2, w1, 20)
            #bc.mineBlock()
    except KeyboardInterrupt:
        bc.save()

if __name__ == '__main__': main()