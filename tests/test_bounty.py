import json

from eth_keys.datatypes import PrivateKey
from web3 import Web3

from polyswarmartifact import ArtifactType
from polyswarmartifact.schema.bounty import Bounty as BountyMetadata
from polyswarmartifact.schema.verdict import Verdict as VerdictMetadata
from polyswarmtransaction.transaction import SignedTransaction
from polyswarmtransaction.bounty import BountyTransaction, AssertionTransaction, VoteTransaction

BOUNTY_METADATA = BountyMetadata().add_file_artifact('')
ASSERTION_METADATA = VerdictMetadata().set_malware_family('')


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


def test_recover_assertion_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "verdict": True,
            "bid": "1000000000000000000",
            "metadata": {'malware_family': ''}
         }
    }
    transaction = AssertionTransaction('test', True, "1000000000000000000", ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_full_metadata(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "verdict": True,
            "bid": "1000000000000000000",
            "metadata": {
                'malware_family': '',
                'scanner': {
                    'environment': {
                        'operating_system': 'test-os',
                        'architecture': 'test-arch',
                    },
                    'polyswarmclient_version': '2.8.0',
                    'version': '1.0.0',
                    'signatures_version': '0.1.0',
                    'vendor_version': '1'
                },
                'domains': ['test-domain'],
                'ip_addresses': ['127.0.0.1'],
                'stix': [{'schema': '', 'signature': 'test-stix'}],
                'extra': 'extra'
            }
         }
    }
    metadata = VerdictMetadata()\
        .set_malware_family('')\
        .set_scanner('test-os', 'test-arch', '1.0.0', '2.8.0', '0.1.0', '1')\
        .add_domain('test-domain')\
        .add_ip_address('127.0.0.1')\
        .add_stix_signature('', 'test-stix')\
        .add_extra('extra', 'extra')

    transaction = AssertionTransaction('test', True, "1000000000000000000", metadata)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.transaction == json.dumps(data)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_assertion_transaction(ethereum_accounts):
    signature = '0x0b2e16aff5f17c95434d06201514c20aed27d899649679cce01327afca495d3c17fc9f8f12551031aeae28a744be4fddf6' \
                '8b46155b24472d6f9d0da0ffa5376c00'
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "verdict": True,
            "bid": "1000000000000000000",
            "metadata": {'malware_family': ''}
        }
    }
    transaction = AssertionTransaction('test', True, "1000000000000000000", ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_recover_assertion_signed_transaction(ethereum_accounts):
    transaction = AssertionTransaction('test', True, "1000000000000000000", ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_assertion_signed_transaction_from_parts():
    signature = '0x0b2e16aff5f17c95434d06201514c20aed27d899649679cce01327afca495d3c17fc9f8f12551031aeae28a744be4fddf6' \
                '8b46155b24472d6f9d0da0ffa5376c00'
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "verdict": True,
            "bid": "1000000000000000000",
            "metadata": {'malware_family': ''}
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_assertion_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = AssertionTransaction('test', True, "1000000000000000000", ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_vote_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "vote": True,
         }
    }
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_vote_transaction(ethereum_accounts):
    signature = '0xc04b6d31e94c26faa039b899e4c58adecc74bff57b3985668f5ba59ce27a0bf301d41b1b07a1117d6c16d6bb31a44da680' \
                'e215178c121988462be4891d86935101'
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "vote": True,
        }
    }
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_recover_vote_signed_transaction(ethereum_accounts):
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_vote_signed_transaction_from_parts():
    signature = '0xc04b6d31e94c26faa039b899e4c58adecc74bff57b3985668f5ba59ce27a0bf301d41b1b07a1117d6c16d6bb31a44da680' \
                'e215178c121988462be4891d86935101'
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            "guid": "test",
            "vote": True,
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_vote_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'
