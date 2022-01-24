import LIVEthereum  
from web3 import Web3
import time
from datetime import datetime
import requests
from hexbytes import HexBytes
from ens import ENS

# web3 = Web3(Web3.HTTPProvider('https://arb-mainnet.g.alchemy.com/v2/nMhcsR5Fy0pEsnb9mvzEkcvQIH2iqD7V'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/ZiONpsBMj0B0RIXVomeMGU4xXkEBjkyq'))
ens = ENS.fromWeb3(web3)
# web3 = Web3(Web3.WebsocketProvider('wss://eth-mainnet.alchemyapi.io/v2/tMUpxrBRib2XG1LhKdvGVql4LtGbdu58'))

tracking_address = ['0x6B175474E89094C44Da98b954EedeAC495271d0F']

tracking_address_names = ['dai']


latest_block_filter = web3.eth.filter('latest')

# pending_tx_filter = web3.eth.filter('pending')

address_filter = web3.eth.filter({'address': tracking_address})

num_last_blocks = 10

last_gas_prices  = []

def try_ens(address):
    domain = ens.name(address)
    return domain if domain != None else f"{address[:5]}...{address[len(address)-3:]}"



def calculate_average_gas(current_price):
    if len(last_gas_prices) >= num_last_blocks:
        last_gas_prices.pop(0)
    last_gas_prices.append(current_price)
    
    return format(sum(last_gas_prices) / len(last_gas_prices), ".3f")


def check_wifi():
     
 try:
    requests.get('https://ethereum.org/en/').status_code
    return True
 except:
    return False
    exit()
 


def connection_health():
    return {
        'is_connected': web3.isConnected(),
        'client_is_listening': web3.net.listening,
        'wifi_is_connected': check_wifi()

    }


def main():

    network_id = web3.eth.chain_id
    client_version = web3.clientVersion
    initial_connection = connection_health()
    

    live_ethereum = LIVEthereum.LIVEthereum(network_id, client_version,initial_connection)



    # block_count = 0
    # seconds_since_start = 0
    # block = web3.eth.getBlock("latest")
    # start_timestamp = block.timestamp

    blocks_since_start = 0
    gas_since_start = 0
    pending = 0
    

    
    while True:
        new_blocks = latest_block_filter.get_new_entries()
        new_tx = address_filter.get_new_entries()


        # pending_tx = pending_tx_filter.get_new_entries()

        for tx in new_tx: 
            address = tx.address
            index = tracking_address.index(address)
            tx_hash = f'{tx.transactionHash.hex()[:5]}...{tx.transactionHash.hex()[len(tx.transactionHash.hex())-3:]}'
            if tracking_address_names[index] != '':
                live_ethereum.handle_activity_monitor(tracking_address_names[index],tx_hash , tx.blockNumber)
            else:
                live_ethereum.handle_activity_monitor(try_ens(tx.address),tx_hash , tx.blockNumber)
                

        current_connection_status = connection_health()
        live_ethereum.handle_health(current_connection_status)

        for block_hash in new_blocks:
            blocks_since_start += 1

            


            gas_price = web3.eth.gas_price / 10**9
            print(gas_price)
            
            
            print("new block", block_hash.hex())
        
            block = web3.eth.get_block(block_hash.hex())
            date_time = datetime.fromtimestamp(block.timestamp)
            num_tx = len(block.transactions)
            pending -= num_tx
            
            

            # gas_since_start += gas_price
            print("average gas: ", gas_since_start / blocks_since_start)
            eth_burned = (block.baseFeePerGas * block.gasUsed) / 10**18

            block_data = {
                'block_number': str(block.number), 
                'block_hash': str(block_hash.hex()),
                'current_gas_price': format(gas_price, ".3f"),
                'num_tx': str(num_tx),
                'date_time': date_time,
                'transactions': block.transactions,
                'eth_burned': format(eth_burned, ".5f"),
                'num_pending': pending,
                'average' : calculate_average_gas(gas_price),
                'is_listening': web3.net.listening,
                'num_last_blocks': num_last_blocks,
                'miner': try_ens(block.miner)
            }
            live_ethereum.update_block(block_data)
            # live_ethereum(pending_transactions)
            # live_ethereum.handle_transactions()



            



        time.sleep(1)

        

if __name__ == "__main__":
    main()
