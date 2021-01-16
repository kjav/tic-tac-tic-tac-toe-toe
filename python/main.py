import textwrap
from typing import Tuple, Union

from . import board


def parse_move(user_input: str) -> Union[Tuple[int, int], str, None]:
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
    if len(move) == 2 and 0 <= move[0] < size and 0 <= move[1] < size:
        return move


if __name__ == "__main__":
    size = int(input("Size of board: "))
    depth = int(input("Depth of board: "))

    main_board = board.create_board(size, depth)

    winner = None
    forfeiter = None

    print(
        main_board,
        textwrap.dedent(
            f"""
            Coordinates start from 0 and go up to size-1, and are expressed by [col], [row]
            e.g. for the bottom left: 0, {size-1}
            Type FORFEIT to forfeit the match.
            """
        ),
        sep="\n",
    )
    move_coords = []
    players = ["X", "O"]  # Works for more than 2!
    player_index = 0
    while not main_board.check_winner() and not forfeiter:
        player = players[player_index]
        while len(move_coords) < depth - 1:
            coord = None
            while type(coord) is not tuple:
                coord = parse_move(
                    input(
                        "Player {}, choose board in layer {} (col, row): ".format(
                            player, depth - len(move_coords)
                        )
                    )
                )
            move_coords.append(coord)
            if not main_board.perform_move(None, move_coords):
                move_coords.pop()  # Remove invalid choice of board
        move = None
        while move is None:
            move = parse_move(input("Move for player {}: ".format(player)))
            if move is None:
                print(
                    "A valid move is either a coordinate as so: 'col, row', "
                    "or 'FORFEIT'"
                )
        if move == "FORFEIT":
            forfeiter = player
        else:
            move_coords.append(move)
            is_valid_move = main_board.perform_move(player, move_coords)
            if is_valid_move:
                print(main_board.draw_board(move_coords[1:]))
                move_coords.pop(0)
                if main_board.check_winner():
                    winner = main_board.check_winner()
                    break
                while not main_board.check_move(move_coords):
                    move_coords.pop()
                player_index = (player_index + 1) % len(players)
            else:
                print("The chosen cell is unavailable.")
                move_coords.pop()  # Remove the invalid move

    if winner:
        print("Player {} won the board, and the game!".format(winner))
    elif forfeiter:
        print("Player {} forfeited the game.".format(forfeiter))
