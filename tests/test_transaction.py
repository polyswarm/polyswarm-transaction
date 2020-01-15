import pytest
from eth_account.signers.local import LocalAccount
from web3.auto import w3

from polyswarmtransaction.transaction import Transaction


@pytest.fixture
def ethereum_account() -> LocalAccount:
    return w3.eth.account.from_key(bytes([0] * 32))


def test_sign_transaction(ethereum_account):
    expected = '0xc9eab3595d67c420579a6604bdb6f8e5d8d89bce5d7d166dc1e846c50ea471d60be55689ce21ed43ca85f01e019eb15d7d49'\
            '4849387b093b18fc6672da4475fc00'
    transaction = Transaction()
    signed = transaction.sign(ethereum_account.key)
    assert signed.transaction == transaction
    assert signed.signature.hex() == expected


def test_recover_signed_transaction(ethereum_account):
    transaction = Transaction()
    signed = transaction.sign(ethereum_account.key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'

