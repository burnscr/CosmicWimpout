#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cosmic Wimpout implementation

Author: Christian Burns
Date:   December 1, 2021
See:    https://www.cosmicwimpout.com/how-to-play
"""

from random import choice
from typing import Optional, Dict, Any, Callable, TypeVar, List

from dice import BlackDie, WhiteDie, Face
from decorators import validate_choice
from throwables import PlayerInstantlyWon, PlayerInstantlyLost


TurnStateT = TypeVar('TurnStateT', bound='TurnState')
ScoreRule = Callable[[TurnStateT], Any]


class TurnState:
    """Represents the state of a turn in progress.

    Attributes
    -----------
    score: :class:`int`
        The total accumulated score for this turn.
    white_die: :class:`WhiteDie`
        The die object used to represent white dice.
    black_die: :class:`BlackDie`
        The die object used to represent black dice.
    scoring_dice: :class:`bool`
        A boolean representing if at least one die
        scored points for the last roll.
    remaining_white: :class:`int`
        The number of white dice still able to be rolled.
    remaining_black: :class:`bool`
        A boolean representing if the black die is still
        able to be rolled.
    white_die_rolls: Dict[:class:`Face`, :class:`int`]
        A dictionary mapping each face of :class:`WhiteDie`
        to the number of times it was rolled.
    black_die_roll: Optional[:class:`Face`]
        The face rolled on a :class:`BlackDie`, or ``None``
        if the die was not rolled.
    clearing_face: Optional[:class:`Face`]
        The face that must be cleared in order to continue
        scoring points, or ``None`` if not present.
    """

    __slots__ = (
        'score',
        'white_die',
        'black_die',
        'scoring_dice',
        'remaining_white',
        'remaining_black',
        'white_die_rolls',
        'black_die_roll',
        'clearing_face',
    )

    def __init__(self, **kwargs: Dict[str, Any]):
        self.score: int = kwargs.get('score', 0)
        self.white_die: WhiteDie = kwargs.get('white_die') or WhiteDie()
        self.black_die: BlackDie = kwargs.get('black_die') or BlackDie()
        self.scoring_dice: bool = kwargs.get('scoring_dice', False)
        self.remaining_white: int = kwargs.get('remaining_white', 4)
        self.remaining_black: bool = kwargs.get('remaining_black', True)
        self.white_die_rolls: Dict[Face, int] = kwargs.get('white_die_rolls') or {}
        self.black_die_roll: Optional[Face] = kwargs.get('black_die_roll')
        self.clearing_face: Optional[Face] = kwargs.get('clearing_face')


class ScoringLogic:
    """

    """

    def __init__(self):
        self.__score_rules__: List[ScoreRule] = [
            self.__score_rule__five_of_a_kind,
            self.__score_rule__three_of_a_kind,
            self.__score_rule__forced_three_of_a_kind,
            self.__score_rule__single_scoring_dice,
            self.__score_rule__single_sun_die,
        ]

    def ingest(self, state: TurnState) -> None:
        for rule in self.__score_rules__:
            rule(state)

    def __score_rule__five_of_a_kind(self, state: TurnState) -> None:
        pass

    def __score_rule__three_of_a_kind(self, state: TurnState) -> None:
        pass

    def __score_rule__forced_three_of_a_kind(self, state: TurnState) -> None:
        pass

    def __score_rule__single_scoring_dice(self, state: TurnState) -> None:
        pass

    def __score_rule__single_sun_die(self, state: TurnState) -> None:
        pass


class TurnLogic:
    """The core game logic to score a single turn.

    Attributes
    -----------
    score: :class:`int`
        The total accumulated score for this turn.
    white_die: :class:`WhiteDie`
        The die object used to represent white dice.
    black_die: :class:`BlackDie`
        The die object used to represent black dice.
    scoring_dice: :class:`bool`
        A boolean representing if at least one die
        scored points for the last roll.
    remaining_white: :class:`int`
        The number of white dice still able to be rolled.
    remaining_black: :class:`bool`
        A boolean representing if the black die is still
        able to be rolled.
    white_die_rolls: Dict[:class:`Face`, :class:`int`]
        A dictionary mapping each face of :class:`WhiteDie`
        to the number of times it was rolled.
    black_die_roll: Optional[:class:`Face`]
        The face rolled on a :class:`BlackDie`, or ``None``
        if the die was not rolled.
    clearing_face: Optional[:class:`Face`]
        The face that must be cleared in order to continue
        scoring points, or ``None`` if not present.
    """

    __slots__ = (
        'score',
        'white_die',
        'black_die',
        'scoring_dice',
        'remaining_white',
        'remaining_black',
        'white_die_rolls',
        'black_die_roll',
        'clearing_face',
        '_state',
    )

    def __init__(self):
        self.score: int = 0
        self.white_die: WhiteDie = WhiteDie()
        self.black_die: BlackDie = BlackDie()
        self.scoring_dice: bool = False
        self.remaining_white: int = 4
        self.remaining_black: bool = True
        self.white_die_rolls: Dict[Face, int] = {}
        self.black_die_roll: Optional[Face] = None
        self.clearing_face: Optional[Face] = None
        self._state: TurnState = TurnState()

    def reset(self) -> None:
        self.score = 0
        self.scoring_dice = False
        self.remaining_white = 4
        self.remaining_black = True
        self.white_die_rolls = {}
        self.black_die_roll = None
        self.clearing_face = None

    def resolve_turn(self):
        should_continue = True

        while should_continue:
            self._resolve_turn()

            # if all dice were used, we should continue
            if self.remaining_white == 0 and not self.remaining_black:
                self.remaining_white = 4
                self.remaining_black = True
                should_continue = True
                print('[DEBUG] All dice were consumed, so the turn continues')
                if self.clearing_face is not None:
                    print(f'[DEBUG] The "{self.clearing_face.value}" face must be cleared')
            # if a clearing face was set, we should continue
            elif self.clearing_face is not None:
                should_continue = True
                print(f'[DEBUG] The "{self.clearing_face.value}" face must be cleared, so the turn continues')
            # if no scoring dice were rolled, we need to stop
            elif not self.scoring_dice:
                should_continue = False
                print('[DEBUG] No scoring dice were rolled, so the turn ends with no points scored')
                print(f'[DEBUG] Score {self.score} -> 0')
                self.score = 0
            # ask the user if they want to keep playing
            else:
                should_continue = self._get_keep_playing_choice() == 1

    def _resolve_turn(self):
        self._roll_dice()

        print()
        self.print_roll()
        print()

        self.scoring_dice = False
        self.clearing_face = None

        self._test_five_of_a_kind()
        self._test_three_of_a_kind()
        self._test_forced_three_of_a_kind()
        self._test_single_scoring_dice()
        self._test_single_sun_die()

    def _test_five_of_a_kind(self) -> None:

        # Shortcut if black die was not rolled
        if self.black_die_roll is None:
            return

        for face in self.white_die.faces:
            if self.white_die_rolls.get(face, 0) == 4 and self.black_die_roll == face:
                points = self.get_five_of_a_kind_points(face)
                print(f'[DEBUG] Rolled five "{face.value}" faces and increased score by {points} points')
                self.score += points
                self.white_die_rolls[face] = 0
                self.black_die_roll = None
                self.remaining_white = 0
                self.remaining_black = False
                self.scoring_dice = True

    def _test_three_of_a_kind(self) -> None:
        for face in self.white_die.faces:
            # check for three of a kind using only white dice
            if self.white_die_rolls.get(face, 0) >= 3:
                points = self.get_three_of_a_kind_points(face)
                print(f'[DEBUG] Rolled three "{face.value}" faces and increased score by {points} points')
                self.score += points
                self.clearing_face = face
                self.white_die_rolls[face] -= 3
                self.remaining_white -= 3
                self.scoring_dice = True

            # check for three of a kind using black die
            elif self.white_die_rolls.get(face, 0) == 2 and self.black_die_roll == face:
                points = self.get_three_of_a_kind_points(face)
                print(f'[DEBUG] Rolled three "{face.value}" faces and increased score by {points} points')
                self.score += points
                self.clearing_face = face
                self.white_die_rolls[face] -= 2
                self.black_die_roll = None
                self.remaining_white -= 2
                self.remaining_black = False
                self.scoring_dice = True

    def _test_forced_three_of_a_kind(self) -> None:
        forced_three_of_a_kind = []

        if self.black_die_roll == Face.SUN:
            for face in self.white_die.faces:
                if self.white_die_rolls.get(face, 0) == 2:
                    forced_three_of_a_kind.append(face)

        if len(forced_three_of_a_kind) == 1:
            face = forced_three_of_a_kind[0]
            points = self.get_three_of_a_kind_points(face)
            print(f'[DEBUG] Rolled two white "{face.value}" faces and a wild sun and increased score by {points} points')
            self.score += points
            self.clearing_face = face
            self.white_die_rolls[face] -= 2
            self.black_die_roll = None
            self.remaining_white -= 2
            self.remaining_black = False
            self.scoring_dice = True

        elif len(forced_three_of_a_kind) > 1:
            face_index = self._get_sun_trio_choice(forced_three_of_a_kind) - 1
            face = forced_three_of_a_kind[face_index]
            points = self.get_three_of_a_kind_points(face)
            print(f'[DEBUG] Rolled two white "{face.value}" faces and a wild sun and increased score by {points} points')
            self.score += points
            self.clearing_face = face
            self.white_die_rolls[face] -= 2
            self.black_die_roll = None
            self.remaining_white -= 2
            self.remaining_black = False
            self.scoring_dice = True

    def _test_single_scoring_dice(self) -> None:
        white_die_rolls = self.white_die_rolls
        black_die_roll = self.black_die_roll

        if white_die_rolls.get(Face.FIVE, 0) > 0:
            num_white_fives = white_die_rolls[Face.FIVE]
            points = num_white_fives * 5
            print(f'[DEBUG] Rolled {num_white_fives} white "5" faces and increased score by {points} points')
            self.score += points
            self.white_die_rolls[Face.FIVE] -= num_white_fives
            self.remaining_white -= num_white_fives
            self.scoring_dice = True

        if black_die_roll == Face.FIVE:
            print('[DEBUG] Rolled a black "5" face and increased score by 5 points')
            self.score += 5
            self.black_die_roll = None
            self.remaining_black = False
            self.scoring_dice = True

        if white_die_rolls.get(Face.TEN, 0) > 0:
            num_white_tens = white_die_rolls[Face.TEN]
            points = num_white_tens * 10
            print(f'[DEBUG] Rolled {num_white_tens} white "10" faces and increased score by {points} points')
            self.score += points
            self.white_die_rolls[Face.TEN] -= num_white_tens
            self.remaining_white -= num_white_tens
            self.scoring_dice = True

        if black_die_roll == Face.TEN:
            print('[DEBUG] Rolled a black "10" face and increased score by 10 points')
            self.score += 10
            self.black_die_roll = None
            self.remaining_black = False
            self.scoring_dice = True

    def _test_single_sun_die(self) -> None:
        if self.black_die_roll == Face.SUN:
            # if dice were already scored, the user doesn't have to use the sun die
            if self.scoring_dice:
                if self._get_sun_die_use_choice() == 2:
                    return
            points = (5, 10)[self._get_sun_die_point_choice()-1]
            print(f'[DEBUG] Sun die increased score by {points} points')
            self.score += points
            self.black_die_roll = None
            self.remaining_black = False
            self.scoring_dice = True

    def _roll_dice(self) -> None:
        # Copying the faces since we may need to mutate them
        white_die_faces = self.white_die.faces.copy()
        black_die_faces = self.black_die.faces.copy()
        clearing_face = self.clearing_face

        # remove clearing face from face options if present
        if clearing_face in white_die_faces:
            white_die_faces.remove(clearing_face)
        if clearing_face in black_die_faces:
            black_die_faces.remove(clearing_face)

        # resolve white dice
        white_die_rolls = {}
        for _ in range(self.remaining_white):
            roll = choice(white_die_faces)
            if roll not in white_die_rolls:
                white_die_rolls[roll] = 0
            white_die_rolls[roll] += 1
        self.white_die_rolls = white_die_rolls

        # resolve black die
        black_die_roll = None
        if self.remaining_black:
            black_die_roll = choice(black_die_faces)
        self.black_die_roll = black_die_roll

    @staticmethod
    def get_five_of_a_kind_points(face: Face) -> int:
        """Gets points for rolling five matching faces
        :param face: die face rolled five times
        :return: number of points player earned
        :raises PlayerInstantlyWon:  if face is a six
        :raises PlayerInstantlyLost: if face is a ten
        """
        # rolling five sixes means you instantly win the game
        if face == Face.SIX:
            raise PlayerInstantlyWon()
        # rolling five tens means you instantly lose the game
        if face == Face.TEN:
            raise PlayerInstantlyLost()
        # return the corresponding point value for the face
        points = {Face.TWO: 200, Face.FOUR: 400, Face.FIVE: 500}
        return points.get(face, 0)

    @staticmethod
    def get_three_of_a_kind_points(face: Face) -> int:
        """Gets points for rolling three matching faces
        :param face: die face rolled three times
        :return: number of points player earned
        """
        points = {Face.TWO: 20, Face.THREE: 30, Face.FOUR: 40,
                  Face.FIVE: 50, Face.SIX: 60, Face.TEN: 100}
        return points.get(face, 0)

    @staticmethod
    @validate_choice(range(1, 3))
    def _get_sun_trio_choice(faces):
        print('\nPlease choose which face to make a trio with using the sun die:')
        for index, face in enumerate(faces):
            print(f'\t[{index + 1}] Face "{face.value}"')
        return input('>>> ')

    @staticmethod
    @validate_choice(range(1, 3))
    def _get_sun_die_use_choice():
        print('\nYou rolled a sun face. Do you want to use it for points or reuse the die?')
        print('\t[1] Use it for points')
        print('\t[2] Keep the die for later')
        return input('>>> ')

    @staticmethod
    @validate_choice(range(1, 3))
    def _get_sun_die_point_choice():
        print('\nDo you want to use the sun face for "5" or "10" points?')
        print('\t[1] Use it for five points')
        print('\t[2] Use it for ten points')
        return input('>>> ')

    @validate_choice(range(1, 3))
    def _get_keep_playing_choice(self):
        dice_left = self.remaining_white
        if self.remaining_black:
            dice_left += 1
        print(f'\nYou currently scored {self.score} points this turn and have {dice_left} dice left. Keep going?')
        print('\t[1] Keep playing')
        print('\t[2] End turn')
        return input('>>> ')

    def print_roll(self) -> None:
        print('Dice:', end=' ')
        for face, count in self.white_die_rolls.items():
            for _ in range(count):
                print(f'[{face.value}]', end=' ')
        if self.black_die_roll is not None:
            print(f'({self.black_die_roll.value})', end=' ')
        print()


# class CosmicWimpout:
#     def __init__(self, players: int, goal: int = 500):
#         """
#         :param players: number of players
#         :param goal:    number of points needed to win (usually 300 or 500)
#         """
#         self.goal = goal
#         self.players: List[Player] = []
#         for index in range(players):
#             self.players.append(Player(name=f'Player {index}'))
#
#     def play(self):
#         # This becomes the first player who's score meets or exceeds
#         # the desired goal. All other players take one more turn.
#         first_player_to_meet_the_goal: Optional[Player] = None
#         current_winner = None
#
#         # The game will keep running until either the victory condition
#         # was met or all players got disqualified due to a supernova.
#         game_in_progress: bool = True
#
#         while game_in_progress:
#             for player in self.players:
#
#                 # Skip if this player is not alive
#                 if not player.alive:
#                     continue
#
#                 # If this player matches first_player_to_meet_the_goal, then
#                 # this marks the end of the final round. The game is finished
#                 if player == first_player_to_meet_the_goal:
#                     game_in_progress = False
#                     break  # no need to process the remaining players
#
#                 # If this player was disqualified due to rolling a supernova
#                 if player.score < 0:
#                     continue
#
#                 # Number of points accumulated after the player's turn is resolved
#                 points_earned = 0  # TODO: method call here
#
#                 # Only increment the player's score if they weren't disqualified
#                 # due to a supernova (rolling all 10's). Otherwise, disqualify the score.
#                 if points_earned is not None:
#                     self.scores[player] += points_earned
#
#                     # Check if this marks the start of the final round
#                     if first_player_to_meet_the_goal is None \
#                             and self.scores[player] >= self.goal:
#                         first_player_to_meet_the_goal = player
#                         current_winner = player
#                     # elif first_player_to_meet_the_goal is not None \
#                     #         and


def main():
    turn_logic = TurnLogic()
    turn_logic.resolve_turn()
    print(f'\nTotal score: {turn_logic.score}')


if __name__ == '__main__':
    main()
