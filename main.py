

from hashlib import sha256
from time import time
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.keypair import Keypair
from solana.publickey import PublicKey

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

def create_solana_transaction(sender_private_key, receiver_public_key, amount):
    client = Client("https://api.devnet.solana.com")
    sender = Keypair.from_secret_key(bytes.fromhex(sender_private_key))
    receiver = PublicKey(receiver_public_key)

    transaction = Transaction()
    transaction.add(
        transfer(
            TransferParams(
                from_pubkey=sender.public_key,
                to_pubkey=receiver,
                lamports=amount
            )
        )
    )

    response = client.send_transaction(transaction, sender)
    return response

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una blockchain y añadir bloques
    blockchain = Blockchain()
    blockchain.add_block(Block(1, time(), {"amount": 4}))
    blockchain.add_block(Block(2, time(), {"amount": 10}))

    # Realizar una transacción en Solana
    sender_private_key = "your_sender_private_key"
    receiver_public_key = "your_receiver_public_key"
    amount = 1000000  # 1 SOL = 1,000,000 lamports

    response = create_solana_transaction(sender_private_key, receiver_public_key, amount)
    print(response)