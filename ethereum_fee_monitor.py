# Write an ethereum transaction fee monitor in Python.

# The monitor should report min/max/avg fee in Gwei for the current and all subsequent blocks (until monitor
# is stopped).

# Hint: it is recommended to use web3 package and some free web3 endpoint.

from web3 import Web3
from apscheduler.schedulers.blocking import BlockingScheduler

class feeMonitor:

    # Connect to the blockchain and get information about the latest block
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/ddf58b1b9c1742a586570078c6823c23'))
    block = w3.eth.getBlock('latest', full_transactions=True)

    # Set the variable to avoid duplicit blocks in the function below
    block_number = block.number

    # Set the interval for getting blocks
    def schedule(self):
        self.scheduler = BlockingScheduler(timezone="Europe/Berlin")
        self.scheduler.add_job(self.latest_block, 'interval', seconds=2)
        self.scheduler.start()

    def latest_block(self):
        # Get information about the latest block
        block = self.w3.eth.getBlock('latest', full_transactions=True)

        # Condition to avoid duplicit blocks
        if block.number == self.block_number:
            pass

        else:
            fees = []
            gas_prices = []

        # iterate through transactions
            for key in block.transactions:
                price_in_wei = key.gas * key.gasPrice
                price_in_gwei = price_in_wei / 1000000000
                fees.append(price_in_gwei)

                gas_price_wei = key.gasPrice
                gas_price_gwei = gas_price_wei / 1000000000
                gas_prices.append(gas_price_gwei)

            # Check the number of transactions via our list len
            number_of_transactions = len(fees)

            # Calculate transaction fees
            fees.sort()
            block_fees_sum = sum(fees)
            self.min_fee = fees[0]
            self.avg_fee = block_fees_sum / number_of_transactions
            self.max_fee = fees[-1]

            # Calculate gas prices
            gas_prices.sort()
            gas_prices_sum = sum(gas_prices)
            self.min_gas_price = gas_prices[0]
            self.avg_gas_price = gas_prices_sum / number_of_transactions
            self.max_gas_price = gas_prices[-1]

            # Convert base fee from wei to gwei
            self.base_fee_gwei = block.baseFeePerGas / 1000000000

            # Print results into the terminal
            print(f"Block number {block.number}:\n"
                  f"\nTRANSACTION FEES\n"
                  f"Min fee per transaction in this block was {self.min_fee} gwei.\n"
                  f"Avg fee per transaction in this block was {self.avg_fee} gwei.\n"
                  f"Max fee per transaction in this block was {self.max_fee} gwei.\n"
                  f"\nGAS PRICES\n"
                  f"Base Fee in this block was {self.base_fee_gwei} gwei.\n"
                  f"Min gas price was {self.min_gas_price} gwei.\n"
                  f"Avg gas price was {self.avg_gas_price} gwei.\n"
                  f"Max gas price was {self.max_gas_price} gwei.\n"
                  f"\n≡\n")

            # Set the new value to block_number variable to avoid printing duplicit blocks
            self.block_number = block.number

# Run
run_the_monitor = feeMonitor()
run_the_monitor.schedule()