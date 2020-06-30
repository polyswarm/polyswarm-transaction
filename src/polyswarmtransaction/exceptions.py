class PolySwarmTransactionException(Exception):
    pass


class InvalidKeyError(PolySwarmTransactionException):
    pass


class InvalidSignatureError(PolySwarmTransactionException):
    pass


class WrongSignatureError(PolySwarmTransactionException):
    """
    To be raised when the payload signature does not match
    """
    pass


class WrongPayloadError(PolySwarmTransactionException):
    """
    To be raised when the signed payload does not comply with the transaction payload needed
    """
    pass


class MissingTransactionError(PolySwarmTransactionException):
    pass


class UnsupportedTransactionError(PolySwarmTransactionException):
    pass
