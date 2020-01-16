import json

import pytest
from eth_keys.datatypes import PrivateKey
from hexbytes import HexBytes

from polyswarmtransaction.exceptions import InvalidKeyError, InvalidSignatureError, WrongSignatureError
from polyswarmtransaction.transaction import Transaction, SignedTransaction
from web3 import Web3


def test_recover_when_computed(ethereum_accounts):
    # Must be a string exact match
    data = {
        'name': 'polyswarmtransaction.transaction:Transaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {}
    }
    signed = Transaction().sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_transaction(ethereum_accounts):
    expected = '0xed2e8602439eec57a84bb372c6de718d88d2c27f265d7c01fe59a940f9c44eb25f849639669897e376dca6b3e745f4d9667' \
               '32f731b6ec20d908673ad882aeed301'
    expected_body = {
        'name': 'polyswarmtransaction.transaction:Transaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {}
    }
    transaction = Transaction()
    signed = transaction.sign(ethereum_accounts[0].key)
    assert json.loads(signed.transaction) == expected_body
    assert signed.signature.hex() == expected


def test_recover_signed_transaction(ethereum_accounts):
    transaction = Transaction()
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_signed_transaction_from_parts():
    signature = '0xed2e8602439eec57a84bb372c6de718d88d2c27f265d7c01fe59a940f9c44eb25f849639669897e376dca6b3e745f4d9667' \
               '32f731b6ec20d908673ad882aeed301'
    # Must be a string exact match
    transaction = '{' \
           '"name": "polyswarmtransaction.transaction:Transaction", ' \
           '"from": "0x3f17f1962B36e491b30A40b2405849e597Ba5FB5", ' \
           '"data": {}}'
    signed = SignedTransaction(transaction, signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = Transaction()
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(signed.transaction, signed.signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_signed_transaction_from_payload(ethereum_accounts):
    transaction = Transaction()
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_sign_none():
    transaction = Transaction()
    with pytest.raises(InvalidKeyError):
        transaction.sign(None)


def test_recover_empty_signature():
    signed = SignedTransaction('', '')
    with pytest.raises(InvalidSignatureError):
        signed.ecrecover()


def test_recover_invalid_signature():
    signed = SignedTransaction('', '0xaa')
    with pytest.raises(InvalidSignatureError):
        signed.ecrecover()


def test_recover_changed_body(ethereum_accounts):
    signature = Transaction().sign(ethereum_accounts[0].key).signature
    body = '{' \
           '"name": "polyswarmtransaction.transaction:Transaction", ' \
           '"from": "0x3f17f1962B36e491b30A40b2405849e597Ba5FB5", ' \
               '"data": {' \
                   '"different": "asdf"' \
               '}' \
           '}'
    signed = SignedTransaction(body, signature)

    with pytest.raises(WrongSignatureError):
        signed.ecrecover()


def test_recover_changed_signature(ethereum_accounts):
    transaction = Transaction().sign(HexBytes(ethereum_accounts[0].key)).transaction
    signature = Transaction().sign(ethereum_accounts[1].key).signature
    signed = SignedTransaction(transaction, signature)

    with pytest.raises(WrongSignatureError):
        signed.ecrecover()
