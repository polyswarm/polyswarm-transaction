import dataclasses

from polyswarmtransaction.transaction import Transaction


@dataclasses.dataclass(init=True)
class WithdrawalTransaction(Transaction):
    amount: str
