from web3 import Web3
import time
from hexbytes import HexBytes
from ens import ENS

# web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/AMq3rziNaAVTV6lQ1OUc5S5jAQXa-_Hl'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/ZiONpsBMj0B0RIXVomeMGU4xXkEBjkyq'))
ens = ENS.fromWeb3(web3)
latest_block_filter = web3.eth.filter('latest')

def try_ens(address):
    domain = ens.name(address)
    return domain if domain != None else f"{address[:5]}...{address[len(address)-3:]}"

print(try_ens('0x7dA30048214E112Dbc41A645e37f9640ac62799E'))


pending_tx_filter = web3.eth.filter('pending')


tracking_address = ['0x7eCb204feD7e386386CAb46a1fcB823ec5067aD5', '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D','0x5B93FF82faaF241c15997ea3975419DDDd8362c5']

tracking_address_names = ["meta card", "BAYC"]

address_filter = web3.eth.filter({'address': tracking_address})






def main():

    not_found = []
    pending_changes = 0
    new_pending = 0



    while True:


        new_tx = address_filter.get_new_entries()

        # new_tx = web3.eth.get_filter_changes(address_filter.filter_id)

        for tx in new_tx: 
            address = tx.address
            index = tracking_address.index(address)
            tx_hash = f'{tx.transactionHash.hex()[:5]}...{tx.transactionHash.hex()[len(tx.transactionHash.hex())-3:]}'
            try: 
                tracking_address_names[index]
                live_ethereum.handle_activity_monitor(tracking_address_names[index],tx_hash , tx.blockNumber)
            except:
                 live_ethereum.handle_activity_monitor(try_ens(tx.address),tx_hash , tx.blockNumber)
            
        


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