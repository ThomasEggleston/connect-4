from board import Board
from random import uniform, shuffle


class Player(object):
    def __init__(self, player_id: int, name: str, colour: str):
        self.id = player_id
        self.name = name
        self.colour = colour

    @property
    def get_id(self) -> int:
        return self.id

    @property
    def get_name(self) -> str:
        return self.name

    @property
    def get_colour(self) -> str:
        return self.colour


class HumanPlayer(Player):
    pass


class ComputerPlayer(Player):
    def __init__(self, player_id, name, colour, difficulty: int):
        super().__init__(player_id, name, colour)

        assert(0 <= difficulty <= 2)
        self.difficulty = difficulty

        assert(player_id == 1 or player_id == 2)
        if player_id == 1:
            self.opponent_id = 2
        else:
            self.opponent_id = 1

    def get_move(self, board):
        move = self.random_non_full_column(board, 0, board.width)  # Initialise with random column
        move_count = self.count_moves(board)
        if move_count == 0:
            if self.difficulty == 0:
                return move  # random column
            elif self.difficulty == 1:
                return int(board.width / 2) + int(uniform(-1, 1))  # select one of middle three columns
            else:
                return int(board.width / 2)  # select middle column
        elif 1 <= move_count <= 10:
            depth = 4
        else:
            depth = 4

        moves = []
        for column in range(board.width):
            if not board.column_full(column):
                board.add(column, self.id)
                if board.has_won(self.id):  # Make sure computer does not miss a winning move
                    board.unmake_move(column)
                    return column
                value = self.alpha_beta(board, depth, -10000, 10000, False)
                board.unmake_move(column)
                moves.append((column, value))

        shuffle(moves)  # To prevent computer from always picking the same move in a given position
        move = max(moves, key=lambda item: item[1])[0]

        return move

    def evaluate_board(self, board):  # Currently accounts for about 90% of alpha-beta search time
        empty_slots = []
        for column in range(board.width):
            for row in range(board.height):
                if board.check_value((column, row), 0):
                    empty_slots.append((column, row))

        this_player = 0
        other_player = 0

        for pos in empty_slots:
            column = pos[0]
            row = pos[1]

            board.state[column][row] = self.id

            if board.has_won(self.id):
                this_player += 1

            board.state[column][row] = self.opponent_id

            if board.has_won(self.opponent_id):
                other_player += 1

            board.state[column][row] = 0

        return this_player - other_player

    def mini_max(self, board: Board, depth: int, max_player: bool) -> int:
        if board.has_won(self.id):
            return 1000

        if board.has_won(self.opponent_id):
            return -1000

        if depth == 0:
            return self.evaluate_board(board)

        if self.count_moves(board) % 2 == 0:
            player = 1
        else:
            player = 2

        if max_player:

            best_value = -1000000
            for column in range(board.width):
                if not board.column_full(column):  # column not full
                    board.add(column, player)
                    value = self.mini_max(board, depth - 1, False)
                    board.unmake_move(column)
                    best_value = max(best_value, value)
            return best_value

        else:

            best_value = 1000000
            for column in range(board.width):
                if not board.column_full(column):
                    board.add(column, player)
                    value = self.mini_max(board, depth - 1, True)
                    board.unmake_move(column)
                    best_value = min(best_value, value)
            return best_value

    def alpha_beta(self, board: Board, depth: int, alpha: int, beta: int, max_player: bool) -> int:
        if board.has_won(self.id):
            return 1000

        if board.has_won(self.opponent_id):
            return -1000

        if depth == 0:
            return self.evaluate_board(board)

        if self.count_moves(board) % 2 == 0:
            player = 1
        else:
            player = 2

        if max_player:

            best_value = -1000000
            for column in range(board.width):
                if not board.column_full(column):  # column not full
                    board.add(column, player)
                    value = self.alpha_beta(board, depth - 1, alpha, beta, False)
                    board.unmake_move(column)
                    best_value = max(best_value, value)
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
            return best_value

        else:

            best_value = 1000000
            for column in range(board.width):
                if not board.column_full(column):
                    board.add(column, player)
                    value = self.alpha_beta(board, depth - 1, alpha, beta, True)
                    board.unmake_move(column)
                    best_value = min(best_value, value)
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
            return best_value

    @staticmethod
    def count_moves(board: Board) -> int:
        moves = 0
        for column in range(board.width):
            moves += board.column_lengths[column]
        return moves

    @staticmethod
    def random_non_full_column(board, lower: int, upper: int) -> int:
        column = 0
        found = False
        while not found:
            column = int(uniform(lower, upper))
            if not board.column_full(column):
                found = True
        return column
