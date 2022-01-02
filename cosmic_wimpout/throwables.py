
class CosmicWimpoutException(Exception):
    """Base class for other cosmic wimpout exceptions"""
    pass


class PlayerInstantlyLost(CosmicWimpoutException):
    """Raised when a player performs an action that removes themselves from the game"""

    def __init__(self, message="Player instantly lost the game"):
        self.message = message
        super().__init__(self.message)


class PlayerInstantlyWon(CosmicWimpoutException):
    """Raised when a player performs an action that instantly causes them to win the game"""

    def __init__(self, message="Player instantly won the game"):
        self.message = message
        super().__init__(self.message)
