import json
from typing import Dict, Any
from uuid import uuid4

from polyswarmtransaction.transaction import Transaction
from polyswarmartifact import ArtifactType
from polyswarmartifact.schema.bounty import Bounty as BountyMetadata
from polyswarmartifact.schema.verdict import Verdict as VerdictMetadata


class BountyTransaction(Transaction):
    guid: uuid4
    artifact: str
    expiration: int
    reward: str
    artifact_type: ArtifactType
    metadata: BountyMetadata

    def __init__(self, guid, reward, artifact, artifact_type, metadata, expiration):
        self.guid = guid
        self.reward = reward
        self.artifact = artifact
        self.artifact_type = artifact_type
        self.metadata = metadata
        self.expiration = expiration

    @property
    def data(self) -> Dict[str, Any]:
        return {
            'guid': str(self.guid),
            'reward': self.reward,
            'artifact': self.artifact,
            'artifact_type': self.artifact_type.name,
            'expiration': self.expiration,
            'metadata': self.metadata.artifacts
        }


class AssertionTransaction(Transaction):
    guid: uuid4
    verdict: bool
    bid: str
    metadata: VerdictMetadata

    def __init__(self, guid, verdict, bid, metadata):
        self.guid = guid
        self.verdict = verdict
        self.bid = bid
        self.metadata = metadata

    @property
    def data(self) -> Dict[str, Any]:
        return {
            'guid': str(self.guid),
            'verdict': self.verdict,
            'bid': self.bid,
            'metadata': self.output_metadata()
        }

    def output_metadata(self):
        metadata = self.metadata
        result = {
            "malware_family": metadata.malware_family,
        }

        if metadata.scanner:
            result["scanner"] = metadata.scanner

        if metadata.domains:
            result['domains'] = metadata.domains

        if metadata.ip_addresses:
            result['ip_addresses'] = metadata.ip_addresses

        if metadata.stix:
            result['stix'] = metadata.stix

        if metadata.extra:
            for key, value in metadata.extra:
                result[key] = value

        return result

class VoteTransaction(Transaction):
    guid: uuid4
    vote: bool

    def __init__(self, guid, vote):
        self.guid = guid
        self.vote = vote

    @property
    def data(self) -> Dict[str, Any]:
        return {
            'guid': str(self.guid),
            'vote': self.vote,
        }
