import time
import random
import copy


class Block(object):
    def __init__(self, miner, time):
        self.miner = miner
        self.time = time


class Miner(object):
    def __init__(self, name, type, suc_prob):
        ''' name - `str`
            type - 'benign' or 'malicious'
        '''
        self.name = name
        self.type = type
        
        # parameters
        self.query_time = 100
        self.probability = suc_prob

    def mine_block(self, block_chains):

        # get one longest
        picked_chain = copy.deepcopy(block_chains.get_longest_chain())

        for i in range(self.query_time):
            if random.random() < self.probability:
                # generate new block
                new_block = Block(miner=self, time=time.time())
                picked_chain.append(new_block)
                
                if self.type == 'benign':
                    break
        
        return picked_chain


class Chain(object):
    def __init__(self):
        self.blocks = [self.generate_genesis()]

    def __len__(self):
        return len(self.blocks)    
    
    def generate_genesis(self):
        miner = Miner(name='god', type='benign', suc_prob=None)
        block = Block(miner, time.time())
        return block
    
    def append(self, block:Block):
        self.blocks.append(block)
    
    def check_attacked(self):
        ''' Check if the chain is attacked
            Check if there is a block created by malicious node
        '''
        for block in self.blocks:
            if block.miner.type == 'malicious':
                return True
        return False

    def __str__(self):
        ret_str = ''
        for block in self.blocks:
            ret_str += block.miner.name + ' '
        return ret_str


class BlockChains(object):
    def __init__(self):
        self.chains = [Chain()]
        self.max_len = 1

    def get_longest_chain(self):
        ''' Get the longest chain,
            if many chains have the same length, pick one randomly
        '''
        random.shuffle(self.chains)
        for chain in self.chains:
            if len(chain) == self.max_len:
                return chain
    
    def update(self, chain_list, maxlen):
        self.chains = chain_list
        self.max_len = maxlen

    def check_attacked(self):
        ''' Check if system is attacked 
            Check if there is one good chain
        '''
        for chain in self.chains:
            if chain.check_attacked() == False:
                return False
        return True

    def __str__(self):
        ''' Overload print '''
        ret_str = ''
        for idx, chain in enumerate(self.chains):
            ret_str += '{} {}\n'.format(idx, chain)
        return ret_str


def test_attack():
    # arguments
    num_benigns = [18, 16, 14, 12]
    num_malicious_s = [2, 4, 6, 8]
    suc_prob = 5e-4

    for num_benign, num_malicious in zip(num_benigns, num_malicious_s):

        # do 300 experiments
        for _ in range(300):
            statistics = 0
            counts = 0

            benign_miners = [
                Miner(name='benign_{}'.format(i), type='benign', suc_prob=suc_prob) for i in range(num_benign)]
            malicious_miners = [
                Miner(name='malicious_{}'.format(i), type='malicious', suc_prob=suc_prob) for i in range(num_malicious)]

            block_chains = BlockChains()

            # keep running until attacked
            while True:
                updated_chains = []
                # mine
                for miner in benign_miners:
                    updated_chains.append(miner.mine_block(block_chains))
                for miner in malicious_miners:
                    updated_chains.append(miner.mine_block(block_chains))
                
                # get max len
                maxlen = 0
                for chain in updated_chains:
                    if len(chain) > maxlen:
                        maxlen = len(chain)

                if maxlen > block_chains.max_len:
                    block_chains.update(list(filter(lambda x: len(x) == maxlen, updated_chains)), maxlen)

                if block_chains.check_attacked():
                    statistics += block_chains.max_len
                    counts += 1
                    break

        print('Benign: {}; Malicious: {}; Suc prob: {}; Attack len: {}'.format(
            num_benign, num_malicious, suc_prob, statistics/counts))


def test_num_nodes():
    num_rounds = 200

    # arguments
    num_benigns = [2, 5, 8, 11, 20, 50]
    suc_prob = 5e-5

    for num_benign in num_benigns:
        speed_statistics = 0.0

        # do 300 experiments
        for _ in range(300):
            statistics = 0
            counts = 0

            benign_miners = [
                Miner(name='benign_{}'.format(i), type='benign', suc_prob=suc_prob) for i in range(num_benign)]

            block_chains = BlockChains()

            # start running
            for rd in range(num_rounds):
                updated_chains = []
                # mine
                for miner in benign_miners:
                    updated_chains.append(miner.mine_block(block_chains))
                
                # get max len
                maxlen = 0
                for chain in updated_chains:
                    if len(chain) > maxlen:
                        maxlen = len(chain)

                if maxlen > block_chains.max_len:
                    block_chains.update(list(filter(lambda x: len(x) == maxlen, updated_chains)), maxlen)
            
            speed_statistics += num_rounds / block_chains.max_len
        
        # end 300 experiments
        print('Benign: {}; Suc prob: {}; Speed: 1 block / {:.2f} rounds'.format(
            num_benign, suc_prob, speed_statistics/300))


def test_prob():
    num_rounds = 200

    # arguments
    num_benign = 4
    suc_probs = [1e-5, 5e-5, 1e-4, 5e-4, 1e-3]

    for suc_prob in suc_probs:
        speed_statistics = 0.0

        # do 300 experiments
        for _ in range(300):
            statistics = 0
            counts = 0

            benign_miners = [
                Miner(name='benign_{}'.format(i), type='benign', suc_prob=suc_prob) for i in range(num_benign)]

            block_chains = BlockChains()

            # start running
            for rd in range(num_rounds):
                updated_chains = []
                # mine
                for miner in benign_miners:
                    updated_chains.append(miner.mine_block(block_chains))
                
                # get max len
                maxlen = 0
                for chain in updated_chains:
                    if len(chain) > maxlen:
                        maxlen = len(chain)

                if maxlen > block_chains.max_len:
                    block_chains.update(list(filter(lambda x: len(x) == maxlen, updated_chains)), maxlen)
            
            speed_statistics += num_rounds / block_chains.max_len
        
        # end 300 experiments
        print('Benign: {}; Suc prob: {}; Speed: 1 block / {:.2f} rounds'.format(
            num_benign, suc_prob, speed_statistics/300))


if __name__ == '__main__':
    # test_attack()
    # test_num_nodes()
    test_prob()

