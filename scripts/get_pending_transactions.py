from web3 import Web3
import time
from hexbytes import HexBytes

web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/AMq3rziNaAVTV6lQ1OUc5S5jAQXa-_Hl'))
# web3 = Web3(Web3.HTTPProvider('https://eth-rinkeby.alchemyapi.io/v2/eriQZWQGeXNylGAMxvyOVIBe4JyU0Kxz'))

latest_block_filter = web3.eth.filter('latest')



pending_tx_filter = web3.eth.filter('pending')

dai_address = '0x6B175474E89094C44Da98b954EedeAC495271d0F'

dai_filter = web3.eth.filter({'address': dai_address})





def main():

    not_found = []
    pending_changes = 0
    new_pending = 0
    network_id = web3.net.version
    print(network_id)

    while True:
        new_block = latest_block_filter.get_new_entries()
        new_pending_tx = pending_tx_filter.get_new_entries()

        # new_tx = dai_filter.get_new_entries()
        # for txs in new_tx:
        #     print(txs["transactionHash"].hex())
        pending_tx_changes = web3.eth.get_filter_changes(pending_tx_filter.filter_id)
        


        pending_changes += len(pending_tx_changes)
        print("get_filter_changes results", pending_changes)

        new_pending += len(new_pending_tx)
        print("get_new_entries results", new_pending)
        
        for block_hash in new_block:
            print("new block")
            block = web3.eth.get_block(block_hash.hex())
            num_tx = len(block.transactions)
            # pending_changes -= num_tx
            new_pending -= num_tx

        time.sleep(2)



        

if __name__ == "__main__":
    main()