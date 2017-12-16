from blockchain import BlockChain


def main():
    my_wallet = '9733fe2ede889ea39c077b3aed5485e22f4919755bcd1cb46c245a3b0293d93f3af40bd8c6644cd22c07df8a0b270a54086e060e44f79be301b0a1c73de624f4'
    bc = BlockChain()

    try:
        for i in range(1000):
            bc.mineBlock(my_wallet)
    except KeyboardInterrupt:
        pass
    bc.save()

if __name__ == '__main__': main()