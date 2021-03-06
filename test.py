#!/usr/bin/env python3

from python.board import create_board

# Create a two-layer board of size 3x3.
main_board = create_board(size=3, depth=2)
print("New game:")
print(main_board)
main_board.perform_move("O", [(0, 1), (0, 0)])
main_board.perform_move("X", [(0, 1), (1, 0)])
main_board.perform_move("O", [(0, 1), (0, 1)])
print("3 moves:")
print(main_board[0, 1])
print(main_board)
main_board.perform_move("X", [(0, 1), (2, 2)])
main_board.perform_move("O", [(0, 1), (0, 2)])  # 3 in a row
print("5 moves:")
print(main_board[0, 1])
print(main_board)
