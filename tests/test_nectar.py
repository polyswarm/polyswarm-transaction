import json

from deepdiff import DeepDiff
from eth_keys.datatypes import PrivateKey
from web3 import Web3

from polyswarmtransaction.transaction import SignedTransaction
from polyswarmtransaction.nectar import WithdrawalTransaction, ApproveNectarReleaseTransaction


def test_recover_release_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.nectar:ApproveNectarReleaseTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'destination': '0x0000000000000000000000000000000000000001',
            'amount': '200000000000000000',
            'transaction_hash': '0x0000000000000000000000000000000',
            'block_hash': '0x0000000000000000000000000000000',
            'block_number': '0x1',
        }
    }
    transaction = ApproveNectarReleaseTransaction(destination='0x0000000000000000000000000000000000000001',
                                       amount='200000000000000000',
                                       transaction_hash='0x0000000000000000000000000000000',
                                       block_hash='0x0000000000000000000000000000000',
                                       block_number='0x1')
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


def test_sign_release_transaction(ethereum_accounts):
    signature = ('0xf042ad34990ad9117a6bc0931842f6b82e1605979b41e28cd93ea256cfa4d4624c71082e383ddbb6795faa4843f3960cb' 
                 'fbca1e9aac375dd40c0136ed32946bb00')
    data = {
        'name': 'polyswarmtransaction.nectar:ApproveNectarReleaseTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'destination': '0x0000000000000000000000000000000000000001',
            'amount': '200000000000000000',
            'transaction_hash': '0x0000000000000000000000000000000',
            'block_hash': '0x0000000000000000000000000000000',
            'block_number': '0x1',
        }
    }
    transaction = ApproveNectarReleaseTransaction(destination='0x0000000000000000000000000000000000000001',
                                       amount='200000000000000000',
                                       transaction_hash='0x0000000000000000000000000000000',
                                       block_hash='0x0000000000000000000000000000000',
                                       block_number='0x1')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_sign_withdrawal_transaction(ethereum_accounts):
    signature = ('0x92787e13b8b556e24d5316e58a344b3feca1b5559571de63eb64160e874bfb78710848fd20e6fe45c5cb19b0adee22ccf1' 
                 '248eefe3fd8ad39e47281ee25b2b8d01')
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


def test_recover_release_signed_transaction(ethereum_accounts):
    transaction = ApproveNectarReleaseTransaction(destination='0x0000000000000000000000000000000000000001',
                                       amount='200000000000000000',
                                       transaction_hash='0x0000000000000000000000000000000',
                                       block_hash='0x0000000000000000000000000000000',
                                       block_number='0x1')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction(ethereum_accounts):
    transaction = WithdrawalTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_release_signed_transaction_from_parts():
    signature = ('0xf042ad34990ad9117a6bc0931842f6b82e1605979b41e28cd93ea256cfa4d4624c71082e383ddbb6795faa4843f3960cb' 
                 'fbca1e9aac375dd40c0136ed32946bb00')
    data = {
        'name': 'polyswarmtransaction.nectar:ApproveNectarReleaseTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'destination': '0x0000000000000000000000000000000000000001',
            'amount': '200000000000000000',
            'transaction_hash': '0x0000000000000000000000000000000',
            'block_hash': '0x0000000000000000000000000000000',
            'block_number': '0x1',
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction_from_parts():
    signature = ('0x92787e13b8b556e24d5316e58a344b3feca1b5559571de63eb64160e874bfb78710848fd20e6fe45c5cb19b0adee22ccf1'
                 '248eefe3fd8ad39e47281ee25b2b8d01')
    data = {
        'name': 'polyswarmtransaction.nectar:WithdrawalTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'amount': '2000000000000000000'
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_release_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = ApproveNectarReleaseTransaction(destination='0x0000000000000000000000000000000000000001',
                                       amount='200000000000000000',
                                       transaction_hash='0x0000000000000000000000000000000',
                                       block_hash='0x0000000000000000000000000000000',
                                       block_number='0x1')
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_withdrawal_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = WithdrawalTransaction('2000000000000000000')
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_load_approve_release():
    data = {
        'name': 'polyswarmtransaction.nectar:ApproveNectarReleaseTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'destination': '0x0000000000000000000000000000000000000001',
            'amount': '200000000000000000',
            'transaction_hash': '0x0000000000000000000000000000000',
            'block_hash': '0x0000000000000000000000000000000',
            'block_number': '0x1',
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))

    approve_nct_release = ApproveNectarReleaseTransaction(destination='0x0000000000000000000000000000000000000001',
                                               amount='200000000000000000',
                                               transaction_hash='0x0000000000000000000000000000000',
                                               block_hash='0x0000000000000000000000000000000',
                                               block_number='0x1')
    assert isinstance(signed.transaction(), ApproveNectarReleaseTransaction)
    assert not DeepDiff(signed.transaction().data, approve_nct_release.data, ignore_order=True)


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
