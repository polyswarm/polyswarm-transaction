import json
import base64

from eth_keys.datatypes import PrivateKey, Signature
from eth_keys.exceptions import ValidationError
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from typing import Any, Dict, Union

from polyswarmtransaction.exceptions import InvalidKeyError, InvalidSignatureError


class Transaction:
    @staticmethod
    def hash(message: bytes) -> bytes:
        return Web3.keccak(message)

    @property
    def data(self) -> Dict[str, Any]:
        return {}

    def message(self):
        return base64.b64encode(json.dumps({"name": self.__class__.__name__, "data": self.data}).encode('utf-8'))

    def sign(self, private_key: HexBytes) -> 'SignedTransaction':
        message = self.message()
        signature = Transaction.sign_message(message, private_key)
        return SignedTransaction(message, signature.to_bytes())

    @staticmethod
    def sign_message(message: bytes, private_key: HexBytes):
        try:
            return PrivateKey(private_key).sign_msg_hash(Transaction.hash(message))
        except ValidationError:
            raise InvalidKeyError(f'{private_key} is not a valid ethereum private key')


class SignedTransaction:
    body: HexBytes
    signature: HexBytes

    def __init__(self, body: Union[bytes, str, int], signature: Union[bytes, str, int]):
        self.body = HexBytes(body)
        self.signature = HexBytes(signature)

    def output(self):
        return {
            "body": self.body.hex(),
            "signature": self.signature.hex()
        }

    def ecrecover(self) -> ChecksumAddress:
        try:
            signature = Signature(signature_bytes=self.signature)
        except (TypeError, ValidationError):
            raise InvalidSignatureError(f'{self.signature} is not a valid signature')

        return signature.recover_public_key_from_msg_hash(Transaction.hash(self.body)).to_checksum_address()
