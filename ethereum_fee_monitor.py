# Write an ethereum transaction fee monitor in Python.

# The monitor should report min/max/avg fee in Gwei for the current and all subsequent blocks (until monitor
# is stopped).

# Hint: it is recommended to use web3 package and some free web3 endpoint.

from web3 import Web3
from apscheduler.schedulers.blocking import BlockingScheduler

class feeMonitor:
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/ddf58b1b9c1742a586570078c6823c23'))
    block = w3.eth.getBlock('latest', full_transactions=True)

    block_number = block.number

    def schedule(self):
        self.scheduler = BlockingScheduler(timezone="Europe/Berlin")
        self.scheduler.add_job(self.latest_block, 'interval', seconds=2)
        self.scheduler.start()

    def latest_block(self):
        # Get information about the latest block
        block = self.w3.eth.getBlock('latest', full_transactions=True)

        if block.number == self.block_number:
            pass

        else:
            fees = []

            for key in block.transactions:
                price_in_wei = key.gas * key.gasPrice
                price_in_gwei = price_in_wei / 1000000000
                fees.append(price_in_gwei)

            fees.sort()
            number_of_transactions = len(fees)
            block_fees_sum = sum(fees)

            self.min_fee = fees[0]
            self.avg_fee = block_fees_sum/number_of_transactions
            self.max_fee = fees[-1]

            print(f"Block number {block.number}:")
            print(f"Min fee per transaction in this block was {self.min_fee} Gwei.")
            print(f"Avg fee per transaction in this block was {self.avg_fee} Gwei.")
            print(f"Max fee per transaction in this block was {self.max_fee} Gwei.")

            self.block_number = block.number

run_the_monitor = feeMonitor()
run_the_monitor.schedule()