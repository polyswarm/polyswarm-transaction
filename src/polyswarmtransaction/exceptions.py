class PolySwarmTransactionException(Exception):
    pass


class InvalidKeyError(PolySwarmTransactionException):
    pass


class InvalidSignatureError(PolySwarmTransactionException):
    pass
