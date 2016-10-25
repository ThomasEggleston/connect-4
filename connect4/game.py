from player import Player, HumanPlayer, ComputerPlayer
from board import Board


class Game(object):
    p1_id = 1
    p2_id = 2
    p1_colour = "red"
    p2_colour = "blue"

    def __init__(self, board_width, board_height, win_seq_length, p1_is_cpu=False, p2_is_cpu=False):
        self.board = Board(board_width, board_height, win_seq_length)
        self.board_width = board_width
        self.board_height = board_height
        self.win_seq_length = win_seq_length
        self.in_progress = True

        if p1_is_cpu:
            self.p1 = ComputerPlayer(self.p1_id, "Computer Player 1", self.p1_colour, 1)
        else:
            self.p1 = HumanPlayer(self.p1_id, "Player 1", self.p1_colour)
        if p2_is_cpu:
            self.p2 = ComputerPlayer(self.p2_id, "Computer Player 2", self.p2_colour, 1)
        else:
            self.p2 = HumanPlayer(self.p2_id, "Player 2", self.p2_colour)

        self.current_player = self.p1

    def add(self, col: int) -> None:
        self.board.add(col, self.current_player.id)  # Possible ValueError raised if column is full

    def switch_player(self) -> None:
        if self.current_player == self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1

    def has_won(self) -> bool:
        state = self.board.state
        win = self.board.has_seq(self.current_player.id, self.win_seq_length)
        if win:
            self.in_progress = False  # Should look for alternative to modifying state in public function
            return True
        else:
            return False

    def get_win_information(self) -> tuple:
        state = self.board.state
        combinations = self.board.has_seq(self.current_player.id, self.win_seq_length)
        index = 0
        for (col, row) in combinations:
            row = self.invert_row(row)
            combinations[index] = (col, row)
            index += 1
        info = (self.current_player, combinations)  # (winner, list of winning positions)
        return info

    def get_target_row(self, col: int) -> int:
        """

        :param col: The integer representation of the column being used.
        :return: An integer representing which row an inserted disc will finish in.
        """
        current_discs = self.board.column_lengths[col]
        target_row = self.invert_row(current_discs) + 1
        return target_row

    @property
    def get_current_player(self) -> Player:
        return self.current_player

    def all_columns_full(self) -> bool:
        if all((self.board.column_full(column) for column in range(self.board_width))):
            self.in_progress = False  # Should look for alternative to modifying state in public function
            return True
        else:
            return False

    def invert_row(self, row: int) -> int:
        return abs(self.board_height - row) - 1
