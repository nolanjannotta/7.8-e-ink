import LIVEthereum  
from web3 import Web3
import time
from datetime import datetime
import requests
from hexbytes import HexBytes
from ens import ENS
import asyncio


# web3 = Web3(Web3.HTTPProvider('https://arb-mainnet.g.alchemy.com/v2/nMhcsR5Fy0pEsnb9mvzEkcvQIH2iqD7V'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/ZiONpsBMj0B0RIXVomeMGU4xXkEBjkyq'))
ens = ENS.fromWeb3(web3)
# web3 = Web3(Web3.WebsocketProvider('wss://eth-mainnet.alchemyapi.io/v2/tMUpxrBRib2XG1LhKdvGVql4LtGbdu58'))

tracking_address = ['0x7eCb204feD7e386386CAb46a1fcB823ec5067aD5', '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D', '0x5B93FF82faaF241c15997ea3975419DDDd8362c5', '0x86a62F9aed781d5E969a8a15C44f6547cC4b7F1B','0xBEEEE21dDaEFe0Ce455B7002EAB9D1703E2191e0']

tracking_address_names = ["meta card", "BAYC", "", "nolan","ramsey"]
# maybe blank names should be represented as empty strings??


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
    
    return format(sum(last_gas_prices) / len(last_gas_prices), ".2f")


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

def activity_monitor(live_ethereum, new_tx):
    for tx in new_tx: 
        index = tracking_address.index(tx.address)
        # tx_hash = f'{tx.transactionHash.hex()[:5]}...{tx.transactionHash.hex()[len(tx.transactionHash.hex())-3:]}'
        if tracking_address_names[index] != "":
            live_ethereum.handle_activity_monitor(tracking_address_names[index],tx.transactionHash.hex() , tx.blockNumber)
        else:
            live_ethereum.handle_activity_monitor(try_ens(tx.address),tx.transactionHash.hex() , tx.blockNumber)
        

def format_tx(transactions):
    num_tx = len(transactions)
    starting_point = 0
    tx_per_page = []
    num_pages = (num_tx // 226) + 1 if num_tx % 226 > 0 else num_tx // 226

    for page in range(num_pages):
        if page < num_pages:
            tx_per_page.append(list(transactions[starting_point:starting_point + 226]))
            starting_point += 226
        else:
            tx_per_page.append(list(transactions[starting_point:]))

    return tx_per_page



def main():

    network_id = web3.eth.chain_id
    client_version = web3.clientVersion
    initial_connection = connection_health()
    

    live_ethereum = LIVEthereum.LIVEthereum(network_id, client_version,initial_connection)


    

    
    while True:

        try:
            new_blocks = latest_block_filter.get_new_entries()
            new_tx = address_filter.get_new_entries()
        

            current_connection_status = connection_health()
            live_ethereum.handle_health(current_connection_status)



            activity_monitor(live_ethereum, new_tx)
                
                    



            for block_hash in new_blocks:

                block = web3.eth.get_block(block_hash.hex())
                gas_price = web3.eth.gas_price / 10**9
                print(gas_price)
                
                
                print("new block", block_hash.hex())
                print("#", {block.number})
            
                

                date_time = datetime.fromtimestamp(block.timestamp)
                num_tx = len(block.transactions)
                

                
                
                eth_burned = (block.baseFeePerGas * block.gasUsed) / 10**18

                block_data = {
                    'block_number': str(block.number), 
                    'block_hash': str(block_hash.hex()),
                    'current_gas_price': format(gas_price, ".2f"),
                    'num_tx': str(num_tx),
                    'date_time': date_time,
                    'transactions': block.transactions,
                    'eth_burned': format(eth_burned, ".4f"),
                    # 'num_pending': pending,
                    'average' : calculate_average_gas(gas_price),
                    # 'is_listening': web3.net.listening,
                    'num_last_blocks': num_last_blocks,
                    'miner': try_ens(block.miner)
                }

                live_ethereum.update_block(block_data)

        except Exception as e:
            live_ethereum.handle_exception(e)
            time.sleep(3)
            current_connection_status = connection_health()
            live_ethereum.handle_health(current_connection_status)


            break

        time.sleep(1)

        

if __name__ == "__main__":
    try:

        main()
    except Exception as e:

        print(e)
        time.sleep(2)
        main()

