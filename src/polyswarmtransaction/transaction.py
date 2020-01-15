import json

from eth_keys.datatypes import PrivateKey, Signature
from eth_keys.exceptions import ValidationError
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from typing import Any, Dict, Union

from polyswarmtransaction.exceptions import InvalidKeyError, InvalidSignatureError


class Transaction:
    @property
    def data(self) -> Dict[str, Any]:
        return {}

    @property
    def hashed(self) -> bytes:
        return Web3.keccak(text=json.dumps(self.data))

    def sign(self, private_key: HexBytes) -> 'SignedTransaction':
        try:
            signature = PrivateKey(private_key).sign_msg_hash(self.hashed)
        except ValidationError:
            raise InvalidKeyError(f'{private_key} is not a valid ethereum private key')
        return SignedTransaction(self, signature.to_bytes())


class SignedTransaction:
    transaction: Transaction
    signature: HexBytes

    def __init__(self, transaction: Transaction, signature: Union[bytes, str, int]):
        self.transaction = transaction
        self.signature = HexBytes(signature)

    def ecrecover(self) -> ChecksumAddress:
        try:
            signature = Signature(signature_bytes=bytes(self.signature))
        except (TypeError, ValidationError):
            raise InvalidSignatureError(f'{self.signature} is not a valid signature')

        return signature.recover_public_key_from_msg_hash(self.transaction.hashed).to_checksum_address()
