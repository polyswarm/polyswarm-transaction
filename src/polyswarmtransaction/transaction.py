import dataclasses
import json
import importlib
import importlib.util
import jsonschema

from eth_keys.datatypes import PrivateKey, Signature, PublicKey
from eth_keys.exceptions import ValidationError, BadSignature
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from types import ModuleType
from typing import Any, Dict, Union, Type, Tuple
from web3 import Web3

from polyswarmtransaction import exceptions

TRANSACTION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "transaction",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[^:]+:[^:]+$"
        },
        "from": {
            "type": "string",
            "minLength": 42,
            "maxLength": 42,
        },
        "data": {
            "type": "object",
            "additionalProperties": True
        },
    },
    "required": ["name", "from", "data"]
}


@dataclasses.dataclass
class Transaction:
    @property
    def data(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    def sign(self, private_key: HexBytes) -> 'SignedTransaction':
        key = self.load_key(private_key)
        message = self.__message(key.public_key)
        signature = self.sign_message(message, key)
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
            raise exceptions.InvalidKeyError(f'{private_key} is not a valid ethereum private key')

    @staticmethod
    def sign_message(message: str, private_key: PrivateKey):
        return private_key.sign_msg_hash(Transaction.hash(message))

    @staticmethod
    def hash(message: str) -> bytes:
        return Web3.keccak(text=message)


class SignedTransaction:
    raw_transaction: str
    signature: HexBytes

    def __init__(self, raw_transaction: str, signature: Union[bytes, str, int]):
        self.raw_transaction = raw_transaction
        self.signature = HexBytes(signature)

    @property
    def payload(self) -> Dict[str, str]:
        return {
            'raw_transaction': self.raw_transaction,
            'signature': self.signature.hex()
        }

    def ecrecover(self) -> ChecksumAddress:
        public_key = self.__recover()
        self.__validate(public_key)
        return public_key.to_checksum_address()

    def __recover(self) -> PublicKey:
        message_hash = Transaction.hash(self.raw_transaction)
        return PublicKey.recover_from_msg_hash(message_hash, self.__load_signature())

    def __load_signature(self) -> Signature:
        try:
            return Signature(signature_bytes=self.signature)
        except (TypeError, ValidationError, BadSignature):
            raise exceptions.InvalidSignatureError(f'{self.signature} is not a valid signature')

    def __validate(self, public_key: PublicKey):
        transaction_address = json.loads(self.raw_transaction)['from']
        recovered_address = public_key.to_checksum_address()
        if transaction_address != recovered_address:
            raise exceptions.WrongSignatureError(f'{recovered_address} did not match expected {transaction_address}')

    def transaction(self) -> Transaction:
        loaded = self.__load_validated_transaction()
        transaction = self.__import_transaction(loaded)
        return transaction(**loaded['data'])

    def __load_validated_transaction(self) -> Dict[str, Any]:
        loaded = json.loads(self.raw_transaction)
        jsonschema.validate(loaded, TRANSACTION_SCHEMA)
        return loaded

    def __import_transaction(self, loaded_transaction: Dict[str, Any]) -> Type[Transaction]:
        module_name, class_name = self.__get_transaction_module_name(loaded_transaction)
        module = self.__import_transaction_module(module_name)
        return self.__import_transaction_class(module, class_name)

    @staticmethod
    def __get_transaction_module_name(loaded_transaction: Dict[str, Any]) -> Tuple[str, str]:
        parts = loaded_transaction['name'].rsplit(':', 1)
        # Assuming this was checked by the schema first
        return parts[0], parts[1]

    @staticmethod
    def __import_transaction_module(module_name: str) -> ModuleType:
        mod_spec = importlib.util.find_spec(module_name)
        if not mod_spec:
            raise exceptions.UnsupportedTransactionError(f'Missing {module_name}')

        return importlib.import_module(mod_spec.name)

    @staticmethod
    def __import_transaction_class(module: ModuleType, class_name: str) -> Type[Transaction]:
        if not hasattr(module, class_name):
            raise exceptions.UnsupportedTransactionError(f'{module.__name__} has no class {class_name}')

        transaction = getattr(module, class_name)
        if not issubclass(transaction, Transaction):
            raise exceptions.UnsupportedTransactionError(f'{module.__name__}:{class_name} is not a Transaction')

        return transaction


@dataclasses.dataclass
class CustomTransaction(Transaction):
    raw_body: str = None
    data_body: str = None

    @property
    def data(self) -> Dict[str, Any]:
        return json.loads(self.data_body)

    def __message(self, public_key: PublicKey) -> str:
        if self.raw_body is not None:
            return self.raw_body

        body = {
            "name": f'{self.__class__.__module__}:{self.__class__.__name__}',
            "from": public_key.to_checksum_address(),
            "data": self.data
        }
        return json.dumps(body)
