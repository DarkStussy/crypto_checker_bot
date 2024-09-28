class CryptoCheckerError(Exception):
    def __init__(self, message: str):
        self.message = message


class UserNotFound(CryptoCheckerError):
    def __init__(self, message: str = "User not found"):
        self.message = message


class PairNotFound(CryptoCheckerError):
    def __init__(self, message: str = "Pair not found"):
        self.message = message


class PairExists(CryptoCheckerError):
    def __init__(self, message: str = "Pair already exists"):
        self.message = message


class PairsLimitExceeded(CryptoCheckerError):
    def __init__(self, message: str = "Pairs limit exceeded (50)"):
        self.message = message
