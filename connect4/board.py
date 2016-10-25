class Board(object):
    def __init__(self, width: int, height: int, win_seq_length: int):
        self.width = width
        self.height = height
        self.win_seq_length = win_seq_length
        self.state = [[0 for x in range(self.height)] for x in range(self.width)]
        self.column_lengths = [0 for x in range(self.width)]

    def add(self, col: int, player_number: int) -> None:
        if col not in range(self.width):
            raise ValueError("Error: Selected column out of range\n")
        if not self.column_full(col):
            row = self.column_lengths[col]
            self.state[col][row] = player_number
            self.column_lengths[col] += 1
        else:
            raise ColumnFullError("Error: Column is already full\n")

    def unmake_move(self, col: int) -> None:
        top_row = self.column_length(col) - 1
        if top_row >= 0:
            self.state[col][top_row] = 0
            self.column_lengths[col] -= 1

    def number_at_location(self, col: int, row: int) -> int:
        if col not in range(self.width):
            raise ValueError("Error: Selected column out of range\n")
        if row not in range(self.height):
            raise ValueError("Error: Selected row out of range")
        return self.board.state[col][row]

    def column_full(self, col: int):
        return self.column_lengths[col] >= self.height

    def column_length(self, col: int) -> int:
        if col not in range(self.width):
            raise ValueError("Error: Cannot return column length. Given column out of range\n")
        return self.column_lengths[col]

    def has_seq(self, player_number: int, seq_length: int) -> list:
        # directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for col in range(self.width):
            for row in range(self.height):
                if self.state[col][row] == player_number:
                    orig_pos = (col, row)
                    for d in directions:
                        seq = 0
                        pos = orig_pos
                        win_pos = []
                        while self.check_value(pos, player_number):
                            win_pos.append(pos)
                            pos = (pos[0] + d[0], pos[1] + d[1])
                            seq += 1
                        if seq >= seq_length:
                            return win_pos
        return []

    # need to improve efficiency
    def has_won(self, player_number: int) -> bool:
        if self.has_seq(player_number, self.win_seq_length):
            return True
        return False

    def sequences_of_length(self, player_number: int, seq_length: int) -> list:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        positions = []
        for col in range(self.width):
            for row in range(self.height):
                if self.state[col][row] == player_number:
                    orig_pos = (col, row)
                    for d in directions:
                        seq = 0
                        pos = orig_pos
                        pos_seq = []
                        while self.check_value(pos, player_number) and seq < seq_length:
                            # Adjusted to ignore longer sequences
                            pos_seq.append(pos)
                            pos = (pos[0] + d[0], pos[1] + d[1])
                            seq += 1
                        pos_seq_set = set(pos_seq)
                        if seq >= seq_length and pos_seq_set not in positions:
                            positions.append(pos_seq_set)
        return positions

    def check_value(self, pos: tuple, val: int) -> bool:
        col = pos[0]
        row = pos[1]

        if (0 <= col < self.width) and (0 <= row < self.height):
            if self.state[col][row] == val:
                return True
            else:
                return False
        else:
            return False

    def to_string(self) -> str:
        output = ""
        for column in range(self.width):
            for row in range(self.height):
                output += str(self.state[column][row])
        return output

    def __repr__(self):
        return str(self.state)


class ColumnFullError(ValueError):
    pass
