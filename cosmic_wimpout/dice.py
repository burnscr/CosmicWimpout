from enum import Enum
from typing import List


__all__ = (
    'Face',
    'Die',
    'BlackDie',
    'WhiteDie',
)


class Face(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    TEN = '10'
    SUN = '*'

    def __str__(self) -> str:
        return self.name


class Die:
    """Represents the core logic of a game die.

    Attributes
    -----------
    faces: List[:class:`Face`]
        A list of faces belonging to this die.
    """

    __slots__ = ('faces',)

    def __init__(self, faces: List[Face]):
        self.faces: List[Face] = faces

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} faces={self.faces}>'


class WhiteDie(Die):
    def __init__(self):
        faces: List[Face] = [Face.TWO, Face.THREE, Face.FOUR, Face.FIVE, Face.SIX, Face.TEN]
        super().__init__(faces)


class BlackDie(Die):
    def __init__(self):
        faces: List[Face] = [Face.TWO, Face.SUN, Face.FOUR, Face.FIVE, Face.SIX, Face.TEN]
        super().__init__(faces)
