import tkinter as tk

from board import Board, create_board


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

    def make_board(self, board):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()
        self.buttons = []
        for i in range(board.rows):
            buttons_row = []
            for j in range(board.cols):
                btn = tk.Button(self.main_frame, height=10, width=10, bd=3,
                    command=lambda: None)
                btn.grid(row=i, column=j)
                buttons_row.append(btn)
            self.buttons.append(buttons_row)


if __name__ == '__main__':
    main_board = create_board(3, 1)
    gui = Gui()
    gui.make_board(main_board)
    gui.mainloop()
