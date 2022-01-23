from web3 import Web3
import time
from hexbytes import HexBytes
from ens import ENS

# web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/AMq3rziNaAVTV6lQ1OUc5S5jAQXa-_Hl'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/ZiONpsBMj0B0RIXVomeMGU4xXkEBjkyq'))
ens = ENS.fromWeb3(web3)
latest_block_filter = web3.eth.filter('latest')

domain = ens.name('0x53C6d68A0826C587B57A50C6C42932eb2B6E8086')
print(domain)

pending_tx_filter = web3.eth.filter('pending')


tracking_address = ['0x6B175474E89094C44Da98b954EedeAC495271d0F', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48']


address_filter = web3.eth.filter({'address': '0x7bf66Ee1717d64B4e7Ac2942600E4EbF6FdB3F53'})






def main():

    not_found = []
    pending_changes = 0
    new_pending = 0



    while True:


        new_tx = address_filter.get_new_entries()

        # new_tx = web3.eth.get_filter_changes(address_filter.filter_id)

        for txs in new_tx:
            print(txs)
        


        # pending_changes += len(pending_tx_changes)
        # print("get_filter_changes results", pending_changes)

        # new_pending += len(new_pending_tx)
        # print("get_new_entries results", new_pending)


        # for tx in new_pending_tx:
        #     try:
        #         transaction = web3.eth.get_transaction(tx.hex())
        #         print(transaction.hash.hex())
        #     except:
        #         print("not found")
        #         pass
        
        # for block_hash in new_block:
        #     print("new block")
        #     block = web3.eth.get_block(block_hash.hex())
        #     for tx in block.transactions:
        #         transaction = web3.eth.get_transaction(tx.hex())
        #         # print(transaction)
        #         for addr in tracking_address:
        #             if addr == transaction['from']:
        #                 print("hello from", transaction.hash.hex())
        #             elif addr == transaction['to']:
        #                 print("Hello to", transaction.hash.hex())
        #     num_tx = len(block.transactions)
        #     # pending_changes -= num_tx
        #     new_pending -= num_tx

        time.sleep(1)



        

if __name__ == "__main__":
    main()