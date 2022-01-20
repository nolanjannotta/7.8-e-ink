import LIVEthereum  
from web3 import Web3
import time
from hexbytes import HexBytes

web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/tMUpxrBRib2XG1LhKdvGVql4LtGbdu58'))

latest_block_filter = web3.eth.filter('latest')

pending_tx_filter = web3.eth.filter('pending')



def main():

    live_ethereum = LIVEthereum.LIVEthereum()



    block_count = 0
    seconds_since_start = 0
    block = web3.eth.getBlock("latest")
    start_timestamp = block.timestamp
    while True:
        new_blocks = latest_block_filter.get_new_entries()
        for block_hash in new_blocks:
            block_count += 1
            
            
            print("_________________________________________new block_________________________________")
            print("blockhash", block_hash.hex())
            block = web3.eth.get_block(block_hash.hex())
            seconds_since_start = (block.timestamp - start_timestamp)            
            num_tx = len(block.transactions)
            gas_price = web3.eth.gas_price / 10**9
            live_ethereum.update_block(str(block.number),str(block_hash.hex()),format(gas_price, ".3f"), str(num_tx),block.timestamp )

            print(f"block # {block.number} | number of transaction:  {num_tx} | at {block.timestamp}")
            print(f"average block length is {int(seconds_since_start / block_count)} seconds")
            print((block.baseFeePerGas * block.gasUsed) / 10**18, "eth burned")
            print(f"current gas price: {web3.eth.gas_price / 10**9} gwei")
            print("____________________________________________________________________________________")
            

        

if __name__ == "__main__":
    main()
