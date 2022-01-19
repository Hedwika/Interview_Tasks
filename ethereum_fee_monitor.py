# Write an ethereum transaction fee monitor in Python.

# The monitor should report min/max/avg fee in Gwei for the current and all subsequent blocks (until monitor
# is stopped).

# Hint: it is recommended to use web3 package and some free web3 endpoint.
from _cffi_backend import callback
from web3 import Web3
from apscheduler.schedulers.blocking import BlockingScheduler

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/ddf58b1b9c1742a586570078c6823c23'))
block = w3.eth.getBlock('latest', full_transactions=True)
# print(block)
# print("xxxxxx")
# print(block.transactions)

for key in block.transactions:
    price_in_wei = key.gas * key.gasPrice
    price_in_gwei = price_in_wei/1000000000
    print(price_in_gwei)

class myClass:
    block_number = block.number

    # gas_price = w3.eth.getTransaction("0x9fc76417374aa880d4449a1f7f31ec597f00b1f6f3dd2d66f4c9c6c445836d8b§234")
    # print(gas_price)

    print(f"Block number {block.number}:")
    print(f"Base fee per gas is {block.baseFeePerGas} Gwei.")

    fee = block.baseFeePerGas

    def schedule(self):
        self.scheduler = BlockingScheduler(timezone="Europe/Berlin")
        self.scheduler.add_job(self.latest_block, 'interval', seconds=2)
        self.scheduler.start()

    def latest_block(self):
        # Get information about the latest block
        block = w3.eth.getBlock('latest')

        if block.number == self.block_number:
            pass

        else:
            # min_fee =
            # avg_fee =
            # max_fee =
            print(f"Block number {block.number}:")
            print(f"Max priority fee: {w3.eth.max_priority_fee}")
            # print(f"Min fee per block was {self.min_fee}:")
            # print(f"Avg fee per block was {self.avg_fee}:")
            # print(f"Max fee per block was {self.max_fee}:")
            print(f"Base fee per gas is {block.baseFeePerGas} Gwei.")
            self.block_number = block.number

test = myClass()
test.schedule()

# print(block.transactions)

# Get the ETH balance of an address
# print(w3.eth.getBalance('0xcE2968E661943F9D7B309E290AAc402bbFA8e58A'))