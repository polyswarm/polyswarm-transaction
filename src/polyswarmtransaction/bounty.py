from typing import Dict, Any, List
from uuid import uuid4

import dataclasses
from polyswarmartifact import ArtifactType
from polyswarmtransaction.transaction import Transaction
from polyswarmartifact.schema.bounty import Bounty as BountyMetadata
from polyswarmartifact.schema.verdict import Verdict as VerdictMetadata


@dataclasses.dataclass
class BountyTransaction(Transaction):
    guid: uuid4
    reward: str
    artifact: str
    artifact_type: int
    duration: int
    metadata: List[Dict[str, Any]]

    def __post_init__(self):
        if not BountyMetadata.validate(self.metadata):
            raise ValueError

        if not ArtifactType(self.artifact_type):
            raise ValueError


@dataclasses.dataclass
class AssertionTransaction(Transaction):
    guid: uuid4
    verdict: bool
    bid: str
    metadata: Dict[str, Any]

    def __post_init__(self):
        if not VerdictMetadata.validate(self.metadata):
            raise ValueError


@dataclasses.dataclass
class VoteTransaction(Transaction):
    guid: uuid4
    vote: bool


