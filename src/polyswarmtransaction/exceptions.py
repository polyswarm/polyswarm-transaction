class PolySwarmTransactionException(Exception):
    pass


class InvalidKeyError(PolySwarmTransactionException):
    pass


class InvalidSignatureError(PolySwarmTransactionException):
    pass


class WrongSignatureError(PolySwarmTransactionException):
    pass


class WrongPayloadError(PolySwarmTransactionException):
    pass


class MissingTransactionError(PolySwarmTransactionException):
    pass


class UnsupportedTransactionError(PolySwarmTransactionException):
    pass
