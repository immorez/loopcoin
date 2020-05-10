import os
import random
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from core.blockchain.blockchain import Blockchain
from core.pubsub import PubSub
from core.wallet.wallet import Wallet
from core.wallet.transaction import Transaction
from core.wallet.transaction_pool import TransactionPool

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)


@app.route('/')
def default():
    return 'Welcome to the blockchain application.'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/range')
def route_blockchain_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(blockchain.to_json()[::-1][start:end])


@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())


@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    # {'recipient': 'foo', 'amount': 15,}
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    # In python, objects are truthy and falsy.
    # Empty object acts like false.
    # False, None, 0, [], '' ~ FALSE
    if transaction:
        transaction.update(wallet, transaction_data['recipient'],
                           transaction_data['amount'])
    else:
        transaction = Transaction(wallet, transaction_data['recipient'],
                                  transaction_data['amount'])

    print(f'transaction.to_json(): {transaction.to_json()}')

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())


@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})


@app.route('/known-addresses')
def route_known_addresses():
    known_addresses = set()
    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())
    return jsonify(list(known_addresses))


@app.route('/transactions')
def route_transactions():
    return jsonify(transaction_pool.transaction_data())


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'result.json(): {result.json()}')

    result_blockchain = Blockchain.deserialize_jsonified_chain(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronized the local chain.')
    except Exception as e:
        print(f'\n -- Error synchronizing: {e} ')
if os.environ.get('SEED_DATA') == 'True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(),
                        Wallet().address, random.randint(2, 50)).to_json(),
            Transaction(Wallet(),
                        Wallet().address, random.randint(2, 50)).to_json()
        ])
    for i in range(3):
        transaction_pool.set_transaction(
            Transaction(Wallet(),
                        Wallet().address, random.randint(2, 50)), )

app.run(port=PORT)