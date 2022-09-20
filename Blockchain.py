# Implementing Blockchain with Proof-of-Authority consensus.
from hashlib import sha256
import random


class Blockchain:
    def __init__(self) -> None:
        self.peers = []  # set of peers
        self.validators = []  # set of validators(authorized persons.)
        self.blocks = []
        self.transaction_pool = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            "prev_hash": "gensis",
            "curr_hash": "",
            "transactions": "",
            "validator_id": "genesis"  # leadership team will track who added the block
        }
        genesis_block['curr_hash'] = sha256(
            str(genesis_block).encode()).hexdigest()
        self.blocks.append(genesis_block)

    def show_blocks(self):
        return self.blocks

    # adding transaction without checking sender and receiver existence (checked in mine fuunction)
    def add_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def add_peer(self, peer):
        self.peers.append(peer)

    def add_validator(self, validator):
        self.validators.append(validator)

    def mine(self):
        # first pick random validator
        if len(self.validators) == 0:
            return False
        validator = random.choice(self.validators)
        validator_country_id = validator['country_id']

        valid_transactions = []
        for transaction in self.transaction_pool:
            peer_sender = None  # neglecting double spending condition
            peer_receiver = None
            for i in range(len(self.peers)):
                if transaction['sender'] == self.peers[i]['public_key']:
                    peer_sender = i
                if transaction['receiver'] == self.peers[i]['public_key']:
                    peer_receiver = i
            if transaction['amount'] > self.peers[peer_sender]['amount'] or peer_sender == None or peer_receiver == None:
                continue  # skip the transaction
            self.peers[peer_sender]['amount'] -= transaction['amount']
            self.peers[peer_receiver]['amount'] += transaction['amount']
            valid_transactions.append(transaction)
        new_block = {
            "transactions": valid_transactions,
            "prev_hash": "",
            "curr_hash": "",
            "validator_id": validator_country_id
        }
        new_block['prev_hash'] = self.blocks[-1]['curr_hash']
        new_block['curr_hash'] = sha256(str(new_block).encode()).hexdigest()
        self.blocks.append(new_block)
        self.transaction_pool.clear()
        return True

    def view_all_transactions(self):
        return self.transaction_pool

    def view_all_peers(self):
        return self.peers

    def view_all_validators(self):
        return self.validators
