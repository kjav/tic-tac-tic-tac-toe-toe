import textwrap
from typing import Tuple, Union

from . import board


class Game:
    """Class representing a tic-tac-toe game."""

    def __init__(self, size: int, depth: int, players: Tuple[str, ...] = ("X", "O")):
        self.size = size
        self.depth = depth
        self.board = board.create_board(size, depth)
        self.winner = None
        self.forfeiter = None
        self.players = players  # Works for more than 2!

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
        while not self.board.check_winner() and not self.forfeiter:
            player = self.players[player_index]
            while len(move_coords) < self.depth - 1:
                coord = None
                while type(coord) is not tuple:
                    coord = self._parse_move(
                        input(
                            "Player {}, choose board in layer {} (col, row): ".format(
                                player, self.depth - len(move_coords)
                            )
                        )
                    )
                move_coords.append(coord)
                if not self.board.perform_move(None, move_coords):
                    move_coords.pop()  # Remove invalid choice of board
            move = None
            while move is None:
                move = self._parse_move(input("Move for player {}: ".format(player)))
                if move is None:
                    print(
                        "A valid move is either a coordinate as so: 'col, row', "
                        "or 'FORFEIT'"
                    )
            if move == "FORFEIT":
                self.forfeiter = player
            else:
                move_coords.append(move)
                is_valid_move = self.board.perform_move(player, move_coords)
                if is_valid_move:
                    self.board.draw_board(move_coords[1:])
                    move_coords.pop(0)
                    if self.board.check_winner():
                        self.winner = self.board.check_winner()
                        break
                    while not self.board.check_move(move_coords):
                        move_coords.pop()
                    player_index = (player_index + 1) % len(self.players)
                else:
                    print("The chosen cell is unavailable.")
                    move_coords.pop()  # Remove the invalid move

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
        if size != 3 or depth != 1:
            raise ValueError(
                "Currently only support size 3, depth 1 boards against CPU"
            )
        super().__init__(size, depth)

    def _mainloop(self):
        """The game loop. Must set one of winner or forfeiter before returning."""
        self.winner = self.players[0]


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
