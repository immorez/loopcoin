from core.wallet.transaction_pool import TransactionPool
from core.wallet.transaction import Transaction
from core.wallet.wallet import Wallet
from core.blockchain.blockchain import Blockchain


def test_set_transaction():
    """Test that a transaction is set into transactions pool"""
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    transaction1 = Transaction(Wallet(), 'recipient', 1)
    transaction2 = Transaction(Wallet(), 'recipient', 2)

    transaction_pool.set_transaction(transaction1)
    transaction_pool.set_transaction(transaction2)

    blockchain = Blockchain()
    blockchain.add_block([transaction1.to_json(), transaction2.to_json()])

    assert transaction1.id in transaction_pool.transaction_map
    assert transaction2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert transaction1.id not in transaction_pool.transaction_map
    assert transaction2.id not in transaction_pool.transaction_map