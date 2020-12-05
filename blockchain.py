from block import Block
import time
from transcation import Transaction


class BlockChain:
    def __init__(self):
        self.chain = [self._genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []
        self.mining_reward = 200

    def _genesis_block(self):
        block = Block(
            timestamp=time.time(),
            transactions=[],
            prev_hash='')
        return block

    @property
    def latest_block(self):
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, reward_addr):
        block = Block(time.time(), self.pending_transactions, self.latest_block.hash)
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, reward_addr, self.mining_reward)]
    
    def get_balance(self, addr):
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                if trans.from_addr == addr:
                    balance -= trans.amount
                if trans.to_addr == addr:
                    balance += trans.amount
        return balance
    
    def verify(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i-1]
            if curr_block.hash != curr_block.calculate_hash():
                return False
            if curr_block.prev_hash != prev_block.calculate_hash():
                return False
        
        return True
    

if __name__ == '__main__':
    blockchain = BlockChain()

    blockchain.add_transaction(Transaction('bowen', 'duan', 100))
    blockchain.add_transaction(Transaction('duan', 'bowen', 50))

    blockchain.mine_pending_transactions('bowen')
    blockchain.mine_pending_transactions('bowen')

    for addr in ['bowen', 'duan']:
        print('Balance of {}: {}'.format(addr, blockchain.get_balance(addr)))
    
