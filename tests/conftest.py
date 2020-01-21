import pytest

from eth_account.signers.local import LocalAccount
from typing import List
from web3.auto import w3


@pytest.fixture
def ethereum_accounts() -> List[LocalAccount]:
    return [w3.eth.account.from_key(bytes([i] * 32)) for i in range(3)]
