from web3 import Web3
import time
from hexbytes import HexBytes

# web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/tMUpxrBRib2XG1LhKdvGVql4LtGbdu58'))
web3 = Web3(Web3.HTTPProvider('https://eth-rinkeby.alchemyapi.io/v2/eriQZWQGeXNylGAMxvyOVIBe4JyU0Kxz'))

latest_block_filter = web3.eth.filter('latest')



pending_tx_filter = web3.eth.filter('pending')

dai_address = '0x6B175474E89094C44Da98b954EedeAC495271d0F'

dai_filter = web3.eth.filter({'address': dai_address})





def main():

    not_found = []
    pending = 0

    while True:
        # new_tx = dai_filter.get_new_entries()
        # for txs in new_tx:
        #     print(txs["transactionHash"].hex())
        pending_tx = web3.eth.get_filter_changes(pending_tx_filter.filter_id)
        pending += len(pending_tx)
        print(pending)

        block = web3.eth.get_block(block_hash.hex())
            date_time = datetime.fromtimestamp(block.timestamp)
            num_tx = len(block.transactions)
            pending -= num_tx


            
        time.sleep(1)


        

if __name__ == "__main__":
    main()