import json

from eth_keys.datatypes import PrivateKey, Signature, PublicKey
from eth_keys.exceptions import ValidationError, BadSignature
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from typing import Any, Dict, Union, Tuple

from polyswarmtransaction.exceptions import InvalidKeyError, InvalidSignatureError, WrongSignatureError


class Transaction:
    @property
    def data(self) -> Dict[str, Any]:
        return {}

    def sign(self, private_key: HexBytes) -> 'SignedTransaction':
        key = Transaction.load_key(private_key)
        message = self.__message(key.public_key)
        signature = Transaction.sign_message(message, key)
        return SignedTransaction(message, signature.to_bytes())

    def __message(self, public_key: PublicKey) -> str:
        body = {
            "name": f'{self.__class__.__module__}:{self.__class__.__name__}',
            "from": public_key.to_checksum_address(),
            "data": self.data
        }
        return json.dumps(body)

    @staticmethod
    def load_key(private_key: HexBytes) -> PrivateKey:
        try:
            return PrivateKey(private_key)
        except ValidationError:
            raise InvalidKeyError(f'{private_key} is not a valid ethereum private key')

    @staticmethod
    def sign_message(message: str, private_key: PrivateKey):
        return private_key.sign_msg_hash(Transaction.hash(message))

    @staticmethod
    def hash(message: str) -> bytes:
        return Web3.keccak(text=message)


class SignedTransaction:
    transaction: str
    signature: HexBytes

    def __init__(self, transaction: str, signature: Union[bytes, str, int]):
        self.transaction = transaction
        self.signature = HexBytes(signature)

    @property
    def payload(self) -> Dict[str, str]:
        return {
            'transaction': self.transaction,
            'signature': self.signature.hex()
        }

    def ecrecover(self) -> ChecksumAddress:
        public_key = self.__recover()
        self.__validate(public_key)
        return public_key.to_checksum_address()

    def __recover(self) -> PublicKey:
        message_hash = Transaction.hash(self.transaction)
        return PublicKey.recover_from_msg_hash(message_hash, self.__load_signature())

    def __load_signature(self) -> Signature:
        try:
            return Signature(signature_bytes=self.signature)
        except (TypeError, ValidationError, BadSignature):
            raise InvalidSignatureError(f'{self.signature} is not a valid signature')

    def __validate(self, public_key: PublicKey):
        from_address = json.loads(self.transaction)['from']
        if from_address != public_key.to_checksum_address():
            raise WrongSignatureError(f'{public_key.to_checksum_address()} did not match expected {from_address}')
