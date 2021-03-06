import json
import pytest

from deepdiff import DeepDiff
from eth_keys.datatypes import PrivateKey
from web3 import Web3

from polyswarmartifact import ArtifactType
from polyswarmartifact.schema.bounty import Bounty as BountyMetadata
from polyswarmartifact.schema.verdict import Verdict as VerdictMetadata, Scanner
from polyswarmtransaction.transaction import SignedTransaction
from polyswarmtransaction.bounty import BountyTransaction, AssertionTransaction, VoteTransaction


BOUNTY_METADATA = json.loads(BountyMetadata().add_file_artifact(mimetype='').json())
ASSERTION_METADATA = json.loads(VerdictMetadata().set_malware_family('').json())


def test_recover_bounty_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'reward': '2000000000000000000',
            'artifact': 'Qm',
            'artifact_type': 0,
            'duration': 123,
            'metadata': [{'mimetype': ''}]
         }
    }
    transaction = BountyTransaction('test', '2000000000000000000', 'Qm', ArtifactType.FILE.value, 123, BOUNTY_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_bounty_transaction(ethereum_accounts):
    signature = ('0x2593843d5ef54ba3588e2d8a9a2b205124612787d7309736ae430dc99c0e797b2ac7975ffc405ff551ef17ae16993fdfca'
                 '22310cb71d638d8971ec51cefd49ec01')
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'reward': '2000000000000000000',
            'artifact': 'Qm',
            'artifact_type': 0,
            'duration': 123,
            'metadata': [{'mimetype': ''}]
        }
    }
    transaction = BountyTransaction('test', '2000000000000000000', 'Qm', ArtifactType.FILE.value, 123, BOUNTY_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_recover_bounty_signed_transaction(ethereum_accounts):
    transaction = BountyTransaction('test', '2000000000000000000', 'Qm', ArtifactType.FILE.value, 123, BOUNTY_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_bounty_signed_transaction_from_parts():
    signature = ('0x2593843d5ef54ba3588e2d8a9a2b205124612787d7309736ae430dc99c0e797b2ac7975ffc405ff551ef17ae16993fdfca'
                 '22310cb71d638d8971ec51cefd49ec01')
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'reward': '2000000000000000000',
            'artifact': 'Qm',
            'artifact_type': 0,
            'duration': 123,
            'metadata': [{'mimetype': ''}]
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_bounty_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = BountyTransaction('test', '2000000000000000000', 'Qm', ArtifactType.FILE.value, 123, BOUNTY_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_load_bounty():
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'reward': '2000000000000000000',
            'artifact': 'Qm',
            'artifact_type': 0,
            'duration': 123,
            'metadata': [{'mimetype': ''}]
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    assert isinstance(signed.transaction(), BountyTransaction)
    assert not DeepDiff(signed.transaction().data,
                        BountyTransaction('test',
                                          '2000000000000000000',
                                          'Qm',
                                          ArtifactType.FILE.value,
                                          123,
                                          BOUNTY_METADATA).data,
                        ignore_order=True)


def test_load_bounty_bad_metadata():
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'reward': '2000000000000000000',
            'artifact': 'Qm',
            'artifact_type': 0,
            'duration': 123,
            'metadata': []
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    with pytest.raises(ValueError):
        assert signed.transaction()


def test_load_bounty_bad_artifact_type():
    data = {
        'name': 'polyswarmtransaction.bounty:BountyTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'reward': '2000000000000000000',
            'artifact': 'Qm',
            'artifact_type': 4,
            'duration': 123,
            'metadata': [{'mimetype': ''}]
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    with pytest.raises(ValueError):
        assert signed.transaction()


def test_recover_assertion_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'verdict': True,
            'bid': '1000000000000000000',
            'metadata': {'malware_family': ''}
         }
    }
    transaction = AssertionTransaction('test', True, '1000000000000000000', ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_full_metadata(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'verdict': True,
            'bid': '1000000000000000000',
            'metadata': {
                'malware_family': '',
                'domains': ['test-domain'],
                'ip_addresses': ['127.0.0.1'],
                'stix': [{'schema': '', 'signature': 'test-stix'}],
                'scanner': {
                    'version': '1.0.0',
                    'polyswarmclient_version': '2.8.0',
                    'vendor_version': '1',
                    'signatures_version': '0.1.0',
                    'environment': {
                        'operating_system': 'test-os',
                        'architecture': 'test-arch',
                    }
                },
                'extra': 'extra'
            }
         }
    }

    scanner = json.loads(
        Scanner(environment={'operating_system': 'test-os', 'architecture': 'test-arch'}, version='1.0.0',
                polyswarmclient_version='2.8.0', signatures_version='0.1.0', vendor_version='1').json())
    metadata = json.loads(VerdictMetadata()
                          .set_malware_family('')
                          .set_scanner(**scanner)
                          .add_domain('test-domain')
                          .add_ip_address('127.0.0.1')
                          .add_stix_signature('', 'test-stix')
                          .add_extra('extra', 'extra').json())

    transaction = AssertionTransaction('test', True, '1000000000000000000', metadata)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_assertion_transaction(ethereum_accounts):
    signature = ('0x0b2e16aff5f17c95434d06201514c20aed27d899649679cce01327afca495d3c17fc9f8f12551031aeae28a744be4fddf6'
                 '8b46155b24472d6f9d0da0ffa5376c00')
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'verdict': True,
            'bid': '1000000000000000000',
            'metadata': {'malware_family': ''}
        }
    }
    transaction = AssertionTransaction('test', True, '1000000000000000000', ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_recover_assertion_signed_transaction(ethereum_accounts):
    transaction = AssertionTransaction('test', True, '1000000000000000000', ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_assertion_signed_transaction_from_parts():
    signature = ('0x0b2e16aff5f17c95434d06201514c20aed27d899649679cce01327afca495d3c17fc9f8f12551031aeae28a744be4fddf6'
                 '8b46155b24472d6f9d0da0ffa5376c00')
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'verdict': True,
            'bid': '1000000000000000000',
            'metadata': {'malware_family': ''}
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_assertion_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = AssertionTransaction('test', True, '1000000000000000000', ASSERTION_METADATA)
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_load_assertion():
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'verdict': True,
            'bid': '1000000000000000000',
            'metadata': {'malware_family': ''}
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    assert isinstance(signed.transaction(), AssertionTransaction)
    assert not DeepDiff(signed.transaction().data,
                        AssertionTransaction('test', True, '1000000000000000000', ASSERTION_METADATA).data,
                        ignore_order=True)


def test_load_assertion_bad_metadata():
    data = {
        'name': 'polyswarmtransaction.bounty:AssertionTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'verdict': True,
            'bid': '1000000000000000000',
            'metadata': {}
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    with pytest.raises(ValueError):
        assert signed.transaction()


def test_recover_vote_when_computed(ethereum_accounts):
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'vote': True,
         }
    }
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.signature == PrivateKey(ethereum_accounts[0].key).sign_msg_hash(Web3.keccak(text=json.dumps(data)))


def test_sign_vote_transaction(ethereum_accounts):
    signature = ('0xc04b6d31e94c26faa039b899e4c58adecc74bff57b3985668f5ba59ce27a0bf301d41b1b07a1117d6c16d6bb31a44da680'
                 'e215178c121988462be4891d86935101')
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'vote': True,
        }
    }
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.raw_transaction == json.dumps(data)
    assert signed.signature.hex() == signature


def test_recover_vote_signed_transaction(ethereum_accounts):
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_vote_signed_transaction_from_parts():
    signature = ('0xc04b6d31e94c26faa039b899e4c58adecc74bff57b3985668f5ba59ce27a0bf301d41b1b07a1117d6c16d6bb31a44da680'
                 'e215178c121988462be4891d86935101')
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'vote': True,
        }
    }
    signed = SignedTransaction(json.dumps(data), signature)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_recover_vote_signed_transaction_from_signed_output(ethereum_accounts):
    transaction = VoteTransaction('test', True)
    signed = transaction.sign(ethereum_accounts[0].key)
    signed = SignedTransaction(**signed.payload)
    assert signed.ecrecover() == '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5'


def test_load_vote():
    data = {
        'name': 'polyswarmtransaction.bounty:VoteTransaction',
        'from': '0x3f17f1962B36e491b30A40b2405849e597Ba5FB5',
        'data': {
            'guid': 'test',
            'vote': True,
        }
    }
    signed = SignedTransaction(json.dumps(data), bytes([0] * 65))
    assert isinstance(signed.transaction(), VoteTransaction)
    assert not DeepDiff(signed.transaction().data, VoteTransaction('test', True).data, ignore_order=True)
