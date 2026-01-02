import torch
from typing import List

class GameState:
    def __init__(self):
        self.board = torch.zeros(2, 7, 6) # 2 players, 7 columns, 6 rows
        self.current_player = 0
        self.game_over = False
        self.winner = None

    def generate_valid_moves(self) -> List[int]:
        valid_moves = [i for i in range(7) if self.board[:, i, 5].sum() == 0]
        if valid_moves == []:
            self.game_over = True
        return valid_moves
    
    def move(self, move: int):
        player = self.current_player
        column = move
        column_data = self.board[:, column].sum(dim=0)
        row = column_data.argmin()
        self.board[player, column, row] = 1
        if self.check_win(player, column, row):
            self.game_over = True
            self.winner = player
        self.current_player = 1 - self.current_player

    def unmove(self, move: int):
        if self.game_over:
            self.game_over = False
            self.winner = None
        column = move
        column_data = self.board[:, column].sum(dim=0)
        for row in range(5, -1, -1):
            if column_data[row] == 1:
                break
        self.current_player = 1 - self.current_player
        self.board[self.current_player, column, row] = 0

    def check_win(self, player: int, column: int, row: int) -> bool:
        # check if the added piece creates a win for the current player
        directions = [
            (1, 0),  # horizontal (right)
            (0, 1),  # vertical (up)
            (1, 1),  # diagonal (up-right)
            (1, -1), # diagonal (down-right)
        ]
        for dx, dy in directions:
            count = 1  # Count the last placed piece
            for sign in [-1, 1]:  # go both directions
                for step in range(1, 4):
                    x = column + dx * step * sign
                    y = row + dy * step * sign
                    if 0 <= x < 7 and 0 <= y < 6:
                        if self.board[player, x, y] == 1:
                            count += 1
                        else:
                            break
                    else:
                        break
            if count >= 4:
                return True
        return False

    
