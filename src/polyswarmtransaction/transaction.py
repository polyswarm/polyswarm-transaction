import json

from eth_keys.datatypes import PrivateKey, Signature
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from typing import Any, Dict, Union


class Transaction:
    @property
    def data(self) -> Dict[str, Any]:
        return {}

    @property
    def hashed(self) -> bytes:
        return Web3.keccak(text=json.dumps(self.data))

    def sign(self, private_key: HexBytes) -> 'SignedTransaction':
        signature = PrivateKey(private_key).sign_msg_hash(self.hashed)
        return SignedTransaction(self, signature.to_bytes())


class SignedTransaction:
    transaction: Transaction
    signature: HexBytes

    def __init__(self, transaction: Transaction, signature: Union[bytes, str, int]):
        self.transaction = transaction
        self.signature = HexBytes(signature)

    def ecrecover(self) -> ChecksumAddress:
        signature = Signature(signature_bytes=bytes(self.signature))
        return signature.recover_public_key_from_msg_hash(self.transaction.hashed).to_checksum_address()
