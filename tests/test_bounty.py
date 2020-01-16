import json

from eth_keys.datatypes import PrivateKey
from web3 import Web3

from polyswarmartifact import ArtifactType
from polyswarmartifact.schema.bounty import Bounty as BountyMetadata
from polyswarmtransaction.transaction import SignedTransaction
from polyswarmtransaction.bounty import BountyTransaction, AssertTransaction, VoteTransaction

BOUNTY_METADATA = BountyMetadata().add_file_artifact('')


def test_recover_bounty_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "reward": "2000000000000000000",
            "artifact": "Qm",
            "artifact_type": "FILE",
            "expiration": 123,
            "metadata": [{'mimetype': ''}]
         }
    }
    transaction = BountyTransaction('test', "2000000000000000000", 'Qm', ArtifactType.FILE, BOUNTY_METADATA, 123)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_bounty_transaction(ethereum_accounts):
    signature = '0x64c865beaac6f182a579a373879e3f161a121ac756fa6f4cdec6e1ad6db988592b8314fcfbe6d07f324a581abdde9445cc' \
                '211154faf6399e10d5f8293be3de8201'
    data = '{' \
        '"name": "polyswarmtransaction.bounty:BountyTransaction", '\
        '"from": "0x3f17f1962B36e491b30A40b2405849e597Ba5FB5", ' \
        '"data": {' \
            '"guid": "test", ' \
            '"reward": "2000000000000000000", ' \
            '"artifact": "Qm", ' \
            '"artifact_type": "FILE", ' \
            '"expiration": 123, '\
            '"metadata": [{"mimetype": ""}]' \
        '}' \
    '}'
    transaction = BountyTransaction('test', "2000000000000000000", 'Qm', ArtifactType.FILE, BOUNTY_METADATA, 123)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.transaction == data
    assert signed.signature.hex() == signature


def test_recover_bounty_signed_transaction(ethereum_accounts):
    transaction = BountyTransaction('test', "2000000000000000000", 'Qm', ArtifactType.FILE, BOUNTY_METADATA, 123)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_bounty_signed_transaction_from_parts():
    signature = '0x64c865beaac6f182a579a373879e3f161a121ac756fa6f4cdec6e1ad6db988592b8314fcfbe6d07f324a581abdde9445cc' \
                '211154faf6399e10d5f8293be3de8201'
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "reward": "2000000000000000000",
            "artifact": "Qm",
            "artifact_type": "FILE",
            "expiration": 123,
            "metadata": [{'mimetype': ''}]
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_bounty_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = BountyTransaction('test', "2000000000000000000", 'Qm', ArtifactType.FILE, BOUNTY_METADATA, 123)
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'
