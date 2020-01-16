import json

from eth_keys.datatypes import PrivateKey
from web3 import Web3

from polyswarmartifact import ArtifactType
from polyswarmtransaction.transaction import SignedTransaction
from polyswarmtransaction.nectar import WithdrawalTransaction


def test_recover_withdrawal_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "amount": "2000000000000000000",
         }
    }
    transaction = WithdrawalTransaction("2000000000000000000")
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_withdrawal_transaction(ethereum_accounts):
    signature = '0x92787e13b8b556e24d5316e58a344b3feca1b5559571de63eb64160e874bfb78710848fd20e6fe45c5cb19b0adee22ccf1' \
                '248eefe3fd8ad39e47281ee25b2b8d01'
    data = '{' \
        '"name": "polyswarmtransaction.nectar:WithdrawalTransaction", '\
        '"from": "0x3f17f1962B36e491b30A40b2405849e597Ba5FB5", ' \
        '"data": {' \
            '"amount": "2000000000000000000"' \
        '}' \
    '}'
    transaction = WithdrawalTransaction("2000000000000000000")
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.transaction == data
    assert signed.signature.hex() == signature


def test_recover_withdrawal_signed_transaction(ethereum_accounts):
    transaction = WithdrawalTransaction("2000000000000000000")
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction_from_parts():
    signature = '0x92787e13b8b556e24d5316e58a344b3feca1b5559571de63eb64160e874bfb78710848fd20e6fe45c5cb19b0adee22ccf1' \
                '248eefe3fd8ad39e47281ee25b2b8d01'
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "amount": "2000000000000000000",
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = WithdrawalTransaction("2000000000000000000")
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'
