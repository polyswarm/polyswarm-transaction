from typing import Dict, Any

from polyswarmtransaction.transaction import Transaction


class WithdrawalTransaction(Transaction):
    amount: str

    def __init__(self, amount, **kwargs):
        self.amount = amount

    @property
    def data(self) -> Dict[str, Any]:
        return {'amount': self.amount}
