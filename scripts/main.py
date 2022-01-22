import LIVEthereum  
from web3 import Web3
import time
from datetime import datetime
from hexbytes import HexBytes

# web3 = Web3(Web3.HTTPProvider('https://arb-mainnet.g.alchemy.com/v2/nMhcsR5Fy0pEsnb9mvzEkcvQIH2iqD7V'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/AMq3rziNaAVTV6lQ1OUc5S5jAQXa-_Hl'))
# web3 = Web3(Web3.WebsocketProvider('wss://eth-mainnet.alchemyapi.io/v2/tMUpxrBRib2XG1LhKdvGVql4LtGbdu58'))

latest_block_filter = web3.eth.filter('latest')

pending_tx_filter = web3.eth.filter('pending')



def main():

    live_ethereum = LIVEthereum.LIVEthereum()



    # block_count = 0
    # seconds_since_start = 0
    # block = web3.eth.getBlock("latest")
    # start_timestamp = block.timestamp

    blocks_since_start = 0
    gas_since_start = 0
    pending = 0
    while True:
        new_blocks = latest_block_filter.get_new_entries()
        pending_tx = pending_tx_filter.get_new_entries()
        pending += len(pending_tx)
        for block_hash in new_blocks:
            blocks_since_start += 1
            
            
            print("new block", block_hash.hex())
        
            block = web3.eth.get_block(block_hash.hex())
            date_time = datetime.fromtimestamp(block.timestamp)
            num_tx = len(block.transactions)
            pending -= num_tx
            gas_price = web3.eth.gas_price / 10**9
            gas_since_start += gas_price
            print("average gas: ", gas_since_start / blocks_since_start)
            eth_burned = (block.baseFeePerGas * block.gasUsed) / 10**18

            live_ethereum.update_block(str(block.number),str(block_hash.hex()),format(gas_price, ".3f"), str(num_tx),date_time, block.transactions, format(eth_burned, ".5f"), pending)
            # live_ethereum(pending_transactions)
            # live_ethereum.handle_transactions()
        time.sleep(1)

        

if __name__ == "__main__":
    main()
