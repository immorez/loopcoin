import time
import pytest
from core.blockchain.block import Block, GENESIS_DATA
from core.config import MINE_RATE, SECONDS
from core.util.hex_to_binary import hex_to_binary


def test_mine_block():
    last_block = Block.genesis_block()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(
        block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis = Block.genesis_block()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value


def test_increased_difficulty_mined_block():
    last_block = Block.mine_block(Block.genesis_block(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1


def test_decreased_difficulty_mined_block():
    last_block = Block.mine_block(Block.genesis_block(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash',
                       'test_data', 1, 0)

    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis_block()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')


def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'evil_last_hash'

    with pytest.raises(Exception, match='last_hash must be correct'):
        Block.is_valid_block(last_block, block)


def test_invalid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'

    with pytest.raises(Exception,
                       match='The proof of requirement was not met.'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}111abc'

    with pytest.raises(Exception,
                       match='The block difficulty must only adjust by 1.'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash = '000000000000000012abbbccccbc'

    with pytest.raises(Exception, match='The block hash must be correct.'):
        Block.is_valid_block(last_block, block)
