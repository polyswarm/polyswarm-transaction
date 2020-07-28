import dataclasses

from polyswarmtransaction.transaction import Transaction


@dataclasses.dataclass
class WithdrawalTransaction(Transaction):
    amount: str


@dataclasses.dataclass
class ApproveNectarReleaseTransaction(Transaction):
    """
    Transaction from relay approving a NCT transfer from the source to the given address
    """
    destination: str  # Ethereum address 160bit hex string
    amount: str  # Nectar amount in nct-wei
    transaction_hash: str  # Transaction hash for original transfer 256 hex string
    block_hash: str  # Block hash for original transfer 256 hex string
    block_number: str  # Block number for original transfer 256 hex string
