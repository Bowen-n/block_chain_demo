import json
import time
import hashlib
from transcation import TransactionEncoder


class Block:
    def __init__(self, timestamp, transactions, prev_hash=''):
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    
    def calculate_hash(self):
        raw_block = self.prev_hash + \
                    str(self.timestamp) + \
                    json.dumps(self.transactions, ensure_ascii=False, cls=TransactionEncoder) + \
                    str(self.nonce)
        sha256 = hashlib.sha256()
        sha256.update(raw_block.encode('utf-8'))
        hash = sha256.hexdigest()
        return hash

    
    def mine(self, difficulty):
        since = time.time()

        while self.hash[0: difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print('Block mined: {}, time: {}s'.format(self.hash, time.time()-since))