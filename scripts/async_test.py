from web3 import Web3
import time
from hexbytes import HexBytes
from ens import ENS
import multiprocessing
import asyncio

# web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/AMq3rziNaAVTV6lQ1OUc5S5jAQXa-_Hl'))
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/ZiONpsBMj0B0RIXVomeMGU4xXkEBjkyq'))




latest_block_filter = web3.eth.filter('latest')
pending_tx_filter = web3.eth.filter('pending')


tracking_address = ['0x7eCb204feD7e386386CAb46a1fcB823ec5067aD5', '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D','0x5B93FF82faaF241c15997ea3975419DDDd8362c5']


address_filter = web3.eth.filter({'address': ['0x86449BFCa17bbAe097db76Ff5873F4522738a54B','0x6B175474E89094C44Da98b954EedeAC495271d0F','0x18598e07554A67a2E9C6dC3DCF4EFF7f5fCDEd20','0x854A199B6193106087939Eb52D58240E8eEA0C1e', '0x9DC09399b17519F6bc5730c1559a35d5C044207E']})



async def tx_task():
    for i in range(10):
        print(i, "hello")
        await asyncio.sleep(1)

async def call_coroutine():
     # loop.close()

    task = asyncio.create_task(tx_task())
    # await asyncio.wait(task)
    




def main():
    
    new_block = latest_block_filter.get_new_entries()


    while True:
        new_block = latest_block_filter.get_new_entries()

       

            

        

        
        for block_hash in new_block:
            loop = asyncio.get_event_loop()

            print("new block")
            block = web3.eth.get_block(block_hash.hex())
            # print( block.transactions)
            print(block.number)
            asyncio.run(call_coroutine())
            loop.close()
            

        time.sleep(1)



        

if __name__ == "__main__":
    main()
    
