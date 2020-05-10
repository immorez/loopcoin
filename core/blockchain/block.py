import time
from core.util.crypto_hash import crypto_hash
from core.util.hex_to_binary import hex_to_binary
from core.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis-hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    A Block is a unit of storage.
    It will store transactions in blockchain
    which supports cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        block_repr = ('Block('
                      f'timestamp: {self.timestamp},\n'
                      f'last_hash: {self.last_hash},\n'
                      f'hash: {self.hash},\n'
                      f'data: {self.data},\n'
                      f'difficulty: {self.difficulty},\n'
                      f'nonce: {self.nonce})')
        return block_repr

    def __eq__(self, other):
        """
        This is a overwritten method of python which
        compares to object references.
        """
        return self.__dict__ == other.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data. Until a block hash
        is found that meets the leading 0's proof of work requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis_block():
        """
        Generate the gensis block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def deserialize_jsonified_block(jsonified_block):
        """
        Deserialize a block's json representation back into a block instance.
        It's result will be used in process of converting channel's message to
        a block instance. So, it will be usable for is_valid_block function. 
        """
        return Block(**jsonified_block)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for quickly mined blocks.
        Decrease the difficulty for slowly mined blocks.
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block by enforcing the following rules:
        - the block must have the proper last_hash reference.
        - the block must meet the proof of work requirement.
        - the difficulty must only adjust by 1.
        - the block hash must be a valid combination of the block fields.
        """
        if block.last_hash != last_block.hash:
            raise Exception('last_hash must be correct')

        if hex_to_binary(
                block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of requirement was not met.')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1.')

        reconstructed_hash = crypto_hash(block.timestamp, block.last_hash,
                                         block.data, block.nonce,
                                         block.difficulty)

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct.')

    def to_json(self):
        """
        Serialize the block into a dictionary of its attrs.
        """
        return self.__dict__


def main():
    genesis_block = Block.genesis_block()
    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil-data'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')


if __name__ == '__main__':
    main()