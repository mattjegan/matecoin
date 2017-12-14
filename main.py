from blockchain import BlockChain

def main():
    bc = BlockChain()
    for i in range(1000):
        bc.mineBlock({
            'tx_id': i
        })

if __name__ == '__main__': main()