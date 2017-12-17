# DollaryDooos - A cryptocurrency proof of concept
## Installation
```
git clone <this_repo_url>
```

## Todo
* Networking to sync the blockchain and broadcast transactions
* Creation of a cli
    * Create a new wallet
        * `python cli.py create_wallet <passphrase>`
    * Mine from the pool:
        * `python cli.py mine`
    * Send DOH to a wallet:
        * `python cli.py send <wallet_file> <recv_addr> <amount>`
    * Inspect a block:
        * `python cli.py inspect_block <block_hash>`
    * Inspect all transactions and current amount for a wallet:
        * `python cli.py inspect_wallet <wallet_addr>`
        * Defaults to the address in the wallet file if no address is given
* Creation of a block explorer so we don't need to inspect `dd.db`

## Example
An example usage of the `BlockChain` object is given in `example.py`
