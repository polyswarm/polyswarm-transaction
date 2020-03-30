import json

from deepdiff import DeepDiff
from eth_keys.datatypes import PrivateKey
from web3 import Web3

from polyswarmtransaction.transaction import SignedTransaction
from polyswarmtransaction.nectar import WithdrawalTransaction, DepositTransaction


def test_recover_deposit_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.nectar:DepositTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    transaction = DepositTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_recover_withdrawal_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    transaction = WithdrawalTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_deposit_transaction(ethereum_accounts):
    signature = ('0x59af24d65251f562dd8be5126917911aa1a660c8f5ce223f48e505ad664b2b4f087acb1a54afc1dc15ce8205cb3d8bf1472'
                 'aaa765b1507b30934d4eb2047778e00')
    data = {
        'name': 'polyswarmtransaction.nectar:DepositTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    transaction = DepositTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_sign_withdrawal_transaction(ethereum_accounts):
    signature = '0x92787e13b8b556e24d5316e58a344b3feca1b5559571de63eb64160e874bfb78710848fd20e6fe45c5cb19b0adee22ccf1' \
                '248eefe3fd8ad39e47281ee25b2b8d01'
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    transaction = WithdrawalTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_recover_deposit_signed_transaction(ethereum_accounts):
    transaction = DepositTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction(ethereum_accounts):
    transaction = WithdrawalTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_deposit_signed_transaction_from_parts():
    signature = ('0x59af24d65251f562dd8be5126917911aa1a660c8f5ce223f48e505ad664b2b4f087acb1a54afc1dc15ce8205cb3d8bf1472'
                 'aaa765b1507b30934d4eb2047778e00')
    data = {
        'name': 'polyswarmtransaction.nectar:DepositTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction_from_parts():
    signature = '0x92787e13b8b556e24d5316e58a344b3feca1b5559571de63eb64160e874bfb78710848fd20e6fe45c5cb19b0adee22ccf1' \
                '248eefe3fd8ad39e47281ee25b2b8d01'
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_deposit_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = DepositTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = WithdrawalTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_load_deposit():
    data = {
        'name': 'polyswarmtransaction.nectar:DepositTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '200000000000000000'
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    assert isinstance(signed.transaction(), DepositTransaction)
    assert not DeepDiff(signed.transaction().data, DepositTransaction('200000000000000000').data, ignore_order=True)


def test_load_withdrawal():
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '200000000000000000'
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    assert isinstance(signed.transaction(), WithdrawalTransaction)
    assert not DeepDiff(signed.transaction().data, WithdrawalTransaction('200000000000000000').data, ignore_order=True)
