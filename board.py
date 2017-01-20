

class Board:
    def __init__(self, cells):
        self.grid = cells
        self.rows = len(self.grid)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(self.grid[0])
        self.owner = None

    def __str__(self):
        piece = {None: ' ', 'O': 'O', 'X': 'X'}[self.owner]
        if self.rows == self.cols == 0:
            return piece
        else:
            result = ""
            for i in range(len(self.grid)):
                result_row = []
                for j in range(len(self.grid[0])):
                    substring = "\n".join([ " " + line + " " for line in self.grid[i][j].__str__().split('\n')])
                    if i > 0:
                        substring = "-" * (len(substring.split('\n')) + 2) + "\n" + substring
                    if j > 0:
                        new_substring = ""
                        split_substring = substring.split("\n")
                        for k in range(len(split_substring)):
                            new_substring += "|" + split_substring[k] + "\n"
                        substring = new_substring
                    result_row.append(substring)
                for k in range(len(result_row)):
                    result_row[k] = result_row[k].split('\n')
                for k in range(len(result_row[0])):
                    for r in range(len(result_row)):
                        result += result_row[r][k]
                    result += '\n'
            return result

    def perform_move(self, player, coords):
        if self.owner is None:
            coord = coords.pop(0)
            if not coord:
                self.owner = player
                return True
            is_valid = self.grid[coord[0]][coord[1]].perform_move(player,
                coords)
            self.check_completion()
            return is_valid
        else:
            return False

    def check_completion(self):
        pass






if __name__ == '__main__':
    grid = []

    for i in range(3):
        subboard_row = []
        for j in range(3):
            subsubboard = []
            for k in range(3):
                subsubboardrow = []
                for l in range(3):
                    subsubboardrow.append(Board([]))
                subsubboard.append(subsubboardrow)
            subboard_row.append(Board(subsubboard))
        grid.append(subboard_row)

    main_board = Board(grid)
    main_board.perform_move('O', [(0, 1), (0, 1), ()])
    main_board.perform_move('X', [(0, 1), (2, 1), ()])
    print(main_board)
    print("\n\n...\n\n")
    print(main_board.grid[0][1])
    print("\n\n...\n\n")
    print(main_board.grid[0][1].grid[0][1])
