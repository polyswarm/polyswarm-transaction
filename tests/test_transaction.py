import base64
import json

import pytest
from eth_account.signers.local import LocalAccount
from eth_keys.exceptions import BadSignature
from web3.auto import w3

from polyswarmtransaction.exceptions import InvalidKeyError, InvalidSignatureError
from polyswarmtransaction.transaction import Transaction, SignedTransaction


@pytest.fixture
def ethereum_account() -> LocalAccount:
    return w3.eth.account.from_key(bytes([0] * 32))


def test_sign_transaction(ethereum_account):
    expected = '0x02ce51e1210856898317649d643cfc8e28f451a17c463a2c4d3653fac505e3c17858aba69adc41bc81ac69fe31ae7c0c125' \
               'ff4648e1cf19b7dce0074759414bf01'
    expected_data = base64.b64encode(json.dumps({'name': 'Transaction', 'data': {}}).encode('utf-8'))
    transaction = Transaction()
    signed = transaction.sign(ethereum_account.key)
    assert signed.body == expected_data
    assert signed.signature.hex() == expected


def test_recover_signed_transaction(ethereum_account):
    transaction = Transaction()
    signed = transaction.sign(ethereum_account.key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_signed_transaction_from_parts():
    signature = '0x02ce51e1210856898317649d643cfc8e28f451a17c463a2c4d3653fac505e3c17858aba69adc41bc81ac69fe31ae7c0c125' \
               'ff4648e1cf19b7dce0074759414bf01'
    body = base64.b64encode(json.dumps({'name': 'Transaction', 'data': {}}).encode('utf-8'))
    signed = SignedTransaction(body, signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_signed_transaction_from_signed_output(ethereum_account):
    transaction = Transaction()
    signed = transaction.sign(ethereum_account.key)
    signed = SignedTransaction(**signed.output())
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_sign_none():
    transaction = Transaction()
    with pytest.raises(InvalidKeyError):
        transaction.sign(None)


def test_recover_empty_signature():
    signed = SignedTransaction(b'', '')
    with pytest.raises(InvalidSignatureError):
        signed.ecrecover()


def test_recover_invalid_signature():
    signed = SignedTransaction(b'', '0xaa')
    with pytest.raises(InvalidSignatureError):
        signed.ecrecover()


def test_recover_wrong_signature():
    signed = SignedTransaction(b'', bytes([0] * 65))
    with pytest.raises(BadSignature):
        signed.ecrecover()
