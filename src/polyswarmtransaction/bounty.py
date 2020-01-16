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


