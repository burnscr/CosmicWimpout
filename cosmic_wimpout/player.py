
__all__ = (
    'Player',
)

class Player:
    """Represents a player in the game

    Attributes
    -----------
    name: :class:`str`
        A name to identify the player.
    score: :class:`int`
        The player's accumulated score.
    alive: :class:`bool`
        A boolean representing if the player is
        still able to participate in the game.
    """

    __slots__ = (
        'name',
        'score',
        'alive',
    )

    def __init__(self, name: str, **kwargs):
        self.name: str = name
        self.score: int = kwargs.get('score', 0)
        self.alive: bool = kwargs.get('alive', True)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} name={self.name} score={self.score} alive={self.alive}>'

    def __str__(self) -> str:
        return self.name
