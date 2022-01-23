from web3 import Web3
import time
from hexbytes import HexBytes

# web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/AMq3rziNaAVTV6lQ1OUc5S5jAQXa-_Hl'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/0tGx2qXzMyIad2mTdWxjJRN3WHKE8bBb'))

latest_block_filter = web3.eth.filter('latest')



pending_tx_filter = web3.eth.filter('pending')


tracking_address = ['0x6B175474E89094C44Da98b954EedeAC495271d0F', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48']

address_filter = web3.eth.filter({'address': '0x6B175474E89094C44Da98b954EedeAC495271d0F'})






def main():

    not_found = []
    pending_changes = 0
    new_pending = 0



    while True:

        new_block = latest_block_filter.get_new_entries()

        new_pending_tx = pending_tx_filter.get_new_entries()

        new_tx = address_filter.get_new_entries()

        # new_tx = web3.eth.get_filter_changes(address_filter.filter_id)
        # for txs in new_tx:
        #     print(txs["transactionHash"].hex())
        


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
        
        for block_hash in new_block:
            print("new block")
            block = web3.eth.get_block(block_hash.hex())

            num_tx = len(block.transactions)
            # pending_changes -= num_tx
            new_pending -= num_tx

        time.sleep(1)



        

if __name__ == "__main__":
    main()