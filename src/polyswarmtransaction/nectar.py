import dataclasses

from polyswarmtransaction.transaction import Transaction


@dataclasses.dataclass
class WithdrawalTransaction(Transaction):
    amount: str
