import requests
from core.wallet.wallet import Wallet
import time

BASE_URL = 'http://localhost:5000'


def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()


def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transact(recipient, amount):
    return requests.post(f'{BASE_URL}/wallet/transact',
                         json={
                             'recipient': recipient,
                             'amount': amount
                         }).json()


def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()


start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

recipient = Wallet().address

post_wallet_transact_for_first_time = post_wallet_transact(recipient, 45)
print(
    f'\npost_wallet_transact_for_first_time: {post_wallet_transact_for_first_time}'
)
time.sleep(1)
post_wallet_transact_for_second_time = post_wallet_transact(recipient, 90)
print(
    f'\npost_wallet_transact_for_second_time: {post_wallet_transact_for_second_time}'
)

time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined_block: {mined_block}')

wallet_info = get_wallet_info()
print(f'\nwallet_info: {wallet_info}')