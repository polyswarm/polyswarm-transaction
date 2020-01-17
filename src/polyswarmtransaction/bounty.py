from typing import Dict, Any, List
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
    artifact_type: str
    metadata: List[Dict[str, Any]]

    def __init__(self, guid: uuid4, reward: str, artifact: str, artifact_type: str, metadata: List[Dict[str, Any]], expiration: int, **kwargs):
        self.guid = guid
        self.reward = reward
        self.artifact = artifact
        self.artifact_type = artifact_type

        if not BountyMetadata.validate(metadata):
            raise ValueError

        self.metadata = metadata
        self.expiration = expiration

    @property
    def data(self) -> Dict[str, Any]:
        return {
            'guid': str(self.guid),
            'reward': self.reward,
            'artifact': self.artifact,
            'artifact_type': self.artifact_type,
            'expiration': self.expiration,
            'metadata': self.metadata
        }


class AssertionTransaction(Transaction):
    guid: uuid4
    verdict: bool
    bid: str
    metadata: Dict[str, Any]

    def __init__(self, guid: uuid4, verdict: bool, bid: str, metadata: Dict[str, Any], **kwargs):
        self.guid = guid
        self.verdict = verdict
        self.bid = bid
        if not VerdictMetadata.validate(metadata):
            raise ValueError

        self.metadata = metadata

    @property
    def data(self) -> Dict[str, Any]:
        return {
            'guid': str(self.guid),
            'verdict': self.verdict,
            'bid': self.bid,
            'metadata': self.metadata
        }


class VoteTransaction(Transaction):
    guid: uuid4
    vote: bool

    def __init__(self, guid: uuid4, vote: bool, **kwargs):
        self.guid = guid
        self.vote = vote

    @property
    def data(self) -> Dict[str, Any]:
        return {
            'guid': str(self.guid),
            'vote': self.vote,
        }
