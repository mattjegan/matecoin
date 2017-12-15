from blockchain import BlockChain


def main():
    bc = BlockChain()
    try:
        for i in range(1000):
            bc.mineBlock({
                'tx_id': i
            })
    except KeyboardInterrupt:
        bc.save()

if __name__ == '__main__': main()