import random as rnd
import textwrap
import time
from typing import List, Tuple, Union

from . import board


class Game:
    """Class representing a tic-tac-toe game."""

    def __init__(self, size: int, depth: int, players: Tuple[str, ...] = ("X", "O")):
        self.size = size
        self.board = board.create_board(size, depth)
        self.forfeiter = None
        self.players = players  # Works for more than 2!

    @property
    def depth(self) -> int:
        return self.board.layer

    @property
    def winner(self):
        return self.board.check_winner()

    def start(self):
        """Start the game, entering the mainloop."""
        print(
            self.board,
            textwrap.dedent(
                f"""
                Coordinates start from 0 and go up to size-1, and are expressed by [col], [row]
                e.g. for the bottom left: 0, {self.size-1}
                Type FORFEIT to forfeit the match.
                """
            ),
            sep="\n",
        )

        self._mainloop()

        if self.winner:
            print("Player {} won the game!".format(self.winner))
        elif self.forfeiter:
            print("Player {} forfeited the game.".format(self.forfeiter))
        else:
            assert False

    def _mainloop(self):
        """The game loop. Must set one of winner or forfeiter before returning."""
        move_coords = []
        player_index = 0
        game_finished = False
        while self.winner is None:
            player = self.players[player_index]
            self._perform_player_turn(player, move_coords)
            if self.forfeiter is not None:
                return
            move_coords.pop(0)
            self.board.draw_board(move_coords)
            player_index = (player_index + 1) % len(self.players)

    def _perform_player_turn(
        self, player: str, move_coords: List[Tuple[int, int]]
    ) -> None:
        """
        Perform a human player's turn, getting console input.

        Arguments:
         - player: The player whose turn it is.
         - move_coords: The list of coords for each board layer, modified in-place.

        Returns a boolean reflecting whether the game terminated on this move.
        """
        # First may need to select board layers if the default board has no
        # spaces available.
        while len(move_coords) < self.depth - 1:
            move = self._input_valid_move(
                "Player {}, choose board in layer {} (col, row): ".format(
                    player, self.depth - len(move_coords)
                )
            )
            if move == "FORFEIT":
                self.forfeiter = player
                return
            move_coords.append(move)
            if not self.board.check_move(move_coords):
                move_coords.pop()  # Remove invalid choice of board

        # Next need to make a move on the inner-most board.
        # Loop until a valid coordinate is selected.
        while True:
            move = self._input_valid_move("Move for player {}: ".format(player))
            if move == "FORFEIT":
                self.forfeiter = player
                return
            move_coords.append(move)
            is_valid_move = self.board.perform_move(player, move_coords)
            if is_valid_move:
                break
            else:
                print("The chosen cell is unavailable.")
                move_coords.pop()  # Remove the invalid move

    def _input_valid_move(self, prompt: str) -> Union[Tuple[int, int], str]:
        """
        Get user to input a coordinate (or forfeit).

        Returns one of:
         - The selected coordinate, e.g. (1, 2)
         - The literal 'FORFEIT'
        """
        move = None
        while move is None:
            move = self._parse_move(input(prompt))
            if move is None:
                print(
                    "A valid choice is either a coordinate as so: 'col, row', "
                    "or 'FORFEIT'"
                )
        return move

    def _parse_move(self, user_input: str) -> Union[Tuple[int, int], str, None]:
        """
        Parse user input expected to represent a move.

        Returns one of:
         - The selected coordinate, e.g. (1, 2)
         - The literal 'FORFEIT'
         - 'None', if parsing failed
        """
        if user_input.upper() == "FORFEIT":
            return "FORFEIT"
        # Transform to list of 2 strings which were separated by comma or spaces.
        user_input = user_input.strip(" ([)]'").replace(",", " ").split(maxsplit=1)
        try:  # Catch the case input can't be converted to int
            move = tuple(map(int, user_input))
        except ValueError:
            return
        # Check two numbers were entered (case of more than 2 already caught) and
        # that they are within the required range.
        if len(move) == 2 and 0 <= move[0] < self.size and 0 <= move[1] < self.size:
            return move


class CPUGame(Game):
    """A tic-tac-toe game against the CPU."""

    def __init__(self, size: int, depth: int):
        # if size != 3 or depth != 1:
        #     raise ValueError(
        #         "Currently only support size 3, depth 1 boards against CPU"
        #     )
        super().__init__(size, depth)
        self.cpu_player = rnd.choice(self.players)

    def _mainloop(self):
        """The game loop. Must set one of winner or forfeiter before returning."""
        move_coords = []
        player_index = 0
        game_finished = False
        while self.winner is None:
            player = self.players[player_index]
            if player == self.cpu_player:
                self._perform_cpu_turn(player, move_coords)
            else:
                self._perform_player_turn(player, move_coords)
            if self.forfeiter is not None:
                return
            move_coords.pop(0)
            self.board.draw_board(move_coords)
            player_index = (player_index + 1) % len(self.players)

    def _perform_cpu_turn(
        self, player: str, move_coords: List[Tuple[int, int]]
    ) -> None:
        time.sleep(0.5)
        all_coords = [(i, j) for i in range(self.size) for j in range(self.size)]
        while len(move_coords) < self.depth:
            rnd.shuffle(all_coords)
            for move in all_coords:
                move_coords.append(move)
                if self.board.check_move(move_coords):
                    break
                else:
                    move_coords.pop()  # Remove invalid choice
        print("CPU player {} performing move at:".format(player), move_coords)
        is_valid_move = self.board.perform_move(player, move_coords)
        assert is_valid_move
        time.sleep(0.5)


def main():
    game_type = input("Select opponent - [human]/cpu: ")
    if game_type == "cpu":
        GameCls = CPUGame
    else:
        GameCls = Game

    size = int(input("Size of board: "))
    depth = int(input("Depth of board: "))

    game = GameCls(size, depth)
    game.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting due to Ctrl+C")
