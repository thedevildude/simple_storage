import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Solidity source code

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get Bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get ABI

abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"])["output"]["abi"]

# for connecting to Ganache

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/a3ea49b96ef34d07941ddf9ced846d10"))
chain_id = 4
my_address = "0x5Ca5c8F9F6eE93021199584f6809124cD2C03067"
private_key = "0xadc86f1da596202f655ba53e4693524758debd337e475f0012db4a7f3626c701"

# Create the contract in Python

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest Transaction

nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a transaction

transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce})

# 2. Sign a transaction

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)

# 3. Send a signed transaction
print("Deploying contract....")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract, we always need
# Contract Address
# Contract ABI

simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# Initial Value of Favorite Number
print(simple_storage.functions.retrieve().call())

print("Updating Contract....")
store_transaction = simple_storage.functions.store(16).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key = private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("Updated!")
print(simple_storage.functions.retrieve().call())
